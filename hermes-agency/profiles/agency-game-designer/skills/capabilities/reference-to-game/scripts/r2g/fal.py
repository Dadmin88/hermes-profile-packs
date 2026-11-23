"""Queue adapter with explicit submission, local deduplication and durable intent.
Not exactly-once delivery: ambiguous network outcomes deliberately require reconciliation.
"""
from __future__ import annotations
import hashlib, json, math, os, re, urllib.request
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit
from .core import read,write

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Unexpected redirect from fal queue')

def queue_url(url):
    u=urlsplit(url)
    if u.scheme!='https' or u.netloc!='queue.fal.run' or u.username or u.password or u.fragment:
        raise ValueError('Untrusted queue URL')
    return url

def transport(method,url,payload=None):
    queue_url(url);key=os.environ.get('FAL_KEY')
    if not key:raise ValueError('Set FAL_KEY in the server environment, never in client code')
    data=None if payload is None else json.dumps(payload,allow_nan=False).encode()
    req=urllib.request.Request(url,data=data,method=method,headers={'Authorization':'Key '+key,'Content-Type':'application/json'})
    with urllib.request.build_opener(NoRedirect).open(req,timeout=60) as r:return json.load(r)

@contextmanager
def locked(root):
    lock=Path(root)/'production/fal/.lock';lock.parent.mkdir(parents=True,exist_ok=True)
    try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError:raise ValueError('fal ledger is locked. Check for a running submit before recovering a stale lock.')
    try:
        os.write(fd,str(os.getpid()).encode());os.close(fd);yield
    finally:lock.unlink(missing_ok=True)

def submit(root,asset,endpoint,payload,estimate,execute=False,send=transport):
    root=Path(root)
    if not re.fullmatch(r'[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_.-]+)+',endpoint) or '..' in endpoint:raise ValueError('Invalid fal endpoint ID')
    if not isinstance(payload,dict):raise ValueError('Model input must be a JSON object')
    if not isinstance(estimate,(int,float)) or not math.isfinite(estimate) or estimate<=0:raise ValueError('Supply a positive finite cost estimate')
    items=read(root/'assets.json')['items']
    if not any(a.get('id')==asset for a in items):raise ValueError('Asset must exist in assets.json first')
    canonical=json.dumps({'asset':asset,'endpoint':endpoint,'input':payload},sort_keys=True,separators=(',',':'),allow_nan=False)
    jobid=hashlib.sha256(canonical.encode()).hexdigest()[:24]
    path=root/'production/fal'/f'{jobid}.json'
    if not execute:return {'dry_run':True,'job_id':jobid,'estimated_usd':estimate,'endpoint':endpoint,'asset':asset}
    with locked(root):
        if path.exists():return read(path)
        cfg=read(root/'case.json')['generation'];budget=cfg.get('budget_usd',0)
        if not cfg.get('enabled'):raise ValueError('Asset generation is not enabled in case.json')
        if not isinstance(budget,(int,float)) or not math.isfinite(budget) or budget<=0:raise ValueError('Set a finite positive generation budget')
        reserved=sum(read(p)['estimated_usd'] for p in path.parent.glob('*.json'))
        if reserved+estimate>budget+1e-9:raise ValueError('Estimated generation budget exceeded')
        record={'job_id':jobid,'asset':asset,'endpoint':endpoint,'input':payload,'estimated_usd':estimate,
                'actual_usd':None,'state':'submitting','request_id':None,'created_at':datetime.now(timezone.utc).isoformat()}
        write(path,record) # Durable intent before any potentially billable action.
        try:
            response=send('POST','https://queue.fal.run/'+endpoint,payload)
            if not response.get('request_id'):raise ValueError('Queue response missing request ID')
            for k in ['status_url','response_url']:queue_url(response[k])
            record.update(state='submitted',request_id=response['request_id'],status_url=response['status_url'],response_url=response['response_url'])
            write(path,record)
        except Exception:
            record['state']='ambiguous';record['note']='Submission response unavailable. Reconcile in fal dashboard; do not automatically resubmit.'
            write(path,record)
            raise ValueError('Submission outcome ambiguous; durable record saved. Inspect the fal dashboard before any retry.') from None
        return record

def status(root,jobid,send=transport):
    if not re.fullmatch(r'[a-f0-9]{24}',jobid):raise ValueError('Invalid job ID')
    root=Path(root)
    with locked(root):
        path=root/'production/fal'/f'{jobid}.json';job=read(path)
        if job['state']=='completed':return job
        if job['state'] not in ('submitted','running'):raise ValueError('No pollable request; reconcile the job record first')
        response=send('GET',queue_url(job['status_url']))
        state=response.get('status');job['queue_status']=state
        if state=='COMPLETED':
            job['result']=send('GET',queue_url(job['response_url']));job['state']='completed'
        elif state in ('IN_QUEUE','IN_PROGRESS'):job['state']='running'
        elif state in ('FAILED','CANCELLED'):job['state']='failed'
        else:raise ValueError('Unexpected queue status; record preserved')
        write(path,job);return job

"""Offline evidence index; no scripts, external resources or reference execution."""
from html import escape
from pathlib import Path
from urllib.parse import quote,urlsplit
from .core import read,contained

def page(root):
    root=Path(root).resolve();case=read(root/'case.json');review=read(root/'review.json')
    def local(rel):
        p=contained(root,rel)
        return '../'+quote(p.relative_to(root).as_posix())
    cards=[]
    for ref in case['references']:
        label=escape(ref['id']+' · '+ref['kind']+' · '+ref.get('role','unassigned'))
        body='<p>Open the original with the appropriate viewer.</p>'
        if ref.get('path'):
            url=local(ref['path'])
            if ref['kind']=='image':body=f'<img loading="lazy" src="{url}" alt="{label}">'
            elif ref['kind']=='video':body=f'<video controls preload="metadata" src="{url}"></video>'
            elif ref['kind']=='audio':body=f'<audio controls preload="metadata" src="{url}"></audio>'
            body+=f'<p><a href="{url}">Open original</a></p>'
        else:
            if urlsplit(ref['source']).scheme not in ('http','https'):raise ValueError('Only HTTP(S) reference links may be displayed')
            body=f'<p>Link only; inspection required.</p><a rel="noreferrer" href="{escape(ref["source"],quote=True)}">Open supplied link</a>'
        cards.append(f'<article><h3>{label}</h3>{body}<p>{escape(ref.get("notes",""))}</p></article>')
    checks=[]
    for name,item in review['checks'].items():
        links=[]
        for e in item['evidence']:
            url=local(e['path']);links.append(f'<li><a href="{url}">{escape(e["path"])}</a></li>')
        checks.append(f'<article><h3>{escape(name)} <span>{escape(item["status"])}</span></h3><p>{escape(item["notes"])}</p><ul>{"".join(links)}</ul></article>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reference review</title>
<style>body{margin:0;background:#f3f1eb;color:#253730;font:16px/1.6 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:48px 24px}header{border-bottom:1px solid #ccd3c9;padding-bottom:28px;margin-bottom:32px}small{letter-spacing:.15em;font-weight:700}h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15;margin:.4em 0}h2{margin-top:48px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:20px}article{background:white;padding:20px;border:1px solid #d8dfd5;border-radius:12px}h3{margin:0 0 16px;font-size:16px}img,video{width:100%;height:auto;max-height:520px;object-fit:contain;background:#f3f1eb}audio{width:100%}a{color:#196d66;overflow-wrap:anywhere}span{font-size:12px;background:#ecf0e8;padding:4px 8px;border-radius:20px}p{white-space:pre-wrap}footer{margin-top:40px;color:#5e6c64;font-size:14px}</style>
<main><header><small>REFERENCE TO GAME / EVIDENCE</small>'''
    html+=f'<h1>{escape(case["title"])}</h1><p>{escape(case["brief"])}</p><p>Engine preference: {escape(case["engine"])}</p></header>'
    html+='<h2>Source references</h2><div class="grid">'+''.join(cards)+'</div><h2>Review record</h2><div class="grid">'+''.join(checks)+'</div>'
    html+='<footer>These are author attestations and source artifacts. Inspect the game and evidence; this page does not independently certify quality or gameplay.</footer></main></html>'
    out=root/'review/index.html';out.parent.mkdir(exist_ok=True);out.write_text(html,encoding='utf-8');return out

#!/usr/bin/env python3
"""Reference-to-game intake, review and generation ledger CLI."""
from __future__ import annotations
import argparse,json,shutil,sys
from pathlib import Path
from r2g.core import init_case,validate,make_prompt,write,read,fingerprint,digest,contained,CHECKS

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('init',help='Preserve local references and scaffold a neutral case')
    p.add_argument('case');p.add_argument('--input',action='append',default=[]);p.add_argument('--brief',default='');p.add_argument('--title');p.add_argument('--engine',default='threejs')
    p=sub.add_parser('inspect',help='Inspect metadata and extract video frames without changing originals')
    p.add_argument('case');p.add_argument('--frames',type=int,default=6)
    p=sub.add_parser('palette',help='Sample named semantic color roles at explicit normalized coordinates')
    p.add_argument('image');p.add_argument('--points',required=True);p.add_argument('--out',required=True)
    p=sub.add_parser('compare',help='Create a labelled reference/implementation comparison')
    p.add_argument('reference');p.add_argument('implementation');p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=960)
    p=sub.add_parser('prompt',help='Write a complete implementation handoff using this case')
    p.add_argument('case');p.add_argument('--out')
    p=sub.add_parser('validate',help='Check case integrity; --release checks fresh evidence and signoffs')
    p.add_argument('case');p.add_argument('--release',action='store_true')
    p=sub.add_parser('review-page',help='Build an offline reference and evidence viewer')
    p.add_argument('case')
    p=sub.add_parser('freeze',help='Fingerprint authored source and contract for a review revision')
    p.add_argument('case')
    p=sub.add_parser('evidence',help='Attach a completed review and hashed local evidence; does not run the check')
    p.add_argument('case');p.add_argument('check',choices=CHECKS);p.add_argument('--file',action='append',required=True);p.add_argument('--notes',required=True)
    p=sub.add_parser('install-core',help='Copy the tested neutral runtime helpers into a case')
    p.add_argument('case')
    p=sub.add_parser('fal-submit',help='Plan a fal job; --execute actually submits with configured budget')
    p.add_argument('case');p.add_argument('--asset',required=True);p.add_argument('--endpoint',required=True);p.add_argument('--input',required=True);p.add_argument('--estimate',type=float,required=True);p.add_argument('--execute',action='store_true')
    p=sub.add_parser('fal-status',help='Poll a recorded fal request once; never resubmits')
    p.add_argument('case');p.add_argument('job')
    a=parser.parse_args(argv)
    try:
        if a.command=='init':result=init_case(a.case,a.input,a.brief,a.title,a.engine)
        elif a.command=='inspect':
            from r2g.media import inspect
            result=inspect(a.case,a.frames)
        elif a.command=='palette':
            from r2g.media import palette
            result=palette(a.image,read(a.points));write(a.out,result)
        elif a.command=='compare':
            from r2g.media import compare
            result=compare(a.reference,a.implementation,a.out,a.width)
        elif a.command=='prompt':
            prompt=make_prompt(a.case)
            if a.out:Path(a.out).write_text(prompt,encoding='utf-8')
            else:print(prompt)
            return 0
        elif a.command=='validate':
            errors=validate(a.case,a.release);print(json.dumps({'ok':not errors,'errors':errors},indent=2));return 1 if errors else 0
        elif a.command=='review-page':
            from r2g.viewer import page
            result={'page':str(page(a.case))}
        elif a.command=='freeze':
            sha,files=fingerprint(a.case);root=Path(a.case)
            write(root/'review/source-snapshot.json',{'fingerprint':sha,'files':files})
            review=read(root/'review.json');review['build_fingerprint']=sha
            for entry in review['checks'].values():entry.update(status='pending',evidence=[],notes='')
            write(root/'review.json',review);result={'fingerprint':sha,'note':'All review signoffs reset; this fingerprints source, not a built binary.'}
        elif a.command=='evidence':
            root=Path(a.case).resolve();review=read(root/'review.json')
            if fingerprint(root)[0]!=review.get('build_fingerprint'):raise ValueError('Run freeze on current source before attaching evidence')
            if not a.notes.strip():raise ValueError('Review notes cannot be blank')
            evidence=[]
            for raw in a.file:
                path=contained(root,raw)
                evidence.append({'path':path.relative_to(root).as_posix(),'sha256':digest(path)})
            review['checks'][a.check]={'status':'passed','evidence':evidence,'notes':a.notes};write(root/'review.json',review)
            result={'attached':a.check,'note':'Author attestation recorded, not independently verified.'}
        elif a.command=='install-core':
            root=Path(a.case);read(root/'case.json');dest=root/'app/lib/reference-core'
            shutil.copytree(Path(__file__).resolve().parent.parent/'assets/runtime',dest)
            result={'installed':str(dest)}
        elif a.command=='fal-submit':
            from r2g.fal import submit
            result=submit(a.case,a.asset,a.endpoint,read(a.input),a.estimate,a.execute)
        elif a.command=='fal-status':
            from r2g.fal import status
            result=status(a.case,a.job)
        print(json.dumps(result,indent=2,ensure_ascii=False));return 0
    except (ValueError,OSError,KeyError,TypeError) as e:
        print('r2g: '+str(e),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())

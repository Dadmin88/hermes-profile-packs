"""Inspection helpers. Measurements support, but never replace, visual review."""
from __future__ import annotations
import json, math, shutil, subprocess
from pathlib import Path
from .core import read, write, contained, digest

def pillow():
    try:
        from PIL import Image,ImageOps,ImageDraw,ImageStat
        return Image,ImageOps,ImageDraw,ImageStat
    except ImportError as e:raise ValueError('Install Pillow: python3 -m pip install Pillow') from e

def load_rgb(path):
    Image,ImageOps,_,_=pillow()
    with Image.open(path) as src:
        image=ImageOps.exif_transpose(src).convert('RGBA')
        # Explicit neutral compositing for review; originals remain untouched.
        bg=Image.new('RGBA',image.size,(128,128,128,255));bg.alpha_composite(image)
        return bg.convert('RGB')

def probe(path):
    if not shutil.which('ffprobe'):raise ValueError('ffprobe is required for audio/video inspection')
    r=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],capture_output=True,text=True,timeout=60)
    if r.returncode:raise ValueError('ffprobe could not decode '+Path(path).name)
    return json.loads(r.stdout)

def inspect(root,frames=6):
    root=Path(root);c=read(root/'case.json');result=[]
    if not 1<=frames<=24:raise ValueError('frames must be between 1 and 24')
    for ref in c['references']:
        row={'reference_id':ref['id'],'kind':ref['kind'],'inspection':'pending'}
        p=contained(root,ref['path']) if ref.get('path') else None
        try:
            if ref['kind']=='image':
                Image,ImageOps,_,_=pillow()
                with Image.open(p) as im:
                    oriented=ImageOps.exif_transpose(im)
                    row.update(size=list(oriented.size),format=im.format,mode=im.mode,embedded_icc=bool(im.info.get('icc_profile')),inspection='metadata-read')
            elif ref['kind'] in ('video','audio'):
                meta=probe(p);write(root/'analysis'/f"{ref['id']}-probe.json",meta)
                row['inspection']='metadata-read'
                if ref['kind']=='video':
                    if not shutil.which('ffmpeg'):raise ValueError('ffmpeg is required to extract video frames')
                    dur=float(meta.get('format',{}).get('duration',0))
                    if not math.isfinite(dur) or dur<=0:raise ValueError('Video duration is unavailable')
                    out=root/'analysis'/ref['id'];out.mkdir(parents=True,exist_ok=True)
                    row['frames']=[]
                    for i in range(frames):
                        t=dur*i/frames
                        target=out/f'frame-{i:02d}.png'
                        cmd=['ffmpeg','-v','error','-y','-i',str(p),'-ss',str(t),'-frames:v','1','-vf','scale=trunc(iw*sar/2)*2:ih,setsar=1,scale=960:960:force_original_aspect_ratio=decrease:force_divisible_by=2',str(target)]
                        # Decode by requested timestamp; ffmpeg applies display rotation. Probe retains SAR/rotation.
                        r=subprocess.run(cmd,capture_output=True,timeout=120)
                        if r.returncode or not target.exists():raise ValueError('Frame extraction failed')
                        row['frames'].append({'requested_seconds':t,'path':target.relative_to(root).as_posix()})
                    row['inspection']='frames-extracted'
            elif ref['kind']=='document' and p.suffix in ('.txt','.md','.json','.yaml','.yml','.csv'):
                row.update(preview=p.read_text(encoding='utf-8',errors='replace')[:4000],inspection='text-preview')
            elif ref['kind']=='url':row.update(inspection='link-only',note='Open using the agent browser/connector; not fetched by this tool.')
            else:row.update(note='Use the source application or an appropriate parser to inspect this format; retained unchanged.')
        except (ValueError,OSError,subprocess.TimeoutExpired) as e:row['error']=str(e)
        result.append(row)
    write(root/'analysis/inspection.json',result)
    return result

def palette(path,points):
    Image,ImageOps,_,ImageStat=pillow()
    with Image.open(path) as src:im=ImageOps.exif_transpose(src).convert('RGBA')
    rows=[];roles=set()
    for pt in points:
        role=pt['role'];u,v=pt['uv']
        if role in roles or not role:raise ValueError('Roles must be nonempty and unique')
        if not all(isinstance(x,(int,float)) and math.isfinite(x) and 0<=x<=1 for x in (u,v)):raise ValueError('uv must be normalized to [0,1]')
        roles.add(role);x=round(u*(im.width-1));y=round(v*(im.height-1))
        radius=int(pt.get('radius',2))
        if not 0<=radius<=100:raise ValueError('radius must be 0..100 pixels')
        crop=im.crop((max(0,x-radius),max(0,y-radius),min(im.width,x+radius+1),min(im.height,y+radius+1)))
        pixels=[p for p in crop.getdata() if p[3]>=128]
        if not pixels:raise ValueError('Palette sample is transparent: '+role)
        import statistics
        rgb=[round(statistics.median(p[i] for p in pixels)) for i in range(3)]
        rows.append({'role':role,'hex':'#'+''.join(f'{v:02x}' for v in rgb),'uv':[u,v],
                     'sample_radius_px':radius,'source_sha256':digest(path), 'reference_id':pt.get('reference_id'),
                     'note':'Median encoded RGB; review ICC/color interpretation before locking.'})
    return rows

def compare(ref,current,out,width=960):
    Image,ImageOps,ImageDraw,_=pillow()
    if not 64<=width<=3840:raise ValueError('width must be 64..3840')
    a,b=load_rgb(ref),load_rgb(current)
    h=round(width*max(a.height/a.width,b.height/b.width));h=min(h,width*2)
    canvas=Image.new('RGB',(width*2,h+44),'#e9e6de');d=ImageDraw.Draw(canvas)
    for i,(im,label) in enumerate([(a,'REFERENCE'),(b,'IMPLEMENTATION')]):
        im=ImageOps.contain(im,(width,h));canvas.paste(im,(i*width+(width-im.width)//2,44+(h-im.height)//2));d.text((i*width+16,15),label,fill='#202b2a')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out)
    info={'reference_sha256':digest(ref),'implementation_sha256':digest(current),
          'reference_size':list(a.size),'implementation_size':list(b.size),
          'geometry':'Aspect preserved; letterboxed, not registered. Match camera and crop deliberately.',
          'verdict':'human-review-required','dimensions':['palette roles and coverage','silhouette','material','lighting','camera','UI','motion in separate recording']}
    write(out.with_suffix('.json'),info)
    return info

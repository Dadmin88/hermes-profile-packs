"""Bounded read-only study tools. Configure source checkout paths in the installation."""
import os,re
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp=FastMCP('study-sources')
PACK=Path(os.environ['STUDY_PROFILE_PACK']).resolve()
DOCS=PACK/'docs'

def profiles():
    return {p.name:p.resolve() for folder in ['hermes-academy','hermes-agency','hermes-council'] for p in (PACK/folder/'profiles').glob('*') if p.is_dir()}

def safe_read(root,path):
    dest=(root/path).resolve()
    if not dest.is_relative_to(root.resolve()) or not dest.is_file() or dest.suffix!='.md':raise ValueError('Choose a listed Markdown source file.')
    if dest.stat().st_size>80000:raise ValueError('Source too large for this tool.')
    return dest.read_text()

@mcp.tool()
def study_list_profiles() -> dict:
    """List portable source profiles available for a teaching walkthrough."""
    return {'profiles':sorted(profiles()),'source':'Profile Packs checkout; not proof these profiles are installed.'}

@mcp.tool()
def study_profile_source(profile:str,path:str='SOUL.md') -> dict:
    """Read a portable profile SOUL or owned skill; returns available files. No runtime config or credentials."""
    catalog=profiles()
    if profile not in catalog:raise ValueError('Choose a listed profile.')
    root=catalog[profile]
    available=['SOUL.md']+[str(p.relative_to(root)) for p in (root/'skills').rglob('*.md') if p.resolve().is_relative_to(root)]
    if path not in available:raise ValueError('Choose one of: '+', '.join(available[:50]))
    return {'profile':profile,'path':path,'content':safe_read(root,path),'files':available,'source_kind':'portable source, not installed runtime'}

@mcp.tool()
def study_workbench_doc(path:str='EVAL_WORKBENCH.md') -> dict:
    """Read evaluation workbench documentation from the configured source checkout."""
    allowed=['EVAL_WORKBENCH.md','EVAL_OPERATIONAL_PILOT.md','PROFILE_EVAL_DESIGN.md','CONTINUING_EDUCATION.md']
    if path not in allowed:raise ValueError('Choose one of: '+', '.join(allowed))
    return {'path':path,'content':safe_read(DOCS,path),'files':allowed}

@mcp.tool()
def study_video_transcript(video_id:str,start_seconds:int=0,duration_seconds:int=180) -> dict:
    """Get a bounded YouTube caption segment. Captions do not establish visual inspection."""
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}',video_id):raise ValueError('An 11-character YouTube video ID is required.')
    if not 0<=start_seconds<=86400 or not 1<=duration_seconds<=600:raise ValueError('Choose a start >=0 and duration 1–600 seconds.')
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript=YouTubeTranscriptApi().fetch(video_id,languages=['en'])
        rows=[{'start':s.start,'duration':s.duration,'text':s.text} for s in transcript if s.start+s.duration>=start_seconds and s.start<start_seconds+duration_seconds]
        # Keep network source content bounded before passing it to the model.
        rows=rows[:200]
        for row in rows:row['text']=row['text'][:500]
        return {'available':True,'video_id':video_id,'url':f'https://www.youtube.com/watch?v={video_id}&t={start_seconds}',
                'language':transcript.language,'generated':transcript.is_generated,'segments':rows,'visuals_inspected':False}
    except Exception as exc:
        return {'available':False,'video_id':video_id,'reason':type(exc).__name__,'message':'Transcript could not be retrieved. Ask for pasted captions; do not infer narration.'}

if __name__=='__main__':mcp.run()

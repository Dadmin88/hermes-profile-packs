#!/usr/bin/env python3
"""Discover, recommend, and install Hermes Profile Packs.

Run with no arguments in a terminal for the interactive wizard. Existing pack-first
commands remain supported. Recommendation is recipe-aware: strong, unambiguous goals
surface a validated Team Recipe first, while ambiguous goals fall back to individual
profile matching.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import recipe_catalog

ROOT = Path(__file__).resolve().parent
PACK_FILE = ROOT / "packs.json"
PACK_ALIASES = {"agency":"agency","hermes-agency":"agency","council":"council","hermes-council":"council","academy":"academy","hermes-academy":"academy"}
PACK_DISPLAY = {"agency":"Hermes Agency","council":"Hermes Council","academy":"Hermes Academy"}
PACK_HINTS = {
    "agency": {"build","work","professional","project","software","code","coding","develop","development","design","product","marketing","business","deploy","devops","engineering","test","qa","content","support"},
    "council": {"life","personal","health","fitness","parent","parenting","family","relationship","finance","budget","faith","sleep","home","career","travel","nutrition","stress","time","focus","community","recreation"},
    "academy": {"learn","study","teach","teacher","professor","course","class","education","practice","understand","school","training","lesson"},
}
QUERY_EXPANSIONS = {
    "api":{"backend","integration","web"},"web":{"frontend","backend","fullstack","full-stack"},"website":{"frontend","backend","fullstack","full-stack"},"app":{"application","frontend","backend"},"apps":{"application","frontend","backend"},"software":{"engineering","architect","developer"},"code":{"engineering","developer","programming"},"coding":{"engineering","developer","programming"},"developer":{"engineering","programming"},"security":{"cybersecurity","threat","privacy","secure"},"cyber":{"cybersecurity","security","threat"},"ai":{"mlops","machine","learning","data"},"ml":{"mlops","machine","learning","data"},"ui":{"ux","frontend","design","interface"},"ux":{"ui","design","product"},"cloud":{"systems","infrastructure","devops","reliability"},"ops":{"operations","devops","infrastructure","reliability"},"sre":{"reliability","site","infrastructure"},"game":{"godot","worldbuilder","level","game"},"games":{"godot","worldbuilder","level","game"},"money":{"finance","budget","financial"},"finances":{"finance","budget","financial"},"parent":{"parenting","family"},"kids":{"parenting","family","children"},"children":{"parenting","family"},"workout":{"fitness","movement","training"},"exercise":{"fitness","movement","training"},"food":{"nutrition","culinary","meal"},"cooking":{"culinary","food","recipe"},"stress":{"resilience","recovery","coping"},"focus":{"attention","time","planning"},"religion":{"faith","theology","religious"},"christian":{"faith","theology"},"math":{"mathematics","quantitative"},"stats":{"statistics","quantitative"},"car":{"automotive"},"cars":{"automotive"},"writing":{"writer","rhetoric","content"},"write":{"writer","rhetoric","content"},"research":{"research","evidence","methods"},"legal":{"law"},"law":{"legal"},"music":{"music"},"art":{"arts","design","creative"},
}
COORDINATION_TERMS = {"coordinate","coordination","orchestrate","orchestrator","steward","dean","team","overview","general","everything","whole","manage","management"}
TOKEN_RE = re.compile(r"[a-z0-9]+")

class CLIError(ValueError): pass

@dataclass(frozen=True)
class PackInfo:
    key:str; name:str; path:Path; namespace:str; manifest_path:Path; purpose:str; version:str; orchestrator:str|None; backbone:frozenset[str]; categories:tuple[str,...]; profile_names:tuple[str,...]

@dataclass(frozen=True)
class Profile:
    pack:str; pack_name:str; name:str; display_name:str; category:str; description:str; role:str; jobs:tuple[str,...]; orchestrator:bool; backbone:bool; source_bytes:int
    def searchable_text(self)->str: return " ".join([self.name.replace("-"," "),self.display_name,self.category,self.description,self.role,*self.jobs]).lower()
    def as_dict(self)->dict: return {"pack":self.pack,"pack_name":self.pack_name,"name":self.name,"display_name":self.display_name,"category":self.category,"description":self.description,"role":self.role,"jobs":list(self.jobs),"orchestrator":self.orchestrator,"backbone":self.backbone,"estimated_source_bytes":self.source_bytes}

def normalize_pack(value:str)->str:
    try: return PACK_ALIASES[value.strip().lower()]
    except KeyError as exc: raise CLIError(f"unknown pack: {value}") from exc

def short_pack_name(name:str)->str:
    return normalize_pack(name[len("hermes-"):] if name.startswith("hermes-") else name)

def _yaml_scalar(path:Path,key:str)->str:
    if not path.is_file(): return ""
    prefix=f"{key}:"
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if line.startswith(prefix):
            value=line.split(":",1)[1].strip()
            if len(value)>=2 and value[0]==value[-1] and value[0] in {'"',"'"}: value=value[1:-1]
            return value.replace(r'\"','"')
    return ""

def directory_size(path:Path)->int:
    total=0
    if not path.is_dir(): return 0
    for child in path.rglob("*"):
        try:
            if child.is_file(): total+=child.stat().st_size
        except OSError: continue
    return total

def derived_capabilities(source:Path)->tuple[str,...]:
    skills=source/"skills"
    if not skills.is_dir(): return ()
    return tuple(sorted(
        skill.parent.name
        for skill in skills.glob("*/SKILL.md")
        if skill.parent.name != "academy-continuing-education"
    ))

def load_catalog(root:Path=ROOT)->tuple[dict[str,PackInfo],list[Profile]]:
    pack_file=root/"packs.json"
    if not pack_file.is_file(): raise CLIError(f"missing pack registry: {pack_file}")
    registry=json.loads(pack_file.read_text(encoding="utf-8")); packs={}; profiles=[]
    for record in registry.get("packs",[]):
        key=short_pack_name(record["name"]); pack_dir=root/record["path"]; manifest_path=root/record["manifest"]
        if not manifest_path.is_file(): raise CLIError(f"missing pack manifest: {record['manifest']}")
        manifest=json.loads(manifest_path.read_text(encoding="utf-8")); rows=manifest.get("profiles",[]); backbone=frozenset(manifest.get("backbone_profiles",[])); orchestrator=manifest.get("orchestrator")
        packs[key]=PackInfo(key,record["name"],pack_dir,record["namespace"],manifest_path,record.get("purpose",manifest.get("description","")),str(manifest.get("version","")),orchestrator,backbone,tuple(sorted({str(i.get("category","other")) for i in rows})),tuple(str(i["name"]) for i in rows))
        for item in rows:
            name=str(item["name"]); source=pack_dir/"profiles"/name; desc=str(item.get("description") or _yaml_scalar(source/"distribution.yaml","description"))
            jobs=tuple(sorted({*(str(j) for j in item.get("jobs",[])),*derived_capabilities(source)}))
            profiles.append(Profile(key,record["name"],name,str(item.get("display_name") or name),str(item.get("category") or "other"),desc,str(item.get("role") or ""),jobs,name==orchestrator,name in backbone,directory_size(source)))
    return packs,profiles

def load_recipe_catalog(root:Path=ROOT):
    try: return recipe_catalog.load_recipes(root)
    except recipe_catalog.RecipeError as exc: raise CLIError(str(exc)) from exc

def tokenize(text:str)->set[str]: return set(TOKEN_RE.findall(text.lower()))
def expanded_query(text:str)->set[str]:
    tokens=tokenize(text); out=set(tokens)
    for token in tokens: out.update(QUERY_EXPANSIONS.get(token,set()))
    return out

def _profile_score(profile:Profile,query:str,query_tokens:set[str]):
    name_hits=sorted(query_tokens & tokenize(profile.name.replace("-"," ")+" "+profile.display_name)); cat_hits=sorted(query_tokens & tokenize(profile.category)); job_hits=sorted(query_tokens & tokenize(" ".join(profile.jobs))); detail_hits=sorted(query_tokens & tokenize(profile.description+" "+profile.role)); score=len(name_hits)*8+len(cat_hits)*5+len(job_hits)*5+len(detail_hits)*3; reasons=[]
    if name_hits: reasons.append("profile: "+", ".join(name_hits[:3]))
    if cat_hits: reasons.append("category: "+", ".join(cat_hits[:2]))
    if job_hits: reasons.append("capability: "+", ".join(job_hits[:3]))
    if detail_hits: reasons.append("description: "+", ".join(detail_hits[:3]))
    raw=" ".join(query.lower().split())
    if raw and len(raw)>=4 and raw in profile.searchable_text(): score+=14; reasons.insert(0,"exact phrase match")
    pack_hits=sorted(tokenize(query)&PACK_HINTS.get(profile.pack,set()))
    if pack_hits: score+=min(8,2*len(pack_hits)); reasons.append(f"{PACK_DISPLAY[profile.pack]} intent")
    if profile.orchestrator: score += 9 if tokenize(query)&COORDINATION_TERMS else -4
    if profile.backbone and not profile.orchestrator: score+=1
    return score,reasons

def recommend_profiles(profiles:Iterable[Profile],query:str,*,limit:int=6,pack_filter:set[str]|None=None):
    if not query.strip(): raise CLIError("recommendation query cannot be empty")
    if limit<1: raise CLIError("--limit must be at least 1")
    q=expanded_query(query); ranked=[]
    for p in profiles:
        if pack_filter and p.pack not in pack_filter: continue
        score,reasons=_profile_score(p,query,q)
        if score>0: ranked.append((p,score,reasons))
    ranked.sort(key=lambda i:(-i[1],i[0].orchestrator,i[0].pack,i[0].category,i[0].name)); return ranked[:limit]

def recommend_recipes(recipes,query,*,limit=5,pack_filter=None):
    try: return recipe_catalog.recommend_recipes(recipes,query,expanded_query=expanded_query,tokenize=tokenize,pack_hints=PACK_HINTS,pack_display=PACK_DISPLAY,limit=limit,pack_filter=pack_filter)
    except recipe_catalog.RecipeError as exc: raise CLIError(str(exc)) from exc

def recommend_goal(profiles,recipes,query,*,limit=6,pack_filter=None):
    display_recipe_limit=min(5,max(1,limit))
    ranked_recipes=recommend_recipes(recipes.values(),query,limit=max(2,display_recipe_limit),pack_filter=pack_filter)
    displayed_recipes=ranked_recipes[:display_recipe_limit]
    profile_matches=recommend_profiles(profiles,query,limit=limit,pack_filter=pack_filter)
    confident_recipe=recipe_catalog.confident_recipe_match(ranked_recipes)
    if confident_recipe and profile_matches and profile_matches[0][1]>=confident_recipe[1]:
        confident_recipe=None
    return displayed_recipes,confident_recipe,profile_matches

def format_bytes(value:int)->str:
    amount=float(value); unit="B"
    for unit in ["B","KiB","MiB","GiB"]:
        if amount<1024 or unit=="GiB": break
        amount/=1024
    return f"{int(amount)} {unit}" if unit=="B" else f"{amount:.1f} {unit}"

def selected_stats(selected,all_profiles):
    s=list(selected); a=list(all_profiles); sb=sum(p.source_bytes for p in s); tb=sum(p.source_bytes for p in a); by={}
    for p in s: by[p.pack]=by.get(p.pack,0)+1
    return {"selected_profiles":len(s),"available_profiles":len(a),"skipped_profiles":max(0,len(a)-len(s)),"estimated_source_bytes":sb,"estimated_source_bytes_skipped":max(0,tb-sb),"by_pack":by}

def filter_packs(values): return None if not values else {normalize_pack(v) for v in values}

def resolve_selection(profiles,*,explicit_names,category_specs,select_all,pack_filter):
    by_name={p.name:p for p in profiles}; chosen={}
    if select_all:
        for p in profiles:
            if not pack_filter or p.pack in pack_filter: chosen[p.name]=p
    for name in explicit_names or []:
        for part in name.split(","):
            item=part.strip()
            if not item: continue
            p=by_name.get(item)
            if not p: raise CLIError(f"unknown profile: {item}")
            if pack_filter and p.pack not in pack_filter: raise CLIError(f"profile {item} is outside the requested --pack filter")
            chosen[item]=p
    for spec in category_specs or []:
        if ":" not in spec: raise CLIError("categories must use PACK:CATEGORY, for example agency:engineering")
        pv,cat=spec.split(":",1); pack=normalize_pack(pv)
        if pack_filter and pack not in pack_filter: raise CLIError(f"category {spec} is outside the requested --pack filter")
        matches=[p for p in profiles if p.pack==pack and p.category==cat]
        if not matches: raise CLIError(f"unknown category '{cat}' for {pack}. Available: {', '.join(sorted({p.category for p in profiles if p.pack==pack}))}")
        for p in matches: chosen[p.name]=p
    return sorted(chosen.values(),key=lambda p:(p.pack,p.name))

def resolve_recipe_selection(recipe,tier,profiles,*,pack_filter=None):
    if pack_filter and recipe.pack not in pack_filter: raise CLIError(f"recipe {recipe.id} is outside the requested --pack filter")
    try: return recipe_catalog.resolve_recipe_profiles(recipe,tier,profiles)
    except recipe_catalog.RecipeError as exc: raise CLIError(str(exc)) from exc

def pack_installer(pack):
    path=pack.path/"install.py"
    if not path.is_file(): raise CLIError(f"missing installer for {pack.name}: {path}")
    return path

def install_selected(selected,packs,*,force,json_mode):
    grouped={}
    for p in selected: grouped.setdefault(p.pack,[]).append(p)
    results=[]
    for key in ("agency","council","academy"):
        members=grouped.get(key)
        if not members: continue
        cmd=[sys.executable,str(pack_installer(packs[key])),*[p.name for p in members]]
        if force: cmd.append("--force")
        if not json_mode: print(f"\n==> {PACK_DISPLAY[key]}: {len(members)} profile(s)")
        c=subprocess.run(cmd,text=True,capture_output=json_mode,check=False); result={"pack":key,"profiles":[p.name for p in members],"returncode":c.returncode}
        if json_mode: result.update(stdout=c.stdout,stderr=c.stderr)
        results.append(result)
        if c.returncode: return c.returncode,results
    return 0,results

def print_pack_list(packs,profiles):
    counts={k:0 for k in packs}
    for p in profiles: counts[p.pack]=counts.get(p.pack,0)+1
    for k in ("agency","council","academy"):
        if k in packs: print(f"{k:<8} {packs[k].namespace:<11} {counts[k]:>3} profiles  {packs[k].purpose}")
def print_catalog(profiles):
    cur=None
    for p in sorted(profiles,key=lambda x:(x.pack,x.category,x.name)):
        marker=(p.pack,p.category)
        if marker!=cur: print(f"\n{PACK_DISPLAY[p.pack]} / {p.category}"); cur=marker
        print(f"  {p.name:<42} {p.display_name}")
def print_recipe_list(recipes,*,profiles=None):
    cur=None
    for r in sorted(recipes,key=lambda x:(x.pack,x.id)):
        if r.pack!=cur: print(f"\n{PACK_DISPLAY[r.pack]}"); cur=r.pack
        counts="/".join(str(len(r.tiers[t])) for t in recipe_catalog.TIER_ORDER); print(f"  {r.id:<28} {r.display_name}  [{counts} profiles]\n    {r.description}")
def _prompt(prompt):
    try: return input(prompt).strip()
    except (EOFError,KeyboardInterrupt) as exc: print(); raise CLIError("selection cancelled") from exc

def _parse_indices(value,count,*,blank_means_all=False):
    value=value.strip().lower()
    if not value: return list(range(count)) if blank_means_all else []
    if value in {"all","a"}: return list(range(count))
    if value in {"none","n"}: return []
    picked=set()
    for chunk in value.split(","):
        chunk=chunk.strip()
        if not chunk: continue
        if "-" in chunk:
            l,r=chunk.split("-",1)
            try: start,end=int(l),int(r)
            except ValueError as exc: raise CLIError(f"invalid selection: {chunk}") from exc
            if start>end: start,end=end,start
            nums=range(start,end+1)
        else:
            try: nums=[int(chunk)]
            except ValueError as exc: raise CLIError(f"invalid selection: {chunk}") from exc
        for n in nums:
            if n<1 or n>count: raise CLIError(f"selection {n} is outside 1-{count}")
            picked.add(n-1)
    return sorted(picked)
def _choose_profiles(items,*,blank_means_all=False):
    for i,p in enumerate(items,1):
        d=p.description or p.role; d=d if len(d)<=96 else d[:93].rstrip()+"..."; print(f"  {i:>2}. {p.display_name}  [{p.name}]"); print(f"      {d}") if d else None
    suffix=" [Enter = all]" if blank_means_all else ""
    while True:
        try: return [items[i] for i in _parse_indices(_prompt(f"Select numbers (for example 1,3-5 or all){suffix}: "),len(items),blank_means_all=blank_means_all)]
        except CLIError as exc: print(f"  {exc}")
def _choose_recipe_tier(recipe,profiles):
    labels={"minimal":"smallest coherent formation","recommended":"default balance of expertise and review","expanded":"broader coverage for larger or higher-risk work"}; print(f"\n{recipe.display_name} tiers:")
    for i,t in enumerate(recipe_catalog.TIER_ORDER,1): print(f"  {i}. {t:<11} {len(recipe.tiers[t]):>2} profiles - {labels[t]}")
    while True:
        value=_prompt("Choose tier 1-3 [2]: ") or "2"
        try: idx=_parse_indices(value,3)
        except CLIError as exc: print(f"  {exc}"); continue
        if len(idx)!=1: print("  Choose exactly one tier."); continue
        tier=recipe_catalog.TIER_ORDER[idx[0]]; selected=resolve_recipe_selection(recipe,tier,profiles); print(f"\n{tier.title()} recipe plan:")
        for p in selected: print(f"  - {p.display_name} ({p.name})")
        return tier,selected
def wizard_recommend(profiles,recipes):
    print("\nTell me what you want Hermes to help with.\nExamples: 'build a web app', 'get my finances organized', 'learn cybersecurity'.")
    while True:
        query=_prompt("What do you need? ")
        try: _,confident,ranked=recommend_goal(profiles,recipes,query,limit=6)
        except CLIError as exc: print(f"  {exc}"); continue
        if confident:
            r,score,reasons=confident; print(f"\nThis maps cleanly to a validated Team Recipe:\n  {r.display_name} [{r.id}]\n  {r.description}\n  Match: {'; '.join(reasons[:2]) or r.description} · score {score}")
            if _prompt("Use this team recipe? [Y/n]: ").lower() not in {"n","no"}: return _choose_recipe_tier(r,profiles)[1]
            print("\nOkay - showing individual profile matches instead.")
        if not ranked: print("I couldn't find a confident match. Try a few more concrete words, or browse instead."); continue
        print("\nSmallest useful individual matches I found:")
        for i,(p,score,reasons) in enumerate(ranked,1): print(f"  {i}. {p.display_name} ({PACK_DISPLAY[p.pack]})\n     {p.name} · {'; '.join(reasons[:2]) or 'catalog match'} · score {score}")
        chosen=_choose_profiles([i[0] for i in ranked],blank_means_all=True)
        return chosen if chosen else []
def wizard_browse_recipes(recipes,profiles):
    ordered=sorted(recipes.values(),key=lambda r:(r.pack,r.id)); print("\nTeam Recipes:")
    for i,r in enumerate(ordered,1): print(f"  {i:>2}. {r.display_name} ({PACK_DISPLAY[r.pack]})\n      {r.id} - {r.description}")
    while True:
        try: idx=_parse_indices(_prompt("Recipe number: "),len(ordered))
        except CLIError as exc: print(f"  {exc}"); continue
        if len(idx)!=1: print("  Choose exactly one recipe."); continue
        return _choose_recipe_tier(ordered[idx[0]],profiles)[1]
def wizard_browse(packs,profiles):
    keys=[k for k in ("agency","council","academy") if k in packs]; print("\nChoose a pack:")
    for i,k in enumerate(keys,1): print(f"  {i}. {PACK_DISPLAY[k]} ({sum(1 for p in profiles if p.pack==k)} profiles) - {packs[k].purpose}")
    while True:
        try: idx=_parse_indices(_prompt("Pack number: "),len(keys))
        except CLIError as exc: print(f"  {exc}"); continue
        if len(idx)==1: pack=keys[idx[0]]; break
        print("  Choose exactly one pack.")
    cats=list(packs[pack].categories); print(f"\n{PACK_DISPLAY[pack]} categories:")
    for i,c in enumerate(cats,1): print(f"  {i}. {c} ({sum(1 for p in profiles if p.pack==pack and p.category==c)})")
    print("  all. Show the whole pack")
    while True:
        v=_prompt("Category number or all: ").lower()
        if v in {"all","a"}: candidates=[p for p in profiles if p.pack==pack]; break
        try: idx=_parse_indices(v,len(cats))
        except CLIError as exc: print(f"  {exc}"); continue
        if len(idx)!=1: print("  Choose exactly one category."); continue
        candidates=[p for p in profiles if p.pack==pack and p.category==cats[idx[0]]]; break
    return _choose_profiles(sorted(candidates,key=lambda p:p.name))
def wizard_direct(profiles):
    ranked=recommend_profiles(profiles,_prompt("\nSearch profile names/descriptions: "),limit=20)
    return _choose_profiles([i[0] for i in ranked]) if ranked else []
def run_wizard(packs,profiles,recipes,*,force):
    if not (sys.stdin.isatty() and sys.stdout.isatty()): raise CLIError("the interactive wizard requires a terminal; agents should use --agent-help")
    print(f"\nHermes Profile Packs 🪽\nPick only what helps. You can always add more later.\nCatalog: {len(profiles)} profiles, {len(recipes)} team recipes, {len(packs)} packs.\n\n  1. Recommend a small team for me\n  2. Browse team recipes\n  3. Browse packs and categories\n  4. Search profiles directly\n  5. Install everything\n  6. Exit")
    while True:
        choice=_prompt("Choose 1-6 [1]: ") or "1"
        if choice=="1": selected=wizard_recommend(profiles,recipes)
        elif choice=="2": selected=wizard_browse_recipes(recipes,profiles)
        elif choice=="3": selected=wizard_browse(packs,profiles)
        elif choice=="4": selected=wizard_direct(profiles)
        elif choice=="5": selected=list(profiles)
        elif choice=="6": print("Nothing installed."); return 0
        else: print("Choose 1, 2, 3, 4, 5, or 6."); continue
        if selected: break
    stats=selected_stats(selected,profiles); print("\nInstall plan")
    for pack in ("agency","council","academy"):
        members=[p for p in selected if p.pack==pack]
        if members:
            print(f"  {PACK_DISPLAY[pack]}: {len(members)}")
            for p in members: print(f"    - {p.display_name} ({p.name})")
    print(f"\nSelected {stats['selected_profiles']} of {stats['available_profiles']} profiles (~{format_bytes(stats['estimated_source_bytes'])} source payload).")
    if stats['skipped_profiles']: print(f"Skipping {stats['skipped_profiles']} profiles (~{format_bytes(stats['estimated_source_bytes_skipped'])} of catalog payload).")
    if _prompt("Install this selection? [y/N]: ").lower() not in {"y","yes"}: print("Nothing installed."); return 0
    return install_selected(selected,packs,force=force,json_mode=False)[0]
def legacy_delegate(argv):
    if not argv or argv[0].startswith("-"): return None
    try: key=normalize_pack(argv[0])
    except CLIError: return None
    reg=json.loads(PACK_FILE.read_text(encoding="utf-8")); rec=next((i for i in reg.get("packs",[]) if short_pack_name(i["name"])==key),None)
    if not rec: raise CLIError(f"pack is registered but unavailable: {key}")
    return subprocess.run([sys.executable,str(ROOT/rec["path"]/"install.py"),*argv[1:]],check=False).returncode
def build_parser():
    p=argparse.ArgumentParser(description="Choose only the Hermes profiles or validated team recipe you need.",epilog="Legacy pack commands still work: python install.py council --list. Run with no arguments in a terminal to launch the wizard.")
    p.add_argument("--wizard",action="store_true"); p.add_argument("--list-packs",action="store_true"); p.add_argument("--catalog",action="store_true"); p.add_argument("--list-recipes",action="store_true"); p.add_argument("--recommend",metavar="TEXT"); p.add_argument("--agent-help",action="store_true"); p.add_argument("--pack",action="append"); p.add_argument("--recipe"); p.add_argument("--tier",choices=recipe_catalog.TIER_ORDER); p.add_argument("--profiles",nargs="+"); p.add_argument("--category",action="append",metavar="PACK:CATEGORY"); p.add_argument("--all",action="store_true"); p.add_argument("--limit",type=int,default=6); p.add_argument("--dry-run",action="store_true"); p.add_argument("--force",action="store_true"); p.add_argument("--yes",action="store_true"); p.add_argument("--json",action="store_true"); return p
def agent_help_payload(): return {"interactive":"python install.py","catalog":"python install.py --catalog --json","recipes":"python install.py --list-recipes --json","recommend":"python install.py --recommend 'build a web app' --json","recipe_dry_run":"python install.py --recipe software-delivery --tier minimal --dry-run --json","install_recipe":"python install.py --recipe software-delivery --tier recommended --yes --json","dry_run":"python install.py --profiles agency-backend-engineer agency-frontend-engineer --dry-run --json","install_profiles":"python install.py --profiles agency-backend-engineer agency-frontend-engineer --yes --json","install_category":"python install.py --category council:growth --yes --json","install_everything":"python install.py --all --yes --json","rules":["--catalog, --list-recipes, and --recommend are read-only","--recommend preserves individual profile results and adds a recipe_match only when confidence is high","--json never prompts","writes require --yes unless using the interactive wizard","use --dry-run to inspect an exact profile or recipe plan","legacy pack-first commands remain supported"]}
def emit_json(payload): print(json.dumps(payload,indent=2,sort_keys=True))
def _recipe_summary(ranked,confident):
    match=None
    if confident:
        r,score,reasons=confident; match={"recipe":r.id,"display_name":r.display_name,"pack":r.pack,"score":score,"reasons":reasons,"default_tier":recipe_catalog.DEFAULT_TIER,"profiles":list(r.tiers[recipe_catalog.DEFAULT_TIER])}
    return match,[{"recipe":r.id,"display_name":r.display_name,"pack":r.pack,"score":score,"reasons":reasons,"recommended_profiles":list(r.tiers[recipe_catalog.DEFAULT_TIER])} for r,score,reasons in ranked]
def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv); legacy=legacy_delegate(argv)
    if legacy is not None: return legacy
    args=build_parser().parse_args(argv)
    try:
        packs,profiles=load_catalog(); recipes=load_recipe_catalog(); pf=filter_packs(args.pack)
        if not argv: return run_wizard(packs,profiles,recipes,force=False)
        if args.wizard:
            if args.json: raise CLIError("--wizard cannot be combined with --json")
            return run_wizard(packs,profiles,recipes,force=args.force)
        read_modes=sum(bool(v) for v in [args.list_packs,args.catalog,args.list_recipes,args.recommend,args.agent_help])
        if read_modes>1: raise CLIError("choose only one of --list-packs, --catalog, --list-recipes, --recommend, or --agent-help")
        if read_modes and (args.recipe or args.profiles or args.category or args.all or args.dry_run or args.yes): raise CLIError("read-only discovery modes cannot be combined with install-selection flags")
        if args.recipe and (args.profiles or args.category or args.all): raise CLIError("--recipe cannot be combined with --profiles, --category, or --all")
        if args.tier and not args.recipe: raise CLIError("--tier requires --recipe")
        fprofiles=[p for p in profiles if not pf or p.pack in pf]; frecipes=[r for r in recipes.values() if not pf or r.pack in pf]
        if args.agent_help:
            payload=agent_help_payload()
            if args.json: emit_json(payload)
            else:
                print("Agent/script usage (non-interactive):")
                for k,v in payload.items():
                    if k=="rules":
                        print("\nRules:")
                        for rule in v: print(f"  - {rule}")
                    else: print(f"  {k:<18} {v}")
            return 0
        if args.list_packs:
            if args.json: emit_json({"packs":[{"key":k,"name":packs[k].name,"namespace":packs[k].namespace,"purpose":packs[k].purpose,"profile_count":sum(1 for p in profiles if p.pack==k),"version":packs[k].version} for k in ("agency","council","academy") if k in packs and (not pf or k in pf)]})
            else: print_pack_list({k:v for k,v in packs.items() if not pf or k in pf},fprofiles)
            return 0
        if args.catalog:
            emit_json({"profile_count":len(fprofiles),"profiles":[p.as_dict() for p in fprofiles]}) if args.json else print_catalog(fprofiles); return 0
        if args.list_recipes:
            ordered=sorted(frecipes,key=lambda r:(r.pack,r.id)); emit_json({"recipe_count":len(ordered),"recipes":[r.as_dict() for r in ordered]}) if args.json else print_recipe_list(ordered,profiles=profiles); return 0
        if args.recommend is not None:
            rr,confident,ranked=recommend_goal(profiles,recipes,args.recommend,limit=args.limit,pack_filter=pf); match,rrecs=_recipe_summary(rr,confident)
            if args.json: emit_json({"query":args.recommend,"limit":args.limit,"recipe_match":match,"recipe_recommendations":rrecs,"recommendation_count":len(ranked),"recommendations":[{**p.as_dict(),"score":score,"reasons":reasons} for p,score,reasons in ranked]})
            else:
                print(f"Recommended for: {args.recommend}")
                if confident:
                    r,score,reasons=confident; print(f"\nClear Team Recipe match:\n  {r.id:<28} {r.display_name}  score={score}\n    {'; '.join(reasons[:3]) or r.description}\n    default tier: {recipe_catalog.DEFAULT_TIER} ({len(r.tiers[recipe_catalog.DEFAULT_TIER])} profiles)")
                elif rr: print("\nNo single Team Recipe is unambiguous enough to promote.")
                if ranked:
                    print("\nIndividual profile matches:")
                    for p,score,reasons in ranked: print(f"  {p.name:<42} {p.display_name}  score={score}\n    {'; '.join(reasons[:3]) or 'catalog match'}")
                elif not rr: print("No confident recommendations found.")
            return 0
        context=None
        if args.recipe:
            r=recipes.get(args.recipe)
            if r is None: raise CLIError(f"unknown recipe: {args.recipe}")
            tier=args.tier or recipe_catalog.DEFAULT_TIER; selected=resolve_recipe_selection(r,tier,profiles,pack_filter=pf); context={"recipe":r.id,"display_name":r.display_name,"pack":r.pack,"tier":tier,"workflow":list(r.workflow),"success_criteria":list(r.success_criteria),"optional_routines":list(r.optional_routines)}
        else: selected=resolve_selection(profiles,explicit_names=args.profiles,category_specs=args.category,select_all=args.all,pack_filter=pf)
        if not selected: raise CLIError("no profiles selected. Use the wizard, --recipe, --profiles, --category, --all, --catalog, --list-recipes, or --recommend.")
        stats=selected_stats(selected,profiles); plan={"status":"plan","profiles":[p.name for p in selected],"stats":stats}; plan.update(context or {})
        if args.dry_run:
            if args.json: emit_json(plan)
            else:
                print(f"Would install recipe {context['recipe']} ({context['tier']}) with {stats['selected_profiles']} profile(s):" if context else f"Would install {stats['selected_profiles']} profile(s):")
                for p in selected: print(f"  - {p.name}")
                print(f"Estimated source payload: {format_bytes(stats['estimated_source_bytes'])}; skipping {stats['skipped_profiles']} profile(s).")
            return 0
        if not args.yes:
            if args.json or not (sys.stdin.isatty() and sys.stdout.isatty()): raise CLIError("installation requires --yes in non-interactive mode; use --dry-run first if desired")
            if _prompt(f"Install {len(selected)} selected profile(s)?\nContinue? [y/N]: ").lower() not in {"y","yes"}: print("Nothing installed."); return 0
        code,results=install_selected(selected,packs,force=args.force,json_mode=args.json)
        if args.json: emit_json({**plan,"status":"ok" if code==0 else "error","returncode":code,"packs":results})
        elif code==0: print(f"\nInstalled {len(selected)} profile(s) from recipe {context['recipe']} ({context['tier']})." if context else f"\nInstalled {len(selected)} selected Hermes profile(s).")
        return code
    except (CLIError,recipe_catalog.RecipeError,json.JSONDecodeError,OSError) as exc:
        if 'args' in locals() and getattr(args,'json',False): print(json.dumps({"status":"error","error":str(exc)}),file=sys.stderr)
        else: print(f"error: {exc}",file=sys.stderr)
        return 2
if __name__=="__main__": raise SystemExit(main())

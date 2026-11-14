"""Print timestamped caption excerpts without YouTube's rolling repetitions."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for vid in sys.argv[1:]:
    metadata=json.loads((ROOT/'videos'/f'{vid}.info.json').read_text(encoding='utf-8'))
    print('\nVIDEO',vid,metadata['title'],'DURATION',metadata['duration'])
    caption=ROOT/'videos'/f'{vid}.en-orig.vtt'
    if not caption.exists():
        print('CAPTIONS NOT AVAILABLE YET')
        continue
    rows,seen=[],set()
    for block in re.split(r'\n\s*\n',caption.read_text(encoding='utf-8-sig')):
        lines=block.splitlines()
        stamp=next((line.split(' --> ')[0] for line in lines if ' --> ' in line),None)
        if not stamp: continue
        contents=[html.unescape(re.sub('<[^>]+>','',line)).strip() for line in lines if line and '-->' not in line and not line.isdigit()]
        fresh=[line for line in contents if line not in seen]
        seen.update(contents)
        if fresh: rows.append((stamp,' '.join(fresh)))
    (ROOT/'research'/f'{vid}.transcript.txt').write_text('\n'.join(t+' '+v for t,v in rows),encoding='utf-8')
    for i in range(0,len(rows),9):
        print(rows[i][0], ' '.join(v for _,v in rows[i:i+9]))

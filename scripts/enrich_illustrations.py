"""Materializa somente figuras com seleção editorial explícita e proveniência registrada."""
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request,urlopen
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    inventory=json.loads((ROOT/'research/documentation-inventory.json').read_text(encoding='utf-8'))
    sources={p['url']:json.loads((ROOT/p['cacheFile']).read_text(encoding='utf-8')) for p in inventory['pages']}
    baseline=json.loads((ROOT/'research/enrichment-baseline.json').read_text(encoding='utf-8'))
    lessons={l['slug']:l for l in baseline['lessons']}
    selection=json.loads((ROOT/'research/illustration-selection.json').read_text(encoding='utf-8'))
    target=ROOT/'site/assets/supplements';target.mkdir(exist_ok=True)
    rows=[]
    for approved in selection['figures']:
        row=dict(approved)
        assert row.get('reviewReason') and row.get('caption'), 'Seleção sem justificativa ou legenda'
        if row['kind']=='documentation':
            doc=sources[row['source']];picture=doc['images'][row['sourceImageIndex']]
            row['imageSource']=picture['url']
            key=hashlib.sha256(picture['url'].encode()).hexdigest()[:16]
            row['path']='assets/supplements/'+key+'.png'
        elif row['kind']=='frame':
            video=lessons[row['lesson']]['video'];timestamp=row['time']
            row['path']=f'assets/supplements/{video}-{timestamp}-audit.jpg'
            row['source']=f'https://www.youtube.com/watch?v={video}&t={timestamp}s'
        else:raise ValueError('Tipo não revisado: '+row['kind'])
        rows.append(row)

    def download(row):
        dest=ROOT/'site'/row['path']
        candidates=[row['imageSource']]
        if '%3F' in row['imageSource']:candidates.append(row['imageSource'].split('%3F')[0])
        if dest.exists() and len(candidates)>1:row['resolvedImageSource']=candidates[-1]
        if not dest.exists():
            for url in candidates:
                try:
                    data=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
                    dest.write_bytes(data);row['resolvedImageSource']=url;break
                except Exception:
                    if url==candidates[-1]:raise
        with Image.open(dest) as im:row['width'],row['height']=im.size
        return row

    unique={row['path']:row for row in rows if row['kind']=='documentation'}
    with ThreadPoolExecutor(max_workers=4) as pool:loaded={row['path']:row for row in pool.map(download,unique.values())}
    for row in rows:
        dest=ROOT/'site'/row['path']
        if row['kind']=='documentation':
            file=loaded[row['path']]
            row.update(width=file['width'],height=file['height'],resolvedImageSource=file.get('resolvedImageSource',row['imageSource']))
        else:
            if not dest.exists():
                video=lessons[row['lesson']]['video']
                subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(row['time']),'-i',str(ROOT/'videos'/(video+'.mp4')),'-frames:v','1','-q:v','3','-y',str(dest)],check=True)
            with Image.open(dest) as im:row['width'],row['height']=im.size
        if row['lesson']=='@introducao':row.update(module=1,lessonTitle='Introdução e arquitetura',stepTitle='Protocolos e implantação')
        else:
            l=lessons[row['lesson']];row.update(module=l['module'],lessonTitle=l['title'],stepTitle=l['steps'][row['step']-1]['title'])
    (ROOT/'research/illustration-additions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'site/illustrations.js').write_text('/* Figuras com revisão explícita de pertinência por passo. */\n(()=>{const rows='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';window.LEAP.illustrationAdditions=rows;rows.forEach(row=>{if(row.lesson==="@introducao"){(window.LEAP.introFigures??=[]).push(row);return;}const lesson=window.LEAP.lessons.find(l=>l.slug===row.lesson);if(!lesson)throw Error(row.lesson);const step=lesson.steps[row.step-1];(step.additionalFigures??=[]).push(row);});})();\n',encoding='utf-8')
    used={row['path'] for row in rows}
    for file in target.iterdir():
        if file.is_file() and file.resolve().parent==target.resolve() and 'assets/supplements/'+file.name not in used:file.unlink()
    print(json.dumps({'figures':len(rows),'uniqueAssets':len({r['path'] for r in rows}),'steps':len({(r['lesson'],r['step']) for r in rows}),'lessons':len({r['lesson'] for r in rows})}),flush=True)


if __name__=='__main__':main()

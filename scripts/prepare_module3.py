"""Cache the module's official block references and original documentation images."""
import json
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
from collect_docs import collect

ROOT=Path(__file__).resolve().parents[1]
PATHS=[
 'data-driven/read-excel','data-driven/write-excel','data-driven/database','data-driven/http-request',
 'data-driven/compress-file','data-driven/save-file','data-driven/set-file','data-driven/command-line','data-driven/send-e-mail',
 'logic/compare','logic/switch','logic/loop','logic/break-iteration','logic/calculate','logic/change-text',
 'logic/regular-expression','logic/offset-date-time','logic/offset-area','logic/offset-position',
 'logic/get-clipboard','logic/set-clipboard','logic/close-windows','logic/wait','logic/c-sharp-code',
 'variables/set-variable','variables/get-variable','generators/generate-number','generators/generate-password','generators/generate-date-time']
out=ROOT/'site/assets/docs';out.mkdir(parents=True,exist_ok=True)
def prepare(path):
    doc=collect('building-blocks/'+path)
    record={'path':'building-blocks/'+path,'url':doc['url'],'title':doc['title']}
    if doc['images']:
        source=doc['images'][0]['url'];name='m3-'+path.split('/')[-1]+'.png';dest=out/name
        if not dest.exists():
            with urlopen(Request(source,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:dest.write_bytes(response.read())
        with Image.open(dest) as image:record['size']=image.size
        record.update(image='assets/docs/'+name,imageSource=source)
    return record
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(prepare,PATHS))
(ROOT/'research/module3-documents.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for batch in range(0,len(records),8):
    subset=records[batch:batch+8];sheet=Image.new('RGB',(1280,360*((len(subset)+3)//4)),'#10152c');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(subset):
        x=i%4*320;y=i//4*360;draw.text((x+8,y+8),r['path'].split('/')[-1],fill='white')
        if 'image' in r:
            with Image.open(ROOT/'site'/r['image']) as image:
                thumb=image.convert('RGB');thumb.thumbnail((304,320));sheet.paste(thumb,(x+8,y+34))
    sheet.save(ROOT/'research/contact-sheets'/f'module3-docs-{batch//8+1}.jpg',quality=90)
print(json.dumps({'docs':len(records),'images':sum('image' in r for r in records)}))

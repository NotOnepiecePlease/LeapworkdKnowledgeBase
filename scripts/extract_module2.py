"""Extract planned teaching frames and contact sheets for the completed collection."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
shots=json.loads((ROOT/'research/module2-shots.json').read_text(encoding='utf-8'))
for vid,times in shots.items():
    if not (ROOT/'videos'/f'{vid}.mp4').exists():continue
    sheet=Image.new('RGB',(1280,390*((len(times)+1)//2)),'#10152c')
    draw=ImageDraw.Draw(sheet)
    for i,sec in enumerate(times):
        target=ROOT/'site/assets/frames'/f'{vid}-{sec}.jpg'
        if not target.exists():
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(sec),'-i',str(ROOT/'videos'/f'{vid}.mp4'),'-frames:v','1','-q:v','2',str(target)],check=True)
        with Image.open(target) as frame:
            frame.thumbnail((640,360));x=i%2*640;y=i//2*390
            sheet.paste(frame,(x,y+30));draw.text((x+12,y+8),f'{vid} | {sec//60:02}:{sec%60:02}',fill='white')
    sheet.save(ROOT/'research/contact-sheets'/f'{vid}.jpg',quality=90)
    print('EXTRACTED',vid,flush=True)

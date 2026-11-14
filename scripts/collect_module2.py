"""Fetch the remaining official Testing the Internet videos and source captions."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
env={**os.environ,'PYTHONPATH':str(ROOT/'tools')}
catalog=json.loads(subprocess.check_output(['node','-e',"global.window={LEAP:{}};require('./site/catalog.js');console.log(JSON.stringify(window.LEAP.testingInternet))"],cwd=ROOT,encoding='utf-8'))
for item in catalog[3:]:
    vid=item['id']
    print('FETCH',item['title'],vid,flush=True)
    common=[sys.executable,'-m','yt_dlp','--ignore-config','--no-playlist','--js-runtimes','node','--socket-timeout','25','--retries','2','--no-progress','--no-overwrites','-o',str(ROOT/'videos/%(id)s.%(ext)s')]
    url='https://www.youtube.com/watch?v='+vid
    if not (ROOT/'videos'/f'{vid}.mp4').exists():
        for fmt in ['bv*[height<=1080]+ba/b[height<=1080]','bv*[height<=720]+ba/b[height<=720]','18']:
            result=subprocess.run(common+['--write-info-json','-f',fmt,'--merge-output-format','mp4',url],env=env)
            if result.returncode==0: break
        if result.returncode: print('VIDEO WARNING',vid,flush=True)
    if not (ROOT/'videos'/f'{vid}.en-orig.vtt').exists():
        result=subprocess.run(common+['--skip-download','--write-auto-subs','--sub-langs','en-orig','--sub-format','vtt',url],env=env)
        if result.returncode: print('CAPTION WARNING',vid,flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/read_transcripts.py'),vid],cwd=ROOT,env={**env,'PYTHONIOENCODING':'utf-8'},stdout=subprocess.DEVNULL,check=True)

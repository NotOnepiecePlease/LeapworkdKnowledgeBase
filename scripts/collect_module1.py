"""Download exactly the nine Desktop and Virtual lessons linked by Module 1."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ('desktop-introducao', '-51LTRplY48', 'Introduction to desktop UI automation', 'Desktop'),
    ('desktop-contatos', 'TXWo3qK9Oy8', 'Automating new contact creation', 'Desktop'),
    ('desktop-web', '23YBj_t1EjA', 'Automating across different technologies', 'Desktop'),
    ('virtual-introducao', 'ynF7HY2ux_c', 'Introduction to virtual desktop automation', 'Virtual'),
    ('virtual-imagens', 'sJ3Fa3kSiJg', 'Using image recognition in virtual automation', 'Virtual'),
    ('virtual-textos', 'qGGNbk0UY-0', 'Text and numbers in virtual automation', 'Virtual'),
    ('virtual-cliques', 'fO6aVmNKUCc', 'Clicking elements in virtual automation', 'Virtual'),
    ('virtual-teclado', 'akmkQk8sc40', 'Driving keyboard actions', 'Virtual'),
    ('virtual-areas', 'rK8qIFccfbk', 'Position and areas', 'Virtual'),
]
manifest = [{'slug':s,'video':v,'officialTitle':t,'section':g,
             'source':'https://leapwork.com/learning-center/self-paced-training/'}
            for s,v,t,g in SOURCES]
(ROOT/'research'/'module1-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT/'tools')
for slug, vid, _, _ in SOURCES:
    print('VIDEO', slug, flush=True)
    url='https://www.youtube.com/watch?v='+vid
    common=[sys.executable,'-m','yt_dlp','--ignore-config','--no-playlist','--js-runtimes','node',
            '--socket-timeout','25','--retries','2','--no-progress','--no-overwrites',
            '-o',str(ROOT/'videos'/'%(id)s.%(ext)s')]
    subprocess.run(common+['--write-info-json','-f','bv*[height<=1080]+ba/b[height<=1080]',
                          '--merge-output-format','mp4',url],env=env,check=True)
    if not (ROOT/'videos'/f'{vid}.en-orig.vtt').exists():
        result=subprocess.run(common+['--skip-download','--write-auto-subs','--sub-langs','en-orig',
                                      '--sub-format','vtt',url],env=env)
        if result.returncode: print('CAPTION WARNING',vid,flush=True)

"""Extract reproducible reference frames; create contact sheets for visual review."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SHOTS = {
    'd9m4N9sxFT0': [45, 100, 145, 155, 250, 300, 365, 470],
    '9IdcfvVSKAc': [125, 185, 295, 340, 420, 480],
    'qHp1RY9AQds': [160, 205, 260, 330, 400, 495],
    'M-y1MxK3_Dw': [85, 150, 180, 320, 390, 435],
    'pZAVmupXWhE': [200, 255, 305, 355, 415, 455],
    'aGduKxCIZAk': [135, 160, 200, 245, 280, 315],
    'HWUVg1tTclg': [265, 350, 480, 630, 850, 940],
    '3ALOfIs_OTY': [230, 345, 445, 465, 510, 565],
    'J-ui6FyDkXg': [265, 325, 400, 470, 550, 710],
    'AL_LQQ4yMLc': [150, 195, 235, 290, 325],
    'xAl2LfFKxj0': [105, 130, 150, 180],
    'lsGjkso3Rbg': [110, 125, 140, 155],
    '-51LTRplY48': [205, 278, 333, 425, 510],
    'TXWo3qK9Oy8': [155, 270, 430, 580, 680, 865, 920],
    '23YBj_t1EjA': [205, 275, 405, 615, 880, 955, 1080],
    'ynF7HY2ux_c': [240, 330, 380, 450, 545, 675, 795],
    'sJ3Fa3kSiJg': [210, 325, 390, 450, 620, 750, 850],
    'qGGNbk0UY-0': [210, 355, 505, 610, 680, 715],
    'fO6aVmNKUCc': [135, 220, 275, 365, 440, 565, 610],
    'akmkQk8sc40': [175, 275, 395, 450, 555, 610, 705, 745],
    'rK8qIFccfbk': [175, 315, 375, 610, 780, 875, 925, 985],
}
OUT = ROOT / 'site' / 'assets' / 'frames'
OUT.mkdir(parents=True, exist_ok=True)
REVIEW = ROOT / 'research' / 'contact-sheets'
REVIEW.mkdir(parents=True, exist_ok=True)
for vid, times in SHOTS.items():
    video = ROOT / 'videos' / f'{vid}.mp4'
    if not video.exists():
        print('MISSING', video, flush=True)
        continue
    rows = (len(times) + 1) // 2
    sheet = Image.new('RGB', (1280, rows * 390), '#15241f')
    draw = ImageDraw.Draw(sheet)
    for i, sec in enumerate(times):
        target = OUT / f'{vid}-{sec}.jpg'
        if not target.exists():
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', str(sec),
                            '-i', str(video), '-frames:v', '1', '-q:v', '2', str(target)], check=True)
        with Image.open(target) as image:
            thumb = image.copy()
            thumb.thumbnail((640, 360))
            x, y = (i % 2) * 640, (i // 2) * 390
            sheet.paste(thumb, (x, y + 30))
            draw.text((x + 12, y + 8), f'{vid} | {sec//60:02}:{sec%60:02}', fill='white')
    sheet.save(REVIEW / f'{vid}.jpg', quality=90)
    print('EXTRACTED', vid, len(times), flush=True)
(ROOT / 'research' / 'frames-manifest.json').write_text(json.dumps(SHOTS, indent=2), encoding='utf-8')

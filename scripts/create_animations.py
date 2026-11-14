"""Create short, user-controlled GIF excerpts directly from local source videos."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site' / 'assets' / 'animations'
OUT.mkdir(parents=True, exist_ok=True)
CLIPS = [
    ('senha-password', 'd9m4N9sxFT0', 147, 158),
    ('estrategias-dom', 'lsGjkso3Rbg', 119, 158),
    ('linhas-desktop', 'HWUVg1tTclg', 423, 461),
    ('campo-dinamico', '3ALOfIs_OTY', 430, 458),
    ('troca-janelas', 'J-ui6FyDkXg', 686, 706),
    ('contatos-iteracao', 'TXWo3qK9Oy8', 905, 925),
    ('virtual-ponto-imagem', 'sJ3Fa3kSiJg', 385, 415),
    ('virtual-atalhos', 'akmkQk8sc40', 379, 413),
    ('virtual-area-relativa', 'rK8qIFccfbk', 870, 894),
    ('web-arraste', 'suIDRArjQEk', 144, 157),
    ('web-visibilidade', 'YP3TJrud2BY', 194, 224),
    ('web-hover', '5SALJ43raC4', 248, 275),
    ('web-imagem-deslocada', 'N8utEzbs2SM', 158, 185),
    ('dados-parametrizacao', 'V5r-Fovn_vs', 43, 65),
]
manifest = []
for name, video, start, end in CLIPS:
    target = OUT / f'{name}.gif'
    if not target.exists():
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', str(start),
            '-t', str(end-start), '-i', str(ROOT / 'videos' / f'{video}.mp4'),
            '-filter_complex', 'fps=5,scale=1280:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=3',
            '-loop', '0', str(target)
        ], check=True)
    manifest.append({'file':target.name,'video':video,'start':start,'end':end,'bytes':target.stat().st_size})
    print(name, target.stat().st_size, flush=True)
(ROOT / 'research' / 'animations-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

"""Embed the OFL-licensed fonts so local-file reading needs no external requests."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
fonts = ROOT / 'site' / 'assets' / 'fonts'
rules = []
for family in ['Manrope','Outfit']:
    source = fonts / (family + '.ttf')
    encoded = base64.b64encode(source.read_bytes()).decode('ascii')
    rules.append("@font-face{font-family:'"+family+"';font-style:normal;font-weight:200 800;font-display:swap;src:url(data:font/ttf;base64,"+encoded+") format('truetype');}")
(fonts / 'fonts.css').write_text('\n'.join(rules), encoding='utf-8')
print('Manrope e Outfit incorporadas para uso offline; licenças OFL preservadas.')

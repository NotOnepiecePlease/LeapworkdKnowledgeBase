"""Cache official documentation and its source links for the local study guide."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research' / 'docs'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://docs.leapwork.com/leapwork-flow/latest/'
PAGES = [
    'what-is-leapwork/architecture-overview', 'building-blocks',
    'working-with-leapwork/designing-automation-flows',
    'working-with-leapwork/designing-automation-flows/sub-flows',
    'building-blocks/web', 'building-blocks/web/start-web-browser',
    'building-blocks/web/type-web-text', 'building-blocks/web/click-web-element',
    'building-blocks/web/find-web-element', 'building-blocks/web/set-web-dropdown',
    'building-blocks/web/set-web-radio-button', 'building-blocks/web/get-web-text',
    'building-blocks/web/get-web-number', 'building-blocks/logic',
    'building-blocks/module-input-and-output', 'building-blocks/start-stop',
    'building-blocks/module-input-and-output/value-input',
    'building-blocks/logic/compare', 'working-with-leapwork/strategy-editor',
    'building-blocks/desktop-ui', 'building-blocks/desktop-ui/find-ui-element',
    'building-blocks/desktop-ui/get-ui-number', 'building-blocks/desktop-ui/get-ui-text',
    'building-blocks/desktop-ui/use-ui-window', 'building-blocks/desktop-ui/set-ui-element-value',
    'building-blocks/variables/set-variable', 'building-blocks/variables/get-variable',
    'building-blocks/logic/calculate', 'building-blocks/data-driven/read-excel',
    'building-blocks/desktop-ui/start-application', 'building-blocks/desktop-ui/click-ui-element',
    'building-blocks/image-and-text-recognition', 'building-blocks/image-and-text-recognition/find-image',
    'building-blocks/image-and-text-recognition/find-text', 'building-blocks/image-and-text-recognition/get-text',
    'building-blocks/image-and-text-recognition/get-number', 'building-blocks/mouse-and-keyboard',
    'building-blocks/mouse-and-keyboard/click-image', 'building-blocks/mouse-and-keyboard/click-text',
    'building-blocks/mouse-and-keyboard/click-position', 'building-blocks/mouse-and-keyboard/type-text',
    'building-blocks/mouse-and-keyboard/press-key', 'building-blocks/mouse-and-keyboard/release-key',
    'building-blocks/mouse-and-keyboard/hover-position', 'building-blocks/mouse-and-keyboard/hover-text',
    'building-blocks/mouse-and-keyboard/scroll-wheel', 'building-blocks/logic/offset-area',
    'building-blocks/logic/offset-position', 'building-blocks/logic/loop',
    'building-blocks/setting-values/set-area', 'building-blocks/web/use-browser-window',
    'building-blocks/module-input-and-output/execution-input',
    'building-blocks/module-input-and-output/execution-output',
    'building-blocks/web/set-web-checkbox', 'building-blocks/web/drag-web-element',
    'building-blocks/web/hover-web-element', 'building-blocks/web/handle-web-alert',
    'building-blocks/web/get-web-attribute', 'building-blocks/web/navigate-web',
    'building-blocks/logic/wait',
    'building-blocks/data-driven',
    'building-blocks/variables',
    'building-blocks/generators',
    'building-blocks/data-driven/write-excel',
    'building-blocks/data-driven/database',
    'building-blocks/data-driven/http-request',
    'building-blocks/data-driven/compress-file',
    'building-blocks/data-driven/save-file',
    'building-blocks/data-driven/set-file',
    'building-blocks/data-driven/command-line',
    'building-blocks/data-driven/send-e-mail',
    'building-blocks/logic/change-text',
    'building-blocks/logic/regular-expression',
    'building-blocks/logic/switch',
    'building-blocks/logic/break-iteration',
    'building-blocks/logic/offset-date-time',
    'building-blocks/logic/c-sharp-code',
    'building-blocks/logic/get-clipboard',
    'building-blocks/logic/set-clipboard',
    'building-blocks/logic/close-windows',
    'building-blocks/generators/generate-date-time',
    'building-blocks/generators/generate-number',
    'building-blocks/generators/generate-password',
]

def collect(path):
    url = BASE + path
    dest = OUT / (path.replace('/', '__') + '.json')
    if dest.exists():
        return json.loads(dest.read_text(encoding='utf-8'))
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(request, timeout=40) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        url = response.url
    title = soup.title.get_text(' ', strip=True).split('|')[0].strip() if soup.title else path
    main = soup.find('main') or soup.find('article') or soup
    for node in main.select('nav, header, footer, script, style'):
        node.decompose()
    data = {
        'url': url, 'title': title,
        'retrievedAt': datetime.now(timezone.utc).isoformat(),
        'text': main.get_text('\n', strip=True),
        'links': [{'title': a.get_text(' ', strip=True), 'url': urljoin(url, a['href'])}
                  for a in main.select('a[href]')],
        'images': [{'alt': i.get('alt', ''), 'url': urljoin(url, i.get('src', ''))}
                   for i in main.select('img[src]')],
    }
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data

if __name__ == '__main__':
    for path in PAGES:
        try:
            d = collect(path)
            print(d['title'], d['url'], len(d['text']))
        except Exception as error:
            print('ERROR', path, str(error))

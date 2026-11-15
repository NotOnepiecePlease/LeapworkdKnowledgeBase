"""Armazena referências oficiais e imagens de interface do módulo 4."""
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from collect_docs import collect

ROOT = Path(__file__).resolve().parents[1]
ADMIN = ['controller-settings', 'user-management', 'emergency-admin-user', 'team-management',
         'wip-security', 'privileges-settings', 'workflow-stettings', 'api-access-keys',
         'e-mail-settings', 'proxy-settings', 'database-decryption-keys', 'database-management',
         'default-flow-settings', 'wip-web-settings', 'wip-capture-settings', 'retention-policies',
         'license-management', 'audit-log', 'other-settings', 'connections',
         'wip-azure-devops-connections', 'mobile-configuration', 'active-directory-settings', 'diagnostics']
WORK = ['agents-overview', 'run-lists', 'run-lists/schedules', 'reporting', 'dashboards',
        'designing-automation-flows', 'designing-automation-flows/flows', 'organizing-your-work',
        'git-version-control']
PICTURES = ['controller-settings', 'user-management', 'connections', 'retention-policies',
            'default-flow-settings', 'agents-overview', 'run-lists', 'schedules', 'reporting',
            'dashboards', 'audit-log', 'flows', 'designing-automation-flows']
MANIFEST = ROOT / 'research/module4-documents.json'
PREVIOUS = {record['path']: record for record in json.loads(MANIFEST.read_text(encoding='utf-8'))} if MANIFEST.exists() else {}


def prepare(path):
    doc = collect(path)
    record = {'path': path, 'url': doc['url'], 'title': doc['title'], 'retrievedAt': doc['retrievedAt']}
    name = path.split('/')[-1]
    if name in PICTURES and doc['images']:
        image_index = {'designing-automation-flows': 14, 'agents-overview': 2, 'schedules': 2}.get(name, 0)
        source = doc['images'][image_index]['url']
        dest = ROOT / 'site/assets/docs' / ('m4-' + name + '.png')
        if not dest.exists() or PREVIOUS.get(path, {}).get('imageSource') != source:
            dest.write_bytes(urlopen(Request(source, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read())
        from PIL import Image
        with Image.open(dest) as image:
            record['size'] = image.size
        record.update(image='assets/docs/' + dest.name, imageSource=source)
    return record


if __name__ == '__main__':
    paths = ['administration'] + ['administration/' + p for p in ADMIN] + ['working-with-leapwork/' + p for p in WORK]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(prepare, paths))
    (ROOT / 'research/module4-documents.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'documents': len(records), 'images': sum('image' in r for r in records)}))

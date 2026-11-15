"""Preserva fontes e contrato OpenAPI usados no módulo final."""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image
from collect_docs import collect

ROOT=Path(__file__).resolve().parents[1]
BASE='https://docs.leapwork.com/best-practices/latest/leapwork-flow-best-practices/'
EXTERNAL={
    'best-practices/organizing-daily-work':BASE+'organizing-daily-work-in-leapwork',
    'best-practices/working-with-run-lists':BASE+'working-with-run-lists',
    'best-practices/ai-blocks':BASE+'guidelines-for-using-the-ai-blocks',
}
PATHS=[
    *EXTERNAL,'public-rest-apis','public-rest-apis/api-endpoints',
    'working-with-leapwork/organizing-your-work',
    'working-with-leapwork/designing-automation-flows',
    'working-with-leapwork/designing-automation-flows/sub-flows',
    'building-blocks/module-input-and-output/value-input',
    'building-blocks/module-input-and-output/value-output',
    'building-blocks/web/find-web-element','building-blocks/web/get-web-text',
    'building-blocks/logic/compare','building-blocks/logic/wait',
    'building-blocks/data-driven/read-excel','building-blocks/data-driven/http-request',
    'administration/api-access-keys','administration/wip-azure-devops-connections',
    'administration/connections/azure-devops-ado-server-connections',
    'working-with-leapwork/microsoft-ado-test-plan-integration',
    'working-with-leapwork/git-version-control/use-git-versioning-for-flows-and-subflows',
    'working-with-leapwork/git-version-control/check-git-sync-status-and-resolve-upload-failures',
    'working-with-leapwork/run-lists','working-with-leapwork/run-lists/schedules',
    'working-with-leapwork/reporting','working-with-leapwork/dashboards',
    'administration/retention-policies','administration/audit-log',
]
PICTURES={
    'best-practices/organizing-daily-work':('organization',0),
    'working-with-leapwork/microsoft-ado-test-plan-integration':('ado',0),
    'working-with-leapwork/git-version-control/use-git-versioning-for-flows-and-subflows':('git',0),
    'building-blocks/module-input-and-output/value-input':('input',0),
    'building-blocks/module-input-and-output/value-output':('output',0),
}


def prepare(path):
    doc=collect(path,EXTERNAL.get(path))
    result={'path':path,'url':doc['url'],'title':doc['title'],'retrievedAt':doc['retrievedAt']}
    if path in PICTURES and doc['images']:
        name,index=PICTURES[path]
        source=doc['images'][index]['url']
        dest=ROOT/'site/assets/docs'/f'm5-{name}.png'
        if not dest.exists():dest.write_bytes(urlopen(Request(source,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
        with Image.open(dest) as image:result['size']=image.size
        result.update(image='assets/docs/'+dest.name,imageSource=source)
    return result


if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(prepare,PATHS))
    endpoints=next(r for r in records if r['path']=='public-rest-apis/api-endpoints')
    doc=collect(endpoints['path'])
    url=next(link['url'] for link in doc['links'] if link['title']=='Open API Spec')
    spec=ROOT/'research/module5-api-spec.json'
    if not spec.exists():spec.write_bytes(urlopen(url,timeout=40).read())
    contract=json.loads(spec.read_text(encoding='utf-8'))
    assert contract['info']['version']=='v4'
    assert 'put' in contract['paths']['/api/v4/schedules/{scheduleId}/runNow']
    assert contract['components']['schemas']['RunStatus']['enum']==['Queued','Executing','Finished']
    (ROOT/'research/module5-documents.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'documents':len(records),'images':sum('image' in r for r in records),'apiVersion':contract['info']['version'],'specSource':url,'specSha256':hashlib.sha256(spec.read_bytes()).hexdigest()}),flush=True)

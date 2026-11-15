"""Confere integridade da revisão editorial e regressões de correspondência já identificadas.

Hashes detectam conteúdo alterado depois da revisão; não são prova de correção semântica.
"""
import hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
course=json.loads((ROOT/'research/course-content.json').read_text(encoding='utf-8'))
library=json.loads((ROOT/'research/documentation-editorial.json').read_text(encoding='utf-8'))
review=json.loads((ROOT/'research/editorial-review.json').read_text(encoding='utf-8'))
lessons={l['slug']:l for l in course['lessons']}
cards={p['path']:p for p in library['pages']}
passed=[];errors=[]
def check(label,value):
    assert value,label
    passed.append(label)
def step(slug,num):return lessons[slug]['steps'][num-1]
check('Review covers all lessons, steps, cards and current figures',review['counts']=={'lessons':98,'steps':427,'cards':338,'operations':83,'visualPairsBefore':336,'visualPairsAfter':324,'removedFigureUses':12,'replacedSupplementUses':6,'replacedOriginalUses':1,'movedSupplementUses':3,'changedSteps':83})
for row in review['lessons']:check('Reviewed lesson unchanged: '+row['slug'],digest(lessons[row['slug']])==row['sha256'])
for row in review['steps']:check('Reviewed step unchanged: '+row['lesson']+'/'+str(row['step']),digest(step(row['lesson'],row['step']))==row['sha256'] and bool(row['source']))
for row in review['cards']:check('Reviewed reference unchanged: '+row['path'],digest(cards[row['path']])==row['sha256'])
for row in review['figures']:check('Reviewed image unchanged: '+row['lesson']+'/'+str(row['step'])+'/'+row['path'],hashlib.sha256((ROOT/'site'/row['path']).read_bytes()).hexdigest()==row['sha256'] and bool(row['basis']))
check('Reviewed operation catalog unchanged',digest(library['operations'])==review['operationsSha256'])
check('Access planning points to User Management',step('controle-ambiente',4)['doc']=='administration/user-management' and not step('controle-ambiente',4).get('additionalFigures'))
check('Expired license screenshot excluded',not step('controle-ambiente',2).get('additionalFigures'))
check('Reading origin illustration shows Local path',step('dados-ler-excel',1)['additionalFigures'][0]['sourceImageIndex']==2)
check('Range screenshot belongs to range preparation',step('dados-escrever-excel',1)['additionalFigures'][0]['sourceImageIndex']==3 and not step('dados-escrever-excel',2).get('additionalFigures'))
check('CSharp references show System Assemblies',step('dados-csharp',3)['additionalFigures'][0]['sourceImageIndex']==4 and not step('dados-csharp',2).get('additionalFigures'))
check('CSharp runtime is qualified by version','2026.1+' not in step('dados-csharp',3)['text'] and '.NET 10' in step('dados-csharp',3)['text'])
check('GET exercise does not show POST screenshot',not step('dados-http',1).get('imagePath') and 'GET' in step('dados-http',1)['text'])
check('Trim exercise does not show Substring screenshot',not step('dados-textos',1).get('imagePath') and 'Trim' in step('dados-textos',1)['text'])
check('Run List figure shows Add flows selection',step('controle-runlists',2)['additionalFigures'][0]['sourceImageIndex']==13)
check('Distribution exercise does not show flow order',not step('controle-agendamentos',2).get('additionalFigures'))
check('Schedule overview shows the schedule form',step('ciclo-integracoes',2)['additionalFigures'][0]['sourceImageIndex']==2)
check('Asset filtering does not show date-value filter',not step('controle-auditoria',2).get('additionalFigures'))
check('Version list belongs to opening history',step('controle-historico',2)['additionalFigures'][0]['sourceImageIndex']==14 and not step('controle-historico',2).get('imagePath'))
check('Restoration comparison is not illustrated by version table',not step('controle-restauracao',2).get('imagePath'))
check('Dropdown figure contains the reviewed Option 2 moment',step('dropdowns-avancados',3)['additionalFigures'][0]['time']==189)
check('Start date instruction uses the matching configured frame',step('formularios',2)['image']==234 and 'Value = Start date' in step('formularios',2)['caption'])
check('Window link step does not show the destination tab',not step('nova-janela',1).get('additionalFigures'))
check('Save File source and lesson agree on managed storage','armazenamento gerenciado' in cards['building-blocks/data-driven/save-file']['summary'] and 'caminho manual' in cards['building-blocks/data-driven/save-file']['summary'])
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page()
    page.on('pageerror',lambda err:errors.append(str(err)))
    url=(ROOT/'site/index.html').as_uri()
    page.goto(url+'#aula/controle-ambiente')
    check('Access step renders without unrelated image',page.locator('#passo-4 img').count()==0 and page.locator('#passo-4 a[href$="administration/user-management"]').count()==1)
    page.goto(url+'#aula/dropdowns-avancados')
    check('Corrected dropdown frame renders',page.locator('#passo-3 img[src$="r8IH1LYegOo-189-audit.jpg"]').count()==1)
    page.goto(url+'#documentacao/building-blocks/data-driven/save-file')
    check('Corrected Save File summary renders','armazenamento gerenciado' in page.locator('main').inner_text())
    page.goto(url+'#aula/dados-csharp')
    check('Version-specific CSharp correction renders','.NET 10' in page.locator('#passo-3').inner_text())
    check('No JavaScript errors',not errors);browser.close()
(ROOT/'research/qa/editorial-review-report.json').write_text(json.dumps({'passed':passed,'errors':errors,'semanticLimit':'Confere integridade e regressões conhecidas. A avaliação de pertinência é editorial; não houve execução em Leapwork.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

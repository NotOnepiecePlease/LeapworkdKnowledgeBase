"""Verifica cobertura da navegação, fichas, API, figuras e funcionamento offline."""
import json
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'research/qa'
URL=(ROOT/'site/index.html').as_uri()
passed,errors,requests=[],[],[]


def check(name,condition):
    assert condition,name
    passed.append(name)
    if len(passed)%100==0:print(f'{len(passed)} verificações concluídas',flush=True)


inventory=json.loads((ROOT/'research/documentation-inventory.json').read_text(encoding='utf-8'))
library=json.loads((ROOT/'research/documentation-editorial.json').read_text(encoding='utf-8'))
report=json.loads((ROOT/'research/enrichment-report.json').read_text(encoding='utf-8'))
spec=json.loads((ROOT/'research/module5-api-spec.json').read_text(encoding='utf-8'))
check('All 338 navigation pages read without page failure',inventory['navigationPages']==338 and inventory['pagesRead']==338 and inventory['unavailable']==0)
check('338 editorial cards, 213 additional sources',len(library['pages'])==338 and library['counts']['newSources']==213)
check('Eight section counts cover all pages',len(library['sections'])==8 and sum(s['count'] for s in library['sections'])==338)
check('Unique routes for every card',len({p['path'] for p in library['pages']})==338)
check('All card source URLs are inventoried',all(p['source'] in {x['url'] for x in inventory['pages']} for p in library['pages']))
check('Source origin stays in requested product and version',all(p['source'].startswith('https://docs.leapwork.com/leapwork-flow/latest/') for p in library['pages']))
check('Every child route resolves',all(child in {x['path'] for x in library['pages']} for p in library['pages'] for child in p['children']))
check('All 83 contract operations covered',len(library['operations'])==83 and {(o['method'].lower(),o['path']) for o in library['operations']}=={(m,path) for path,methods in spec['paths'].items() for m in methods if m in ['get','put','post','delete','patch']})
check('81 figure inclusions, 72 unique assets',report['addedFigureUses']==81 and report['uniqueSupplementAssets']==72)
check('75 steps receive figures; 74 were previously without',report['stepsReceivingFigures']==75 and report['newlyIllustratedSteps']==74 and report['illustratedStepsAfter']==329)
check('All 427 steps have a recorded audit decision',len(report['steps'])==427 and all(r['decision'] for r in report['steps']))
for row in report['additions']:
    check('Asset and source: '+row['lesson']+' #'+str(row['step'])+' / '+row['path'],(ROOT/'site'/row['path']).is_file() and row['width']>0 and row['height']>0 and row['source'].startswith(('https://docs.leapwork.com/','https://www.youtube.com/')))

with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda req:requests.append(req.url))
    page.goto(URL+'#documentacao');page.wait_for_selector('.doc-result')
    check('Library root renders all cards and eight menus',page.locator('.doc-result').count()==338 and page.locator('.doc-section-card').count()==8)
    page.locator('[data-doc-filter]').fill('instalacao')
    check('Local library filter handles accents',page.locator('.doc-result:visible').count()>0 and page.locator('.doc-result:visible').count()<338)
    page.locator('[data-doc-filter]').fill('<script>sem-correspondencia</script>')
    check('Empty search state uses safe text',page.locator('.doc-result:visible').count()==0 and page.locator('.doc-no-results').is_visible())
    for card in library['pages']:
        page.goto(URL+'#documentacao/'+card['path']);page.wait_for_selector('main h1')
        check('Card renders with its original source: '+card['path'],page.locator('main h1').inner_text()==card['title'] and page.locator('.lesson-hero a.button').first.get_attribute('href')==card['source'])
        check('No missing labels: '+card['path'],'undefined' not in page.locator('main').inner_text())
    page.goto(URL+'#documentacao/public-rest-apis/api-endpoints')
    check('Full API catalog rendered',page.locator('.api-operation').count()==83)
    page.locator('[data-api-filter]').fill('PUT')
    expected=sum(o['method']=='PUT' for o in library['operations'])
    check('API method filter matches contract',page.locator('.api-operation:visible').count()==expected)
    check('Catalog offers no execution control',page.locator('#api-catalog button').count()==0)
    page.locator('#search').fill('Electron')
    page.wait_for_selector('.search-result')
    check('Global search finds newly covered technology',page.locator('.search-result[href^="#documentacao/building-blocks/electron-blocks"]').count()>0)
    page.goto(URL+'#aula/controle-acessos/passo-4')
    page.wait_for_function("document.activeElement.id==='passo-4'")
    check('User example receives three relevant figures',page.locator('#passo-4 .supplement-figure').count()==3)
    for img in page.locator('#passo-4 .supplement-figure img').all():img.evaluate('(img)=>{img.loading="eager";return img.decode()}')
    check('AD/SSO figure points to correct source',page.locator('#passo-4 .supplement-figure a[href="https://docs.leapwork.com/leapwork-flow/latest/administration/user-management"]').count()==2)
    page.locator('#passo-4 [data-image]').first.click()
    check('New figure opens in original zoom dialog',page.locator('#image-dialog').evaluate('(d)=>d.open'))
    page.wait_for_function("document.getElementById('large-image').naturalWidth>0");page.keyboard.press('Escape')
    page.locator('#lesson-notes').fill('Nota preservada após novas referências.')
    page.reload()
    check('Existing notes storage remains functional',page.locator('#lesson-notes').input_value()=='Nota preservada após novas referências.')
    for slug in sorted({row['lesson'] for row in report['additions']} - {'@introducao'}):
        page.goto(URL+'#aula/'+slug);page.wait_for_selector('.step')
        expected=sum(r['lesson']==slug for r in report['additions'])
        check('Supplement count matches manifest: '+slug,page.locator('.supplement-figure').count()==expected)
        for img in page.locator('.supplement-figure img').all():
            img.evaluate('(img)=>{img.loading="eager";return img.decode()}')
            check('New figure loads: '+slug+' / '+img.get_attribute('src'),img.evaluate('(img)=>img.naturalWidth>0'))
    page.goto(URL+'#introducao')
    check('Architecture includes protocols and deployment tables',page.locator('#arquitetura-complementar table').count()==2 and page.locator('#arquitetura-complementar .supplement-figure').count()==3)
    for img in page.locator('#arquitetura-complementar img').all():img.evaluate('(img)=>{img.loading="eager";return img.decode()}')
    page.goto(URL+'#novidades')
    check('Report lists all enriched lessons and intro',page.locator('main .source-list li').count()==47)
    for theme in ['light','dark']:
        page.goto(URL+'#documentacao')
        if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
        for route in ['documentacao','documentacao/public-rest-apis/api-endpoints','documentacao/building-blocks/electron-blocks','novidades','introducao','aula/controle-acessos']:
            page.goto(URL+'#'+route);page.wait_for_selector('main h1')
            for width in [1440,768,390]:
                page.set_viewport_size({'width':width,'height':1000})
                check('No overflow '+theme+' '+str(width)+' / '+route,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000});page.goto(URL+'#documentacao');page.screenshot(path=str(QA/f'documentation-{theme}.png'))
    check('No JavaScript errors',not errors)
    check('All tested routes stay offline',not any(u.startswith(('http://','https://')) for u in requests))
    browser.close()
(QA/'documentation-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

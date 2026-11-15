"""Confere o módulo final, os contratos da API e os laboratórios sem rede."""
import csv
import io
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'research/qa'
URL=(ROOT/'site/index.html').as_uri()
passed,errors,requests=[],[],[]


def check(name,condition):
    assert condition,name
    passed.append(name)


with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce',accept_downloads=True)
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda req:requests.append(req.url))
    page.goto(URL)
    page.evaluate("localStorage.setItem('leapwork-caderno-v1',JSON.stringify({completed:['primeiro-fluxo','dados-fundamentos','controle-restauracao'],notes:{'primeiro-fluxo':'Nota antiga Web','controle-restauracao':'Nota antiga controle'}}))")
    page.goto(URL+'#modulo/5');page.reload();page.wait_for_selector('.lesson-card')
    lessons=page.evaluate('window.LEAP.lessons.filter(l=>l.module===5)')
    check('98 lessons in five modules',page.evaluate('window.LEAP.lessons.length')==98 and page.evaluate('new Set(window.LEAP.lessons.map(l=>l.module)).size')==5)
    check('16 documentation lessons with no fabricated videos',len(lessons)==16 and all(not l.get('video') and l['sourceKind']=='documentation' for l in lessons))
    check('16 overview cards',page.locator('.lesson-card').count()==16)
    check('Ten fictional cases',page.locator('[data-m5-case]').count()==10)
    check('Module 5 starts with independent progress',page.locator('.progress-overview progress').get_attribute('value')=='0')
    spec=json.loads((ROOT/'research/module5-api-spec.json').read_text(encoding='utf-8'))
    for endpoint in page.evaluate('window.LEAP.module5Endpoints'):
        check('Method and path in official OpenAPI: '+endpoint['method']+' '+endpoint['path'],endpoint['method'].lower() in spec['paths'][endpoint['path']])
    check('Run states match stored OpenAPI',spec['components']['schemas']['RunStatus']['enum']==['Queued','Executing','Finished'])
    check('Done is a distinct item state',all(s in spec['components']['schemas']['ApiRunItemStatus']['enum'] for s in ['Done','Passed','Failed']))
    page.locator('a[href="#modulo/5/tema-integracoes"]').first.click()
    page.wait_for_function("document.activeElement.id==='tema-integracoes'")
    check('Topic shortcut focuses its target',page.locator('#tema-integracoes').evaluate('(e)=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<innerHeight'))
    for lesson in lessons:
        slug=lesson['slug'];page.goto(URL+'#aula/'+slug);page.wait_for_selector('.quiz-form[data-lesson="'+slug+'"]')
        check('Back link to module 5: '+slug,page.locator('.back-link').get_attribute('href')=='#modulo/5')
        check('Four documented steps without fake player: '+slug,page.locator('.step').count()==4 and page.locator('.step-source a[href^="https://docs.leapwork.com/"]').count()==4 and page.locator('[data-video]').count()==0)
        check('Review has two questions: '+slug,len(lesson['quiz'])==2)
        for i,q in enumerate(lesson['quiz']):page.locator(f'input[name="q{i}"][value="{q["correct"]}"]').check()
        page.locator('.quiz-form button[type=submit]').click()
        check('Review answers and explanation: '+slug,'2 de 2' in page.locator('.quiz-feedback').inner_text() and all(q['why'] in page.locator('.quiz-form').inner_text() for q in lesson['quiz']))
        for _,path in lesson['docs']:
            check('Cached official reference: '+slug+' / '+path,(ROOT/'research/docs'/(path.replace('/','__')+'.json')).is_file())
        for image in page.locator('.step img').all():
            image.evaluate('(img)=>img.decode()');check('Image loads: '+slug,image.evaluate('(img)=>img.naturalWidth>0'))
        check('No missing labels: '+slug,'undefined' not in page.locator('main').inner_text())
    page.goto(URL+'#aula/ciclo-organizacao')
    check('Best Practices primary source resolves outside Flow namespace',page.locator('.lesson-hero a.button').first.get_attribute('href').startswith('https://docs.leapwork.com/best-practices/latest/'))
    check('Best Practices step source is correctly resolved','/best-practices/latest/' in page.locator('.step-source a').first.get_attribute('href'))
    page.goto(URL+'#aula/ciclo-api-resultados')
    page.locator('#lesson-notes').fill('Finished não é Passed. <script>texto de estudo</script>')
    page.locator('[data-complete]').click();page.reload()
    check('New notes and completion persist safely',page.locator('#lesson-notes').input_value()=='Finished não é Passed. <script>texto de estudo</script>' and page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    with page.expect_download() as download:page.locator('[data-export]').click()
    text=Path(download.value.path()).read_text(encoding='utf-8')
    check('Notes export preserves older modules and new module','Nota antiga Web' in text and 'Nota antiga controle' in text and 'Finished não é Passed' in text)
    page.goto(URL+'#modulo/5')
    check('Independent progress is one of sixteen',page.locator('.progress-overview progress').get_attribute('value')=='1' and page.locator('.progress-overview progress').get_attribute('max')=='16')
    check('Previous completion intact',page.evaluate("['primeiro-fluxo','dados-fundamentos','controle-restauracao'].every(s=>JSON.parse(localStorage.getItem('leapwork-caderno-v1')).completed.includes(s))"))
    baseline={'http':200,'run':'Finished','items':['Passed']*4,'expected':4,'correlated':True,'timeout':False}
    scenarios=[('criteria-met',{}),('integration-error',{'http':401}),('integration-error',{'http':503}),('correlation-error',{'correlated':False}),('wait',{'run':'Queued'}),('wait',{'run':'Executing'}),('timeout',{'run':'Executing','timeout':True}),('incomplete',{'items':[]}),('incomplete',{'items':['Passed']*3}),('incomplete',{'items':['Passed']*5})]
    scenarios += [('review',{'items':['Passed']*3+[state]}) for state in ['Failed','Done','Cancelled','Error','NoStatus','IsProcessing']]
    for i,(code,changes) in enumerate(scenarios):
        actual=page.evaluate('(input)=>window.LEAP.module5EvaluateIntegration(input)',baseline|changes)
        check('Integration decision '+str(i)+' / '+code,actual['code']==code)
    for changes in [{'expected':0},{'expected':1.5},{'items':['invented']},{'items':['Passed']*21},{'http':999},{'run':'Unknown'}]:
        check('Invalid integration input rejected: '+str(changes)[:60],page.evaluate('(x)=>{try{window.LEAP.module5EvaluateIntegration(x);return false}catch{return true}}',baseline|changes))
    f=page.locator('#m5-integration');f.locator('button[type=submit]').click()
    check('Initial 200 with Queued requires waiting','Aguardar dentro do prazo' in page.locator('#m5-integration-output').inner_text())
    f.locator('select[name=run]').select_option('Finished');f.locator('select[name=item]').select_option('Done');f.locator('button[type=submit]').click()
    check('UI does not treat Done as Passed','Revisar os resultados' in page.locator('#m5-integration-output').inner_text())
    f.locator('select[name=item]').select_option('Passed');f.locator('button[type=submit]').click()
    check('UI accepts complete correlated fictional case','Critérios didáticos atendidos' in page.locator('#m5-integration-output').inner_text())
    f.locator('input[name=received]').fill('0');f.locator('button[type=submit]').click()
    check('UI rejects empty population','Revisar a população' in page.locator('#m5-integration-output').inner_text())
    f.locator('input[name=received]').fill('4.5');check('Fractional count rejected',not f.evaluate('(form)=>form.checkValidity()'))
    f.locator('input[name=received]').fill('4')
    cycle=page.locator('#m5-cycle');cycle.locator('button[type=submit]').click()
    result=page.locator('#m5-cycle-output').inner_text()
    check('Initial matrix reports all four categories','5 aprovados · 1 falhos · 1 bloqueados · 3 não executados' in result and '50%' in result and '6/10' in result)
    rows=page.evaluate('window.LEAP.module5Cases.map(c=>({id:c.id,status:"passed",evidence:true}))')
    review=page.evaluate('(rows)=>window.LEAP.module5ReviewCycle(rows,[true,true,true])',rows)
    check('Complete matrix meets explicit criteria',review['met'] and review['approvedPercent']==100)
    for state in ['failed','blocked','notrun']:
        changed=[dict(r) for r in rows];changed[-1]['status']=state
        check('Each pending category prevents completion: '+state,not page.evaluate('(r)=>window.LEAP.module5ReviewCycle(r,[true,true,true]).met',changed))
    changed=[dict(r) for r in rows];changed[-1]['evidence']=False
    check('Missing evidence prevents completion',not page.evaluate('(r)=>window.LEAP.module5ReviewCycle(r,[true,true,true]).met',changed))
    for ready in [[False,True,True],[True,False,True],[True,True,False]]:
        check('Missing prerequisite prevents completion: '+str(ready),not page.evaluate('([r,p])=>window.LEAP.module5ReviewCycle(r,p).met',[rows,ready]))
    check('Duplicate case IDs rejected',page.evaluate('(r)=>{try{window.LEAP.module5ReviewCycle([r[0],...r.slice(0,9)],[true,true,true]);return false}catch{return true}}',rows))
    for c in page.evaluate('window.LEAP.module5Cases'):
        cycle.locator('select[name="status-'+c['id']+'"]').select_option('passed')
        cycle.locator('input[name="evidence-'+c['id']+'"]').check()
    cycle.locator('button[type=submit]').click()
    check('All ten complete UI scenario accepted','Critérios didáticos atendidos' in page.locator('#m5-cycle-output').inner_text())
    cycle.locator('input[name=environment]').uncheck();cycle.locator('button[type=submit]').click()
    check('UI prerequisite is respected','Ciclo com pendências' in page.locator('#m5-cycle-output').inner_text())
    page.locator('[data-m5-reset]').click()
    check('Reset restores original fictional matrix','5 aprovados' in page.locator('#m5-cycle-output').inner_text() and cycle.locator('input[name=environment]').is_checked())
    page.locator('#m5-notes').fill('Parecer de estudo <script>literal</script>')
    with page.expect_download() as download:page.locator('[data-m5-json]').click()
    payload=json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
    check('JSON exports current selections and literal note',payload['kind']=='projeto-autoral-modulo5' and payload['integration']['decision']['code']=='criteria-met' and payload['cycle']['review']['counts']['notrun']==3 and payload['notes']=='Parecer de estudo <script>literal</script>')
    with page.expect_download() as download:page.locator('[data-m5-csv]').click()
    raw=Path(download.value.path()).read_text(encoding='utf-8-sig');matrix=list(csv.DictReader(io.StringIO(raw),delimiter=';'))
    check('CSV exports ten cases and preserves quotes/semicolon',len(matrix)==10 and matrix[0]['caso']=='ORC-01' and '" Ana Lima "' in matrix[0]['entrada_ficticia'] and matrix[-1]['estado_ficticio']=='Não executado')
    page.locator('#search').fill('integração');page.wait_for_selector('.search-result')
    check('Search reaches new lessons',page.locator('.search-result[href="#aula/ciclo-integracoes"]').count()>0)
    page.goto(URL+'#glossario')
    check('Every glossary link points to an existing lesson',page.evaluate('window.LEAP.glossary.every(t=>window.LEAP.lessons.some(l=>l.slug===t[3]))'))
    check('No glossary links contain undefined',page.locator('main a[href*="undefined"]').count()==0)
    page.goto(URL+'#fontes')
    check('Source directory resolves external documentation',page.locator('main a[href^="https://docs.leapwork.com/best-practices/latest/"]').count()>=2)
    page.goto(URL+'#trilha')
    check('All five modules prepared',all('Planejado' not in page.locator('#modulo-'+str(i).zfill(2)).inner_text() for i in range(1,6)))
    for module in range(1,5):
        page.goto(URL+('#inicio' if module==1 else '#modulo/'+str(module)))
        check('Module 5 reachable from module '+str(module),page.locator('main .module-switch a[href="#modulo/5"]').count()>0)
    for theme in ['light','dark']:
        page.goto(URL+'#modulo/5')
        if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
        for width in [1440,768,390]:
            page.set_viewport_size({'width':width,'height':1000})
            check('Overview/labs fit '+theme+' '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000});page.screenshot(path=str(QA/f'module5-overview-{theme}.png'))
        page.locator('#m5-integration').scroll_into_view_if_needed();page.screenshot(path=str(QA/f'module5-lab-{theme}.png'))
        page.goto(URL+'#aula/ciclo-organizacao')
        for width in [1440,390]:
            page.set_viewport_size({'width':width,'height':1000})
            check('Illustrated lesson fits '+theme+' '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    check('No JavaScript errors',not errors)
    check('No external network requests',not any(u.startswith(('http://','https://')) for u in requests))
    browser.close()
(QA/'module5-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

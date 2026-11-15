"""Valida o módulo 4 offline, seus laboratórios e a preservação dos estudos anteriores."""
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
    page.evaluate("localStorage.setItem('leapwork-caderno-v1',JSON.stringify({completed:['primeiro-fluxo','dados-fundamentos'],notes:{'primeiro-fluxo':'Nota anterior Web','dados-fundamentos':'Nota anterior de dados'}}))")
    page.goto(URL+'#modulo/4')
    page.reload()
    page.wait_for_selector('.lesson-card')
    lessons=page.evaluate('window.LEAP.lessons.filter(l=>l.module===4)')
    check('16 documentation lessons, no fabricated video',len(lessons)==16 and all(not l.get('video') and l['sourceKind']=='documentation' for l in lessons))
    check('82 total lessons',page.evaluate('window.LEAP.lessons.length')==82)
    check('16 overview cards',page.locator('.lesson-card').count()==16)
    check('All nine core references mapped',page.locator('#cobertura .catalog-entry').count()==9)
    check('Existing module 1 notes preserved',page.evaluate("JSON.parse(localStorage.getItem('leapwork-caderno-v1')).notes['primeiro-fluxo']")=='Nota anterior Web')
    check('New progress starts at zero',page.locator('.progress-overview progress').get_attribute('value')=='0')
    page.locator('a[href="#modulo/4/tema-versoes"]').first.click()
    page.wait_for_function("document.activeElement.id==='tema-versoes'")
    check('Topic shortcut focuses target',page.locator('#tema-versoes').evaluate('(e)=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<innerHeight'))
    for lesson in lessons:
        slug=lesson['slug']
        page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('.quiz-form[data-lesson="'+slug+'"]')
        check('Module 4 back link: '+slug,page.locator('.back-link').get_attribute('href')=='#modulo/4')
        check('Four documented steps, no fabricated player: '+slug,page.locator('.step').count()==4 and page.locator('[data-video]').count()==0 and page.locator('.step-source a[href^="https://docs.leapwork.com/"]').count()==4)
        check('Two review questions: '+slug,len(lesson['quiz'])==2)
        for i,q in enumerate(lesson['quiz']):
            page.locator(f'input[name="q{i}"][value="{q["correct"]}"]').check()
        page.locator('.quiz-form button[type=submit]').click()
        check('Correct review with explanations: '+slug,'2 de 2' in page.locator('.quiz-feedback').inner_text() and all(q['why'] in page.locator('.quiz-form').inner_text() for q in lesson['quiz']))
        for image in page.locator('.step img').all():
            image.evaluate('(img)=>img.decode()')
            check('Referenced image loads: '+slug,image.evaluate('(img)=>img.naturalWidth>0'))
        for _,path in lesson['docs']:
            check('Cached documentation: '+slug+' / '+path,(ROOT/'research/docs'/(path.replace('/','__')+'.json')).is_file())
        check('No undefined labels: '+slug,'undefined' not in page.locator('main').inner_text())
    page.goto(URL+'#aula/controle-restauracao')
    page.locator('#lesson-notes').fill('Only Flow mantém os Locators atuais. <script>estudo</script>')
    page.locator('[data-complete]').click()
    page.reload()
    check('Notes persist safely as text',page.locator('#lesson-notes').input_value()=='Only Flow mantém os Locators atuais. <script>estudo</script>')
    check('Completion persists',page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    with page.expect_download() as download:
        page.locator('[data-export]').click()
    text=Path(download.value.path()).read_text(encoding='utf-8')
    check('Notes export includes old and new lessons','Nota anterior Web' in text and 'Nota anterior de dados' in text and 'Only Flow mantém' in text)
    page.goto(URL+'#modulo/4')
    check('Independent progress is one of sixteen',page.locator('.progress-overview progress').get_attribute('value')=='1' and page.locator('.progress-overview progress').get_attribute('max')=='16')
    old=page.evaluate("JSON.parse(localStorage.getItem('leapwork-caderno-v1'))")
    check('Previous completion preserved',all(s in old['completed'] for s in ['primeiro-fluxo','dados-fundamentos']))
    form=page.locator('#m4-distribution')
    for mode,total in [('each',8),('divide',4),('first',4)]:
        form.locator('select').select_option(mode)
        form.locator('button').click()
        check('Distribution result: '+mode,str(total)+' execuções planejadas' in page.locator('#m4-plan-output').inner_text())
    check('First available keeps other Agent unassigned','Agent 2: nenhum fluxo atribuído' in page.locator('#m4-plan-output').inner_text())
    form.locator('input[name=flows]').fill('0')
    check('Zero flows rejected',not form.evaluate('(f)=>f.checkValidity()'))
    form.locator('input[name=flows]').fill('4.5')
    check('Fractional flows rejected',not form.evaluate('(f)=>f.checkValidity()'))
    form.locator('input[name=flows]').fill('4')
    check('Unknown distribution rejected',page.evaluate("(()=>{try{window.LEAP.module4Plan(4,2,'invalid');return false}catch{return true}})()"))
    check('Divide covers each flow once including unequal groups',page.evaluate("JSON.stringify(window.LEAP.module4Plan(5,2,'divide').assignments.flat().sort())")=='[1,2,3,4,5]')
    restore=page.locator('#m4-restoration')
    for mode,expected,has_copy in [('only','lógica A / Locator B',False),('full','lógica A / Locator A',False),('copy','lógica B / Locator B',True),('only','lógica A / Locator B',False)]:
        restore.locator('select').select_option(mode)
        restore.locator('button').click()
        result=page.locator('#m4-restore-output').inner_text()
        check('Restoration starts from baseline: '+mode,expected in result and ('O fluxo atual foi preservado.' in result)==has_copy)
    page.locator('#m4-plan-notes').fill('Plano fictício <b>sem HTML</b>')
    with page.expect_download() as download:
        page.locator('[data-m4-export]').click()
    payload=json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
    check('Offline JSON worksheet uses current choices and literal notes',payload['kind']=='ficha-autoral-modulo4' and payload['plan']['total']==4 and payload['restoration']['mode']=='only' and payload['notes']=='Plano fictício <b>sem HTML</b>')
    page.locator('#search').fill('restauração')
    page.wait_for_selector('.search-result')
    check('Accent-aware search finds module 4',page.locator('.search-result[href="#aula/controle-restauracao"]').count()>0)
    page.goto(URL+'#glossario')
    check('New glossary terms available','Full Restore' in page.locator('main').inner_text())
    page.goto(URL+'#trilha')
    check('Module 4 prepared; only 5 planned','16 aulas' in page.locator('#modulo-04').inner_text() and 'Planejado' not in page.locator('#modulo-04').inner_text() and 'Planejado' in page.locator('#modulo-05').inner_text())
    for module in [1,2,3]:
        page.goto(URL+('#inicio' if module==1 else '#modulo/'+str(module)))
        check('Module 4 reachable from module '+str(module),page.locator('main .module-switch a[href="#modulo/4"]').count()>0)
    for theme in ['light','dark']:
        page.goto(URL+'#modulo/4')
        if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
        for width in [1440,768,390]:
            page.set_viewport_size({'width':width,'height':1000})
            check('Overview and labs fit '+theme+' '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
        page.screenshot(path=str(QA/f'module4-overview-{theme}.png'),full_page=True)
        page.goto(URL+'#aula/controle-restauracao')
        for width in [1440,390]:
            page.set_viewport_size({'width':width,'height':1000})
            check('Illustrated lesson fits '+theme+' '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
        page.screenshot(path=str(QA/f'module4-restoration-{theme}.png'),full_page=True)
    check('No runtime errors',not errors)
    check('Offline browsing makes no external requests',not any(u.startswith(('http://','https://')) for u in requests))
    browser.close()
(QA/'module4-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

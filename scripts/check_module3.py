"""Check source provenance, offline assets, lab contract and module isolation."""
import csv,json
from pathlib import Path
from openpyxl import load_workbook
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'research/qa'
URL=(ROOT/'site/index.html').as_uri()
passed,errors,requests=[],[],[]
def check(name,condition):
    assert condition,name
    passed.append(name)

book=load_workbook(ROOT/'site/assets/examples/modulo3-entradas.xlsx',data_only=True)
check('Workbook includes four fictional inputs',book['Casos'].max_row==5)
check('Input ID preserves leading zeros',book['Casos']['A2'].value=='001')
with (ROOT/'site/assets/examples/modulo3-esperados.csv').open(encoding='utf-8-sig') as f:
    expected=list(csv.DictReader(f,delimiter=';'))

with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda req:requests.append(req.url))
    page.goto(URL+'#modulo/3')
    page.wait_for_selector('.lesson-card')
    lessons=page.evaluate('window.LEAP.lessons.filter(l=>l.module===3)')
    check('19 lessons with one video and 18 documentation studies',len(lessons)==19 and sum(bool(l.get('video')) for l in lessons)==1)
    check('19 cards on module overview',page.locator('.lesson-card').count()==19)
    check('Coverage includes all 29 block references',page.locator('#cobertura .source-list li').count()==29)
    check('Source distinction disclosed','não uma coleção de 19 vídeos oficiais' in page.locator('aside.learning-note').inner_text())
    check('No undefined source labels','undefined' not in page.locator('main').inner_text())
    page.locator('a[href="#modulo/3/tema-estado"]').first.click()
    page.wait_for_function("document.activeElement.id==='tema-estado'")
    check('Module section shortcut focuses its target',page.locator('#tema-estado').evaluate('(e)=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<innerHeight'))
    for l in lessons:
        slug=l['slug'];page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('.quiz-form[data-lesson="'+slug+'"]')
        check('Back link returns to module 3: '+slug,page.locator('.back-link').get_attribute('href')=='#modulo/3')
        if not l.get('video'):
            check('Documentation study has no fabricated player or timestamps: '+slug,page.locator('[data-video]').count()==0 and 'Esta aula não tem um vídeo específico' in page.locator('#passos').inner_text())
            check('Official documentation link on every step: '+slug,page.locator('.step-source a[href^="https://docs.leapwork.com/"]').count()==len(l['steps']))
        for i,q in enumerate(l['quiz']):page.locator(f'input[name="q{i}"][value="{q["correct"]}"]').check()
        page.locator('.quiz-form button[type=submit]').click()
        check('Review answers and explanation: '+slug,'2 de 2' in page.locator('.quiz-feedback').inner_text())
        for image in page.locator('.step img').all():
            image.scroll_into_view_if_needed();image.evaluate('(img)=>img.decode()')
        check('Step images load: '+slug,page.locator('.step img').evaluate_all('(imgs)=>imgs.every(i=>i.naturalWidth>0)'))
        if not l.get('video'):
            check('Documentation images preserve native aspect ratio: '+slug,page.locator('.documentation-figure img').evaluate_all('(imgs)=>imgs.every(i=>Math.abs(i.getBoundingClientRect().width/i.getBoundingClientRect().height-i.naturalWidth/i.naturalHeight)<0.01)'))
        page.set_viewport_size({'width':390,'height':844})
        check('Mobile study does not overflow: '+slug,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
    page.goto(URL+'#aula/dados-laboratorio')
    page.wait_for_selector('[data-lab-run]')
    page.locator('[data-lab-run]').click()
    check('Default dataset accepts three and rejects one','3 aceitos e 1 rejeitados' in page.locator('.lab-summary').inner_text())
    for row in expected:
        actual=page.evaluate('(id)=>window.LEAP.runDataLab(window.LEAP.module3Rows.find(r=>r.id===id))',row['ID'])
        check('Lab agrees with independent expected CSV: '+row['ID'],actual['status']==row['Status'] and actual['nome']==row['NomeNormalizado'] and (str(actual['totalCentavos']) if actual['totalCentavos'] is not None else '')==row['TotalCentavos'])
    check('Midpoint rounding uses nearest even',page.evaluate("window.LEAP.runDataLab({id:'x',nome:'Teste',quantidade:'1',preco:'0,30',grupo:'BASICO'}).totalCentavos")==28)
    row=page.locator('[data-lab-row="001"]')
    row.locator('[data-lab-field="preco"]').fill('1.234,56');page.locator('[data-lab-run]').click()
    check('Unsupported thousands format rejected',row.get_attribute('data-lab-status')=='REJEITADO')
    page.locator('[data-lab-reset]').click()
    row.locator('[data-lab-field="quantidade"]').fill('1.5');page.locator('[data-lab-run]').click()
    check('Fractional quantity rejected',row.get_attribute('data-lab-status')=='REJEITADO')
    page.locator('[data-lab-reset]').click()
    row.locator('[data-lab-field="grupo"]').fill('DESCONHECIDO');page.locator('[data-lab-run]').click()
    check('Unknown group rejected',row.get_attribute('data-lab-status')=='REJEITADO')
    page.locator('[data-lab-reset]').click()
    row.locator('[data-lab-field="nome"]').fill('<script>teste</script>');page.locator('[data-lab-run]').click()
    check('Input rendered as text rather than HTML','<script>' in row.locator('[data-lab-output="motivo"]').inner_text() and row.locator('script').count()==0)
    page.locator('[data-lab-reset]').click()
    check('Reset restores original values and status',row.locator('[data-lab-field="nome"]').input_value()==' Ana Lima ' and row.locator('[data-lab-output="status"]').inner_text()=='Aguardando')
    for link in page.locator('.data-lab a[download]').all():
        with page.expect_download() as pending:link.click()
        download=pending.value
        check('Download available: '+download.suggested_filename,download.failure() is None)
        saved=QA/('download-'+download.suggested_filename);download.save_as(saved)
        check('Offline download matches original file: '+download.suggested_filename,saved.read_bytes()==(ROOT/'site/assets/examples'/download.suggested_filename).read_bytes())
    page.locator('#lesson-notes').fill('Conferir tipos e arredondamento antes de gravar.')
    page.locator('[data-complete]').click();page.reload()
    check('New notes and completion survive reload',page.locator('#lesson-notes').input_value()=='Conferir tipos e arredondamento antes de gravar.' and page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    page.goto(URL+'#modulo/3');page.wait_for_selector('.progress-meter')
    check('Module 3 progress is 1 of 19','1 de 19 revisadas' in page.locator('.progress-meter').inner_text())
    page.goto(URL+'#modulo/2');page.wait_for_selector('.progress-meter')
    check('Module 2 progress is unchanged','0 de 32 revisadas' in page.locator('.progress-meter').inner_text())
    page.goto(URL+'#inicio');page.wait_for_selector('.progress-meter')
    check('Module 1 progress is unchanged','0 de 15 revisadas' in page.locator('.progress-meter').inner_text())
    page.goto(URL+'#buscar/escopo');page.wait_for_selector('.search-result')
    check('Search finds new variable lesson',page.locator('.search-result[href*="dados-variaveis"]').count()>0)
    page.goto(URL+'#aula/dados-fundamentos');page.wait_for_selector('[data-animation]')
    check('New GIF starts paused',page.locator('[data-animation]').get_attribute('aria-pressed')=='false')
    page.locator('[data-animation]').click();page.locator('figure.is-playing img').evaluate('(img)=>img.decode()')
    check('New GIF loads on request',page.locator('[data-animation]').get_attribute('aria-pressed')=='true')
    page.locator('[data-animation]').click()
    page.locator('.step [data-video][data-time="26"]').click()
    page.wait_for_function("document.getElementById('local-video').readyState>=2&&document.getElementById('local-video').currentTime>=25",timeout=30000)
    check('Intro video seeks to linked time',page.locator('#local-video').evaluate('(v)=>v.videoWidth')>0)
    page.locator('#close-video').click()
    for theme in ['light','dark']:
        page.goto(URL+'#modulo/3');page.wait_for_selector('.lesson-card')
        if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
        for width in [1440,768,390]:
            page.set_viewport_size({'width':width,'height':1000})
            check('Overview fits '+theme+' '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000});page.screenshot(path=str(QA/f'module3-overview-{theme}.png'))
        page.goto(URL+'#aula/dados-variaveis');page.wait_for_selector('.documentation-figure')
        page.locator('#passo-1').scroll_into_view_if_needed();page.locator('#passo-1 img').evaluate('(img)=>img.decode()')
        page.screenshot(path=str(QA/f'module3-doc-{theme}.png'))
        page.goto(URL+'#modulo/3/laboratorio');page.wait_for_selector('[data-lab-run]')
        page.locator('[data-lab-run]').click();page.screenshot(path=str(QA/f'module3-lab-{theme}.png'))
    check('Site stays offline without external requests',not any(u.startswith(('https://','http://')) for u in requests))
    check('No runtime errors',not errors)
    browser.close()
(QA/'module3-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

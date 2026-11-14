"""Validate the complete collection through the local site's user flows."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'research/qa'
URL=(ROOT/'site/index.html').as_uri()
passed,errors=[],[]
def check(name,ok):
    assert ok,name
    passed.append(name)

with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.goto(URL+'#modulo/2')
    page.wait_for_selector('.lesson-card')
    lessons=page.evaluate('window.LEAP.lessons.filter(l=>l.module===2)')
    catalog=page.evaluate('window.LEAP.testingInternet')
    check('32 lessons with distinct source videos',len(lessons)==len({l['video'] for l in lessons})==32)
    check('29 official web videos all mapped to local content',len(catalog)==29 and all(any(l['slug']==v['slug'] and l['video']==v['id'] for l in lessons) for v in catalog))
    check('All 32 lessons occur exactly once in topic sections',page.locator('.module-section .lesson-card').count()==32)
    check('Lesson numbers unique and sequential',[int(l['number']) for l in lessons]==list(range(1,33)))
    check('No remaining pending adaptation message','adaptação local pendente' not in page.locator('main').inner_text())
    page.locator('a[href="#modulo/2/tema-dom"]').first.click()
    page.wait_for_function("document.activeElement.id==='tema-dom'")
    check('Topic shortcut reaches DOM group',page.locator('#tema-dom').evaluate('(e)=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<innerHeight'))
    new_ids={v['id'] for v in catalog[3:]}
    for l in [l for l in lessons if l['video'] in new_ids]:
        slug=l['slug']
        check('Source captions available: '+slug,(ROOT/'videos'/f'{l["video"]}.en-orig.vtt').exists())
        page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('.quiz-form[data-lesson="'+slug+'"]')
        for i,question in enumerate(l['quiz']):
            page.locator(f'input[name="q{i}"][value="{question["correct"]}"]').check()
        page.locator('.quiz-form button[type=submit]').click()
        check('Review answers and feedback: '+slug,'2 de 2' in page.locator('.quiz-feedback').inner_text())
        for control in page.locator('[data-animation]').all():
            check('Animation stopped initially: '+slug,control.get_attribute('aria-pressed')=='false')
            control.click()
            page.locator('figure.is-playing img').evaluate('(img)=>img.decode()')
            check('Animation loads on request: '+slug,control.get_attribute('aria-pressed')=='true')
            control.click()
            check('Animation restores still frame: '+slug,page.locator('figure.is-playing').count()==0)
        sec=l['steps'][0]['time']
        page.locator('.step [data-video]').first.click()
        page.wait_for_function('(sec)=>{const v=document.getElementById("local-video");return v.readyState>=2&&v.currentTime>=sec-1}',arg=sec,timeout=30000)
        check('Local video opens at step timestamp: '+slug,page.locator('#local-video').evaluate('(v)=>v.videoWidth>=640'))
        page.locator('#close-video').click()
        page.set_viewport_size({'width':390,'height':844})
        check('Mobile article stays within viewport: '+slug,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
    for slug in ['dropdowns-avancados','tabela-ordenavel']:
        page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('aside.learning-note')
        check('Source discrepancy disclosed: '+slug,'Failed' in page.locator('aside.learning-note').inner_text())
    page.goto(URL+'#aula/variacoes-texto')
    page.wait_for_selector('#lesson-notes')
    page.locator('#lesson-notes').fill('Localizar a região não aprova sua ortografia.')
    page.locator('[data-complete]').click()
    page.reload()
    check('New lesson notes and completion persist',page.locator('#lesson-notes').input_value()=='Localizar a região não aprova sua ortografia.' and page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    page.goto(URL+'#modulo/2')
    page.wait_for_selector('.progress-meter')
    check('Full module progress counts new lesson','1 de 32 revisadas' in page.locator('.progress-meter').inner_text())
    page.goto(URL+'#buscar/visibilidade')
    page.wait_for_selector('.search-result')
    check('Search finds new loading lesson',page.locator('.search-result[href*="carregamento-visibilidade"]').count()>0)
    for theme,slug in [('light','hover-elementos'),('dark','tabela-ordenavel')]:
        page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('.step')
        if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
        step=page.locator('#passo-4')
        step.scroll_into_view_if_needed()
        step.locator('img').evaluate('(img)=>img.decode()')
        page.screenshot(path=str(QA/f'module2-complete-{theme}.png'))
    check('No runtime errors',not errors)
    browser.close()
(QA/'module2-completion-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

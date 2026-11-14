"""Check source coverage, new local media and progress across the module boundary."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'research' / 'qa'
URL = (ROOT / 'site' / 'index.html').as_uri()
passed, errors = [], []

def check(name, condition):
    assert condition, name
    passed.append(name)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width':1440,'height':1000}, reduced_motion='reduce')
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_selector('.lesson-card')
    lessons = page.evaluate('window.LEAP.lessons.filter(l=>l.module===1)')
    check('Module 1 has fifteen distinct lesson videos', len(lessons)==len({l['video'] for l in lessons})==15)
    for group, count in [('web',6),('desktop',3),('virtual',6)]:
        check('Home section: '+group,page.locator('#'+group+' .lesson-card').count()==count)
    sources=json.loads((ROOT/'research/module1-sources.json').read_text(encoding='utf-8'))
    check('All nine official additions are represented',all(any(l['slug']==s['slug'] and l['video']==s['video'] for l in lessons) for s in sources))
    page.locator('.module-switch a[href="#inicio/virtual"]').click()
    page.wait_for_function("document.activeElement.id==='virtual'")
    check('Section link scrolls and focuses Virtual',page.locator('#virtual').evaluate('(e)=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<innerHeight'))
    for source in sources:
        slug=source['slug']
        page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('.quiz-form[data-lesson="'+slug+'"]')
        lesson=next(l for l in lessons if l['slug']==slug)
        for i,q in enumerate(lesson['quiz']):
            page.locator(f'input[name="q{i}"][value="{q["correct"]}"]').check()
        page.locator('.quiz-form button[type=submit]').click()
        check('Quiz and explanation: '+slug,'2 de 2' in page.locator('.quiz-feedback').inner_text())
        for control in page.locator('[data-animation]').all():
            check('Animation starts paused: '+slug,control.get_attribute('aria-pressed')=='false')
            control.click()
            page.wait_for_function("document.querySelector('figure.is-playing img').complete&&document.querySelector('figure.is-playing img').naturalWidth>0")
            check('Animation can start: '+slug,control.get_attribute('aria-pressed')=='true')
            control.click()
            check('Animation can stop: '+slug,control.get_attribute('aria-pressed')=='false')
        first=lesson['steps'][0]['time']
        page.locator(f'.step [data-video="{slug}"]').first.click()
        page.wait_for_function('(sec)=>{let v=document.getElementById("local-video");return v.readyState>=2&&v.currentTime>=sec-1}',arg=first,timeout=30000)
        check('Local video opens at linked time: '+slug,page.locator('#local-video').evaluate('(v)=>v.videoWidth>0'))
        page.locator('#close-video').click()
        page.set_viewport_size({'width':390,'height':844})
        check('Mobile has no horizontal overflow: '+slug,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':1440,'height':1000})
    page.goto(URL+'#aula/desktop-contatos')
    page.wait_for_selector('#lesson-notes')
    page.locator('#lesson-notes').fill('Conferir Completed antes de Pass.')
    page.locator('[data-complete]').click()
    page.reload()
    check('New lesson notes and completion persist',page.locator('#lesson-notes').input_value()=='Conferir Completed antes de Pass.' and page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    page.goto(URL+'#inicio')
    page.wait_for_selector('.progress-meter')
    check('Full module progress includes desktop','1 de 15 revisadas' in page.locator('.progress-meter').inner_text())
    page.goto(URL+'#modulo/2')
    page.wait_for_selector('.progress-meter')
    check('Module 2 progress stays independent','0 de 32 revisadas' in page.locator('.progress-meter').inner_text())
    page.goto(URL+'#buscar/Offset Position')
    page.wait_for_selector('.search-result')
    check('Search finds virtual content',page.locator('.search-result[href*="virtual-areas"]').count()>0)
    for theme,slug in [('light','desktop-contatos'),('dark','virtual-areas')]:
        page.goto(URL+'#aula/'+slug)
        page.wait_for_selector('.step')
        if page.evaluate('document.documentElement.dataset.theme') != theme:
            page.locator('#theme-toggle').click()
        page.locator('#passo-5').scroll_into_view_if_needed()
        page.locator('#passo-5 img').evaluate('(img)=>img.decode()')
        page.screenshot(path=str(QA/('module1-'+theme+'.png')))
    check('No JavaScript runtime errors',not errors)
    context.close()
    browser.close()
(QA/'module1-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors}))

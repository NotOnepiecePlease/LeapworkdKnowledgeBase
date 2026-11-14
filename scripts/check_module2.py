"""Check module navigation, backward-compatible notes and opt-in animations."""
import json
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'research' / 'qa'
URL = (ROOT / 'site' / 'index.html').as_uri()
passed, errors = [], []

def check(name, condition):
    assert condition, name
    passed.append(name)

for clip in json.loads((ROOT / 'research' / 'animations-manifest.json').read_text(encoding='utf-8')):
    with Image.open(ROOT / 'site' / 'assets' / 'animations' / clip['file']) as image:
        check('Animated GIF contains multiple frames: '+clip['file'], image.n_frames > 1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width':1440,'height':1000}, reduced_motion='reduce')
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    gif_requests = []
    page.on('request', lambda request: gif_requests.append(request.url) if '.gif' in request.url else None)
    def go(route):
        page.goto(URL+route)
        if route.startswith('#aula/'):
            page.wait_for_selector('.quiz-form[data-lesson="'+route.split('/')[1]+'"]')
        elif route.startswith('#modulo/2'):
            page.wait_for_function("document.title.startsWith('Módulo 2')")
        else:
            page.wait_for_selector('.hero')
    page.goto(URL)
    page.evaluate("localStorage.setItem('leapwork-caderno-v1', JSON.stringify({completed:['primeiro-fluxo'],notes:{'primeiro-fluxo':'Anotação preservada da versão anterior.'}}))")
    page.reload()
    page.locator('.module-switch a[href="#modulo/2"]').click()
    page.wait_for_function("document.title.startsWith('Módulo 2')")
    check('Module 2 has 32 lesson cards', page.locator('.lesson-card').count()==32)
    check('Module 2 has separate initial progress', '0 de 32 revisadas' in page.locator('.progress-meter').inner_text())
    page.locator('.catalog-details summary').click()
    check('All 29 official examples have local lessons', page.locator('.catalog-details li').count()==29 and page.evaluate('window.LEAP.testingInternet.every(v=>v.slug&&window.LEAP.lessons.some(l=>l.slug===v.slug&&l.video===v.id))'))
    page.locator('.catalog-details summary').click()
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(QA/'modulo2-desktop.png'),full_page=True)
    check('Module 2 has no horizontal overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    go('#aula/primeiro-fluxo')
    check('Old notes survive the module expansion', page.locator('#lesson-notes').input_value()=='Anotação preservada da versão anterior.')
    check('Old progress survives the module expansion', page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    check('GIF is not fetched before user action', len(gif_requests)==0)
    check('Replaced login frame is the clear Password configuration', page.locator('#passo-3 img').get_attribute('src').endswith('-155.jpg'))
    for slug in ['primeiro-fluxo','dom-avancado','strategy-desktop','campos-dinamicos','transferencia-desktop']:
        go('#aula/'+slug)
        button=page.locator('[data-animation]')
        check('Animation starts stopped: '+slug,button.get_attribute('aria-pressed')=='false')
        button.click()
        check('Animation starts on request: '+slug,button.get_attribute('aria-pressed')=='true')
        image=page.locator('figure.is-playing img')
        image.evaluate('(img)=>img.decode()')
        check('GIF loads correctly: '+slug,image.get_attribute('src').endswith('.gif'))
        button.click()
        check('Stop restores the still image: '+slug,page.locator('figure.is-playing').count()==0 and page.locator('[data-animation]').get_attribute('aria-pressed')=='false')
    go('#aula/campos-dinamicos')
    page.locator('[data-complete]').click()
    page.reload()
    check('Module 2 progress persists',page.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    go('#modulo/2')
    check('Module 2 progress counts only its lessons','1 de 32 revisadas' in page.locator('.progress-meter').inner_text())
    go('#inicio')
    check('Module 1 progress excludes module 2','1 de 15 revisadas' in page.locator('.progress-meter').inner_text())
    page.locator('#search').fill('campo dinâmico')
    page.wait_for_selector('.search-result')
    check('Search includes module 2 lessons',page.locator('.search-result[href*="campos-dinamicos"]').count()>0)
    go('#aula/transferencia-desktop')
    page.locator('[data-video][data-time="580"]').click()
    page.wait_for_function("document.getElementById('local-video').readyState >= 2 && document.getElementById('local-video').currentTime >= 579",timeout=20000)
    check('New local desktop video seeks to the chosen moment',page.locator('#local-video').evaluate('(v)=>v.currentTime')>=579)
    page.locator('#close-video').click()
    go('#aula/primeiro-fluxo/passo-3')
    page.locator('#passo-3').screenshot(path=str(QA/'login-com-animacao.png'))
    page.set_viewport_size({'width':390,'height':844})
    go('#modulo/2')
    check('Mobile module 2 does not overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    page.screenshot(path=str(QA/'modulo2-mobile.png'),full_page=True)
    go('#aula/campos-dinamicos')
    check('Mobile animation lesson does not overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    check('No runtime JavaScript errors',not errors)
    context.close()
    browser.close()

(QA/'module2-report.json').write_text(json.dumps({'passed':passed,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(passed),'errors':errors},ensure_ascii=False))

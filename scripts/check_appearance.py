"""Verify both palettes, reading sizes, preference persistence and responsive layout."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'research' / 'qa'
URL = (ROOT / 'site' / 'index.html').as_uri()
checks, errors = [], []

def check(name, result):
    assert result, name
    checks.append(name)

def luminance(color):
    values=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(v*w for v,w in zip(values,[.2126,.7152,.0722]))

def contrast(a,b):
    high,low=sorted([luminance(a),luminance(b)],reverse=True)
    return (high+.05)/(low+.05)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1600,'height':1050},reduced_motion='reduce')
    page=context.new_page()
    page.on('pageerror',lambda err:errors.append(str(err)))
    requests=[]
    page.on('request',lambda req:requests.append(req.url))
    page.goto(URL+'#aula/dom-avancado')
    page.wait_for_selector('.quiz-form[data-lesson="dom-avancado"]')
    page.evaluate('document.fonts.ready')
    check('Manrope available offline',page.evaluate('document.fonts.check("400 18px Manrope")'))
    check('Outfit available offline',page.evaluate('document.fonts.check("500 24px Outfit")'))
    check('Body uses Manrope', 'Manrope' in page.locator('.step-description').first.evaluate('(e)=>getComputedStyle(e).fontFamily'))
    check('Main lesson text is 18px',page.locator('.step-description').first.evaluate('(e)=>getComputedStyle(e).fontSize')=='18px')
    check('Section spacing is at least 64px',page.locator('.reading-section').first.evaluate('(e)=>parseFloat(getComputedStyle(e).marginBottom)')>=64)
    check('Steps have 32px separation',page.locator('.steps').evaluate('(e)=>getComputedStyle(e).gap')=='32px')
    page.locator('#lesson-notes').fill('Nota preservada durante a troca de tema.')
    for theme in ['light','dark']:
        if page.locator('html').get_attribute('data-theme')!=theme:
            page.locator('#theme-toggle').click()
        check('Toggle selects '+theme,page.locator('html').get_attribute('data-theme')==theme)
        page.reload()
        page.wait_for_selector('.quiz-form[data-lesson="dom-avancado"]')
        page.evaluate('document.fonts.ready')
        check('Theme persists on reload: '+theme,page.locator('html').get_attribute('data-theme')==theme)
        check('Notes survive theme change: '+theme,page.locator('#lesson-notes').input_value()=='Nota preservada durante a troca de tema.')
        palette=page.evaluate("Object.fromEntries(['--text','--subtle','--surface','--bg','--accent','--tint'].map(k=>[k,getComputedStyle(document.documentElement).getPropertyValue(k).trim()]))")
        check('Main text contrast meets 4.5:1: '+theme,contrast(palette['--text'],palette['--surface'])>=4.5)
        check('Secondary text contrast meets 4.5:1: '+theme,contrast(palette['--subtle'],palette['--surface'])>=4.5)
        check('Accent text contrast meets 4.5:1: '+theme,contrast(palette['--accent'],palette['--tint'])>=4.5)
        page.locator('#passos').scroll_into_view_if_needed()
        page.screenshot(path=str(QA/('leitura-'+theme+'.png')))
        page.goto(URL+'#inicio')
        page.wait_for_selector('.hero')
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(QA/('inicio-'+theme+'.png')),full_page=True)
        for width in [1905,1280,768,390]:
            page.set_viewport_size({'width':width,'height':1000})
            check('No horizontal overflow on home: '+theme+' '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.goto(URL+'#aula/dom-avancado')
        page.wait_for_selector('.quiz-form[data-lesson="dom-avancado"]')
        check('Mobile article stays at 17px: '+theme,page.locator('.step-description').first.evaluate('(e)=>getComputedStyle(e).fontSize')=='17px')
        check('No horizontal overflow on mobile article: '+theme,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.locator('#passo-2').scroll_into_view_if_needed()
        page.screenshot(path=str(QA/('leitura-mobile-'+theme+'.png')))
        page.set_viewport_size({'width':1600,'height':1050})
    check('No external font or other external requests',not any(u.startswith(('http://','https://')) for u in requests))
    check('No JavaScript runtime errors',not errors)
    context.close()
    system_context=browser.new_context(color_scheme='dark')
    system_page=system_context.new_page()
    system_page.goto(URL)
    system_page.wait_for_selector('.hero')
    check('Uses system dark theme before a manual choice',system_page.locator('html').get_attribute('data-theme')=='dark')
    system_context.close()
    browser.close()
(QA/'appearance-report.json').write_text(json.dumps({'passed':checks,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(checks),'errors':errors},ensure_ascii=False))

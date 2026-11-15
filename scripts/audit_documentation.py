"""Inventaria toda a navegação de Leapwork Flow/latest e consulta os artigos públicos."""
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://docs.leapwork.com'
PREFIX='/leapwork-flow/latest/'
CACHE=ROOT/'.publication/docs-crawl'
TREE_URL=ORIGIN+PREFIX+'__pagetree.json'


def normalize(url):
    parts=urlsplit(urljoin(ORIGIN,url))
    if parts.hostname!='docs.leapwork.com' or not parts.path.startswith(PREFIX):return None
    path=parts.path.rstrip('/')
    if '__' in path or path.endswith(('.json','.png','.jpg','.pdf','.zip')):return None
    return ORIGIN+path


def request(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url,headers={'User-Agent':'LeapworkKnowledgeBase/1.3 documentation study audit'}),timeout=35) as response:
                return response.read(),response.url,response.status
        except Exception:
            if attempt==2:raise
            time.sleep(0.5*(attempt+1))


def collect(url):
    key=hashlib.sha256(url.encode()).hexdigest()[:20]
    dest=CACHE/(key+'.json')
    if dest.exists():return json.loads(dest.read_text(encoding='utf-8'))
    record={'url':url,'retrievedAt':datetime.now(timezone.utc).isoformat()}
    try:
        raw,actual,status=request(url)
        soup=BeautifulSoup(raw,'html.parser')
        content=soup.select_one('.article-body')
        if content is None:raise ValueError('Article body unavailable')
        title=soup.select_one('article h1') or soup.find('h1')
        record.update(title=title.get_text(' ',strip=True) if title else url.rsplit('/',1)[-1],status='read',httpStatus=status,canonicalUrl=actual)
        for x in content.select('script,style'):x.decompose()
        record['text']=content.get_text('\n',strip=True)
        record['headings']=[x.get_text(' ',strip=True) for x in content.select('h2,h3,h4')]
        record['links']=[{'title':a.get_text(' ',strip=True),'url':urljoin(actual,a['href'])} for a in content.select('a[href]')]
        tokens=[]
        for x in content.descendants:
            if isinstance(x,Tag) and x.name=='img':tokens.append(('image',{'alt':x.get('alt',''),'url':urljoin(actual,x.get('src',''))}))
            elif isinstance(x,NavigableString) and str(x).strip():tokens.append(('text',str(x).strip()))
        images=[]
        for i,(kind,value) in enumerate(tokens):
            if kind=='image':
                before=' '.join(v for k,v in tokens[:i] if k=='text')[-650:]
                after=' '.join(v for k,v in tokens[i+1:] if k=='text')[:280]
                images.append({**value,'index':len(images),'before':before,'after':after})
        record['images']=images
        record['wordCount']=len(record['text'].split())
        record['sha256']=hashlib.sha256(raw).hexdigest()
    except Exception as error:record.update(status='unavailable',error=f'{type(error).__name__}: {error}',links=[],images=[])
    dest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return record


def main():
    CACHE.mkdir(parents=True,exist_ok=True)
    raw,_,_=request(TREE_URL)
    tree=json.loads(raw)
    (ROOT/'research/documentation-navigation.json').write_text(json.dumps(tree,ensure_ascii=False,indent=2),encoding='utf-8')
    nodes={}
    def visit(node,section,parent=None):
        url=normalize(node['path'])
        if url:nodes[url]={'title':node['title'],'section':section,'parent':parent,'inNavigation':True}
        for child in node.get('children',[]):visit(child,section,url)
    for node in tree:visit(node,node['title'])
    queue=list(nodes);results={}
    while queue:
        batch=queue[:32];queue=queue[32:]
        with ThreadPoolExecutor(max_workers=4) as pool:
            for future in as_completed({pool.submit(collect,url):url for url in batch}):
                record=future.result();url=record['url'];results[url]=record
                for link in record['links']:
                    linked=normalize(link['url'])
                    if linked and linked not in nodes:
                        section=next((n['title'] for n in tree if urlsplit(linked).path.startswith(n['path'])),nodes[url]['section'])
                        nodes[linked]={'title':link['title'] or linked.rsplit('/',1)[-1],'section':section,'parent':url,'inNavigation':False};queue.append(linked)
        print(json.dumps({'consulted':len(results),'queued':len(queue),'found':len(nodes),'unavailable':sum(r['status']!='read' for r in results.values())}),flush=True)
    inventory=[]
    for url,meta in nodes.items():
        record=results[url]
        inventory.append({**meta,'url':url,'title':record.get('title') or meta['title'],'status':record['status'],'retrievedAt':record['retrievedAt'],'wordCount':record.get('wordCount',0),'images':len(record['images']),'headings':record.get('headings',[]),'error':record.get('error'),'cacheFile':str((CACHE/(hashlib.sha256(url.encode()).hexdigest()[:20]+'.json')).relative_to(ROOT)).replace('\\','/')})
    report={'scope':ORIGIN+PREFIX,'navigationSource':TREE_URL,'navigationPages':sum(p['inNavigation'] for p in inventory),'pagesFound':len(inventory),'pagesRead':sum(p['status']=='read' for p in inventory),'unavailable':sum(p['status']!='read' for p in inventory),'completedAt':datetime.now(timezone.utc).isoformat(),'pages':inventory}
    (ROOT/'research/documentation-inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='pages'}),flush=True)


if __name__=='__main__':main()

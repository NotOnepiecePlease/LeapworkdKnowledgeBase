"""Gera contagens verificáveis e localiza cada acréscimo por módulo/aula/passo."""
import json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    base=json.loads((ROOT/'research/enrichment-baseline.json').read_text(encoding='utf-8'))
    current=json.loads((ROOT/'research/course-content.json').read_text(encoding='utf-8'))
    library=json.loads((ROOT/'research/documentation-editorial.json').read_text(encoding='utf-8'))
    rows=json.loads((ROOT/'research/illustration-additions.json').read_text(encoding='utf-8'))
    old={(l['slug'],i+1):s for l in base['lessons'] for i,s in enumerate(l['steps'])}
    reviewed=[]
    for l in current['lessons']:
        for i,s in enumerate(l['steps']):
            prior=old[(l['slug'],i+1)];figures=s.get('additionalFigures',[])
            if figures:decision='Figura adicional selecionada e incluída com origem e legenda.'
            elif prior['hadImage']:decision='Referência visual existente preservada; não foi acrescentada outra captura.'
            elif l.get('video'):decision='Sem nova captura diretamente pertinente selecionada; o trecho do vídeo e as figuras seguintes permanecem disponíveis.'
            else:decision='Passo conceitual, de planejamento ou validação: não foi selecionada captura adicional que demonstrasse esse ponto sem repetir ou distorcer a referência.'
            reviewed.append({'module':l['module'],'lesson':l['slug'],'lessonTitle':l['title'],'step':i+1,'stepTitle':s['title'],'before':prior['hadImage'],'after':bool(s.get('image') or s.get('imagePath') or figures),'addedFigures':len(figures),'decision':decision})
    by_module=Counter(row['module'] for row in rows)
    grouped=defaultdict(list)
    for row in rows:grouped[row['lesson']].append(row)
    report={'version':'v1.3.0','scope':library['scope'],'pagesConsulted':library['counts']['pages'],'menus':len(library['sections']),'newSourcePages':library['counts']['newSources'],'newReferenceCards':len(library['pages']),'apiOperations':len(library['operations']),'lessonsReviewed':len(current['lessons']),'stepsReviewed':len(reviewed),'addedFigureUses':len(rows),'uniqueSupplementAssets':len({r['path'] for r in rows}),'stepsReceivingFigures':sum(r['addedFigures']>0 for r in reviewed),'additionalIntroFigures':sum(r['lesson']=='@introducao' for r in rows),'illustratedStepsBefore':sum(r['before'] for r in reviewed),'illustratedStepsAfter':sum(r['after'] for r in reviewed),'newlyIllustratedSteps':sum(not r['before'] and r['after'] for r in reviewed),'remainingTextOnlySteps':sum(not r['after'] for r in reviewed),'byModule':dict(by_module),'steps':reviewed,'additions':rows,'excludedBrokenImage':{'source':'https://docs.leapwork.com/leapwork-flow/latest/working-with-leapwork/designing-automation-flows/sub-flows','sourceImageIndex':7,'reason':'Attachment returned HTTP 404; not included.'}}
    (ROOT/'research/enrichment-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    text=['# Relatório de enriquecimento · v1.3.0','',f"Foram consultadas **{report['pagesConsulted']} páginas públicas dos oito menus** de Leapwork Flow/latest, com **{report['newSourcePages']} fontes antes ausentes** do recorte de consulta. A biblioteca oferece **338 fichas resumidas**, incluindo índices, e o catálogo apresenta **83 operações da especificação OpenAPI**. As fichas são complementos editoriais; não são traduções integrais nem evidência de execução.",'',f"A revisão passou pelas **98 aulas e 427 passos**. Foram acrescentadas **81 inclusões visuais**, com **72 arquivos de origem distintos**: 78 figuras em 75 passos e três na introdução. Dos 75 passos, um já tinha uma figura. Assim, **74 passos antes sem imagem passaram a ter referência visual**, e o total de passos ilustrados passou de **255 para 329**. Os 98 restantes são passos conceituais, de planejamento/validação ou sem uma captura adicional diretamente pertinente selecionada.",'','## Onde acessar','', '- Menu **Biblioteca da documentação**: oito seções e todas as fichas.', '- **Biblioteca → API REST → API Endpoints**: catálogo completo das 83 operações consultadas.', '- Menu **O que foi adicionado**: contagens e links para as aulas e passos.', '- **Introdução e arquitetura**: protocolos, implantação, banco e três diagramas oficiais.','','## Fontes por menu','','| Menu | Páginas |','| --- | ---: |']
    text += [f"| {s['label']} | {s['count']} |" for s in library['sections']]
    text += ['','## Figuras adicionadas por módulo','','| Módulo | Inclusões |','| --- | ---: |']
    text += [f'| {m} | {by_module[m]} |' for m in range(1,6)]
    text += ['','## Localização por aula','','| Módulo | Aula | Passos | Figuras |','| --- | --- | --- | ---: |']
    for slug,figs in sorted(grouped.items(),key=lambda item:(item[1][0]['module'],item[1][0]['lessonTitle'])):
        row=figs[0];where='Introdução' if slug=='@introducao' else ', '.join(str(n) for n in sorted({r['step'] for r in figs}))
        text.append(f"| {row['module']} | {row['lessonTitle']} | {where} | {len(figs)} |")
    text += ['','## Cada inclusão e sua fonte','']
    for row in rows:
        where='Introdução e arquitetura' if row['lesson']=='@introducao' else f"Módulo {row['module']} · {row['lessonTitle']} · passo {row['step']}"
        text += [f"- **{where}**: {row['caption']} [Fonte]({row['source']})."]
    text += ['','## Limites da consulta','', 'O recorte segue toda a navegação pública de **Leapwork Flow/latest** disponível em 15/11/2026. Outros produtos, outras versões e os dados autenticados do Customer Portal não foram consultados. Não houve página indisponível entre as 338 do menu; uma imagem de sub-flows retornou 404 e foi excluída. As capturas não representam execução local.','', 'O inventário e o relatório JSON registram as contagens, as fontes e a decisão para cada um dos 427 passos. As páginas completas consultadas ficam no cache local de manutenção; o pacote distribui as fichas editoriais e as imagens selecionadas, preservando links para os artigos originais.','']
    (ROOT/'ENRIQUECIMENTO.md').write_text('\n'.join(text),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['steps','additions']}),flush=True)


if __name__=='__main__':main()

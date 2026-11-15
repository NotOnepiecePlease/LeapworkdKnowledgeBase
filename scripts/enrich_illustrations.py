"""Adiciona capturas selecionadas por contexto, mantendo a origem de cada figura."""
import hashlib
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request,urlopen
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
W='working-with-leapwork/'
A='administration/'
D='building-blocks/data-driven/'
SELECTION=[
 ('dados-ler-excel',2,D+'read-excel',3,'Opções de origem e configuração da planilha na documentação. Confira o modo e o intervalo usados no seu ambiente.'),
 ('dados-escrever-excel',2,D+'write-excel',3,'Configuração do intervalo de escrita. O índice e o acréscimo precisam corresponder à região selecionada.'),
 ('dados-decisoes',3,'building-blocks/logic/switch',1,'Exemplo oficial de casos do Switch. O caminho sem correspondência precisa ser previsto pelo caso.'),
 ('dados-csharp',2,'building-blocks/logic/c-sharp-code',1,'Editor C# da documentação consultada. Use o template da versão instalada; não copie uma assinatura de outra versão sem conferir.'),
 ('dados-csharp',3,'building-blocks/logic/c-sharp-code',3,'Área de referências do C# Code. Dependências externas precisam ser adicionadas no contexto documentado.'),
 ('controle-ambiente',2,A+'license-management',0,'License Management mostra a configuração da licença ativa e os recursos do Controller. Consulta é diferente de desativação.'),
 ('controle-ambiente',4,A+'license-management',1,'Ação Refresh License apresentada na fonte. Ela atualiza dados da licença e não substitui um diagnóstico de acesso.'),
 ('controle-acessos',2,A+'privileges-settings',0,'Privileges Settings reúne opções que alteram o acesso efetivo dos papéis; confira a configuração atual.'),
 ('controle-acessos',3,A+'team-management',0,'Formulário de criação de equipe e seleção dos integrantes. A disponibilidade depende da edição.'),
 ('controle-acessos',4,A+'user-management',10,'Opções de identidade na entrada do Flow: conta Leapwork, diretório ou SSO conforme a configuração. Esta figura vem de User Management.'),
 ('controle-acessos',4,A+'active-directory-settings',2,'Configuração de domínio específico na documentação de AD. O responsável pelo ambiente precisa validar os requisitos e o alcance.'),
 ('controle-acessos',4,A+'emergency-admin-user',3,'Tela do procedimento de conta administrativa de emergência na fonte específica. Conhecer o procedimento não exige alterar uma conta durante o estudo.'),
 ('controle-conexoes',1,A+'connections/appium-server-connection',0,'Exemplo de cadastro de conexão Appium. É um dos tipos disponíveis; o provedor e o formulário devem corresponder ao objetivo da integração.'),
 ('controle-conexoes',2,A+'api-access-keys',0,'Criação de uma chave de API com finalidade e escopo. A imagem é um exemplo oficial; não registre segredos reais nas notas.'),
 ('controle-conexoes',3,A+'e-mail-settings',1,'Seleção do protocolo de e-mail na fonte. SMTP e OAuth têm requisitos e comportamentos de teste próprios.'),
 ('controle-conexoes',4,A+'proxy-settings',0,'Configuração de proxy apresentada na documentação. Verifique o acesso no componente que efetivamente fará a chamada.'),
 ('controle-retencao',2,A+'retention-policies',1,'Detalhe de política de retenção. Confira o tipo de execução e a herança de configuração antes de reduzir a janela de evidências.'),
 ('controle-retencao',3,A+'database-decryption-keys',0,'Acesso à opção de chave do banco pelo Controller. O procedimento da fonte trata a recuperação dos dados SQLite.'),
 ('controle-retencao',4,A+'database-management',0,'Database Management oferece correções específicas de sub-flows. Esses controles não representam um backup integral.'),
 ('controle-padroes',2,A+'wip-capture-settings',0,'Capture Settings apresenta limites e comportamento da inspeção. Esses limites são diferentes do tempo de execução de um fluxo.'),
 ('controle-padroes',3,A+'wip-web-settings',0,'Web Settings com configuração de estratégias Salesforce. A tela é específica do recurso documentado.'),
 ('controle-agentes',2,W+'agents-overview',3,'Propriedades de Remote Agent, incluindo autenticação e sessão. Confira os valores do ambiente de homologação.'),
 ('controle-runlists',2,W+'run-lists',12,'Seleção de fluxos para um passo da Run List. Confira os itens antes de adicioná-los.'),
 ('controle-runlists',3,W+'run-lists',10,'Passo da Run List na interface oficial. As condições controlam se o trabalho seguinte deve executar.'),
 ('controle-runlists',4,W+'run-lists',4,'Cópia de Run List e agendamentos no exemplo oficial. As referências aos fluxos permanecem compartilhadas.'),
 ('controle-repeticoes',1,W+'run-lists',16,'Opções de Retry Policy. Desativar, herdar e personalizar são escolhas distintas.'),
 ('controle-repeticoes',2,W+'run-lists/schedules',0,'Acesso aos agendamentos e à política de retry no menu da lista. Confira o nível que define a política efetiva.'),
 ('controle-repeticoes',4,W+'reporting',6,'Detalhes da execução associam vídeo, canvas e Activity log para preservar o diagnóstico das tentativas.'),
 ('controle-agendamentos',2,W+'run-lists/schedules',3,'Configuração de Agents e distribuição do agendamento. Repartir carga não equivale a repetir tudo em cada ambiente.'),
 ('controle-agendamentos',3,W+'run-lists/schedules',9,'Configurações adicionais do agendamento na fonte. Revise ocupação, limites e disponibilidade de opções na sua edição.'),
 ('controle-agendamentos',4,W+'run-lists/schedules',5,'Ações do Schedule e condições de disparo de notificações. Configuração e recebimento precisam de verificação própria.'),
 ('controle-relatorios',2,W+'reporting',4,'Filtros do relatório restringem a população a investigar; confira lista e Schedule correspondentes.'),
 ('controle-relatorios',3,W+'reporting',6,'Vídeo, canvas e Activity log nos detalhes de um run. A imagem pertence ao exemplo da documentação.'),
 ('controle-dashboards',2,W+'dashboards',1,'Criação de widget com tipo, período e parâmetros. Defina a pergunta antes de escolher o gráfico.'),
 ('controle-dashboards',3,W+'dashboards',4,'Filtro por Agents do widget. O indicador representa apenas os ambientes selecionados.'),
 ('controle-dashboards',3,W+'dashboards',5,'Filtro por Run Lists e Schedules do widget. Registre esse recorte ao comparar períodos.'),
 ('controle-auditoria',2,A+'audit-log',1,'Filtro de auditoria no exemplo oficial. O recorte precisa manter os eventos relevantes ao incidente.'),
 ('controle-auditoria',4,A+'diagnostics',0,'Diagnostics reúne seleção de componentes, pacote e resultados da coleta. A evidência precisa corresponder ao ambiente investigado.'),
 ('controle-historico',1,A+'workflow-stettings',2,'Política de comentários ao salvar ou mudar estado. Registre o que mudou e a verificação realizada.'),
 ('controle-historico',3,W+'designing-automation-flows',14,'Version History na documentação. Confira versão, contexto e comentário antes de escolher uma recuperação.'),
 ('controle-restauracao',4,W+'reporting',6,'A validação posterior depende das evidências da nova execução, não apenas da conclusão da restauração.'),
 ('controle-compartilhamento',2,W+'organizing-your-work',5,'Exemplo de fluxo com seus ativos na árvore. Inventarie arquivos e componentes antes da transferência.'),
 ('controle-compartilhamento',3,W+'run-lists',8,'Importação de Run List e tratamento de conflitos. Confira o que será criado ou atualizado no destino.'),
 ('ciclo-organizacao',2,W+'organizing-your-work',5,'Organização de ativos sob o fluxo na referência oficial. A estrutura deve tornar as dependências visíveis.'),
 ('ciclo-subflows',3,W+'designing-automation-flows/sub-flows',7,'Exemplo de sub-flow com caminhos de resultado nomeados. A decisão do caso precisa respeitar o contrato do componente.'),
 ('ciclo-estabilidade',1,'building-blocks/web/find-web-element',0,'Find Web Element e suas propriedades. Identifique o alvo correto, em vez de aceitar qualquer elemento parecido.'),
 ('ciclo-estabilidade',2,'building-blocks/logic/wait',0,'Wait configura uma pausa de tempo. Esse bloco sozinho não comprova que uma confirmação apareceu.'),
 ('ciclo-estabilidade',3,'building-blocks/web/get-web-text',0,'Get Web Text fornece o texto do elemento identificado. Relacione o retorno ao registro atual.'),
 ('ciclo-estabilidade',4,'building-blocks/logic/compare',0,'Compare dirige os caminhos pelo resultado da comparação. Confira valores e método conforme a regra do caso.'),
 ('ciclo-dados',1,D+'read-excel',3,'Configuração de origem da planilha. Os dados precisam estar disponíveis na máquina e identidade de execução.'),
 ('ciclo-revisao',1,W+'designing-automation-flows',13,'Comentário de uma versão na interface documentada. Descreva intenção e evidência, não apenas que algo foi ajustado.'),
 ('ciclo-integracoes',1,'what-is-leapwork/architecture-overview',0,'Arquitetura oficial com Flow, Controller e Agent. O disparo externo deve preservar o contexto da execução coordenada pelo Controller.'),
 ('ciclo-integracoes',2,W+'run-lists/schedules',3,'Escolha de Agents e distribuição no Schedule. Confira a configuração acionada pela integração.'),
 ('ciclo-api-acesso',2,A+'api-access-keys',0,'Configuração administrativa de AccessKey e escopos. O laboratório do caderno usa somente um marcador de segredo.'),
 ('ciclo-api-resultados',4,W+'reporting',6,'Detalhes do resultado no relatório. Relacione o item da API à execução e à evidência corretas.'),
 ('ciclo-ado',1,A+'connections/azure-devops-ado-server-connections',2,'Configuração da conexão ADO na fonte. O PAT externo e AccessKey do Controller atendem a serviços diferentes.'),
 ('ciclo-ado',3,W+'microsoft-ado-test-plan-integration',5,'Seleção do projeto na sincronização ADO. A entrada de novos casos e a atualização dos existentes têm procedimentos distintos.'),
 ('ciclo-ado',4,W+'microsoft-ado-test-plan-integration',14,'Resumo de um test run no ADO apresentado na fonte. Confira caso, configuração e resultado no destino.'),
 ('ciclo-primeira-execucao',2,W+'run-lists',14,'Fluxos adicionados a um passo da Run List no exemplo oficial. Confira a correspondência com a matriz planejada.'),
 ('ciclo-primeira-execucao',3,W+'run-lists/schedules',2,'Formulário de Schedule. O exemplo oficial ilustra a configuração; não é uma execução dos dez casos fictícios.'),
 ('ciclo-triagem',1,W+'reporting',6,'A investigação parte dos detalhes da execução e cruza log, canvas e gravação disponível.'),
 ('ciclo-triagem',2,A+'audit-log',0,'Registro de eventos administrativos. Mudanças próximas ao horário da falha são pistas, não prova automática de causa.'),
 ('ciclo-triagem',3,W+'microsoft-ado-test-plan-integration',18,'Formulário de bug ADO na documentação. Um relato útil registra contexto, reprodução, esperado, observado e evidência.'),
 ('ciclo-encerramento',3,A+'retention-policies',0,'Políticas de retenção definem a disponibilidade de resultados, versões e gravações para a revisão posterior.'),
]


def main():
    inventory=json.loads((ROOT/'research/documentation-inventory.json').read_text(encoding='utf-8'))
    sources={p['url'].split('/latest/')[-1]:json.loads((ROOT/p['cacheFile']).read_text(encoding='utf-8')) for p in inventory['pages']}
    baseline=json.loads((ROOT/'research/enrichment-baseline.json').read_text(encoding='utf-8'))
    lessons={l['slug']:l for l in baseline['lessons']}
    target=ROOT/'site/assets/supplements';target.mkdir(exist_ok=True)
    rows=[]
    reviewed=[]
    for entry in SELECTION:
        slug,num,path,index,caption=entry
        if (slug,num)==('controle-agendamentos',3):continue  # A figura mostra Flow Report, não filas.
        if (slug,num)==('dados-ler-excel',2):num=1;caption='Read Excel com Source type Cloud file, conexão e Range. Esta é a alternativa de origem em nuvem; não é a janela de seleção de células.'
        if (slug,num)==('controle-runlists',3):index=11
        if (slug,num)==('controle-auditoria',2):index=2
        if (slug,num)==('controle-historico',1):index=3
        if (slug,num)==('ciclo-triagem',3):index=17
        if slug=='controle-acessos' and path==A+'active-directory-settings':path=A+'user-management';index=1;caption='Acesso a Add AD/SSO User na documentação de User Management. A identidade externa depende da configuração de diretório ou SSO.'
        if (slug,num)==('controle-ambiente',2):caption='Exemplo oficial antigo de License Information, com licença, Agents e validade. A interface da sua versão pode diferir; esta imagem não representa uma licença deste computador.'
        reviewed.append((slug,num,path,index,caption))
    reviewed += [
        ('@introducao',0,'what-is-leapwork/architecture-overview',0,'Comunicação entre Flow, Controller e Agent no diagrama oficial. O Flow também se comunica com Agents durante desenho e prévia.'),
        ('@introducao',0,'what-is-leapwork/architecture-overview',1,'Diagrama de implantação apresentado na fonte. Compare a localização dos componentes com o modelo contratado.'),
        ('@introducao',0,'what-is-leapwork/architecture-overview',3,'Implantação híbrida no exemplo oficial. As capacidades de execução dependem do tipo de Agent selecionado.')
    ]
    for slug,num,path,index,caption in reviewed:
        doc=sources[path];picture=doc['images'][index];key=hashlib.sha256(picture['url'].encode()).hexdigest()[:16]
        rows.append({'lesson':slug,'step':num,'path':'assets/supplements/'+key+'.png','kind':'documentation','source':doc['url'],'imageSource':picture['url'],'caption':caption,'sourceImageIndex':index})
    def download(row):
        dest=ROOT/'site'/row['path']
        try:
            if not dest.exists():
                candidates=[row['imageSource']]
                if '%3F' in row['imageSource']:candidates.append(row['imageSource'].split('%3F')[0])
                for url in candidates:
                    try:
                        data=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
                        dest.write_bytes(data);row['resolvedImageSource']=url;break
                    except Exception:
                        if url==candidates[-1]:raise
            with Image.open(dest) as im:row['width'],row['height']=im.size
        except Exception as error:
            row['error']=str(error);print('IMAGE UNAVAILABLE: '+row['source']+' #'+str(row['sourceImageIndex'])+' '+str(error),flush=True)
        return row
    # Deduplicar downloads antes de iniciar o pool.
    unique={row['path']:row for row in rows}
    with ThreadPoolExecutor(max_workers=4) as pool:loaded={row['path']:row for row in pool.map(download,unique.values())}
    unavailable=[loaded[p] for p in loaded if 'error' in loaded[p]]
    (ROOT/'.publication/illustration-download-errors.json').write_text(json.dumps(unavailable,ensure_ascii=False,indent=2),encoding='utf-8')
    rows=[row for row in rows if 'error' not in loaded[row['path']]]
    for row in rows:row.update(width=loaded[row['path']]['width'],height=loaded[row['path']]['height'],resolvedImageSource=loaded[row['path']].get('resolvedImageSource',row['imageSource']))
    video=[{'lesson':l['slug'],'step':i+1,'time':s['time'],'video':l['video']} for l in baseline['lessons'] if l.get('video') for i,s in enumerate(l['steps']) if not s['hadImage']]
    corrections={'desktop-introducao':522,'desktop-contatos':260,'virtual-textos':205,'virtual-teclado':145,'arrastar-soltar':105,'dropdowns-avancados':183}
    skip={'frames-aninhados','controles-dinamicos','carregamento-novo-elemento'}
    for v in video:
        if v['lesson'] in skip:continue
        timestamp=corrections.get(v['lesson'],v['time'])
        filename=f"{v['video']}-{timestamp}-audit.jpg";dest=target/filename
        if not dest.exists():subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(timestamp),'-i',str(ROOT/'videos'/(v['video']+'.mp4')),'-frames:v','1','-q:v','3','-y',str(dest)],check=True)
        with Image.open(dest) as im:width,height=im.size
        rows.append({'lesson':v['lesson'],'step':v['step'],'path':'assets/supplements/'+filename,'kind':'frame','source':f"https://www.youtube.com/watch?v={v['video']}&t={timestamp}s",'caption':f"Quadro do vídeo original em {timestamp//60}:{timestamp%60:02} para acompanhar o contexto deste passo. Não é uma captura de execução local.",'time':timestamp,'width':width,'height':height})
    for row in rows:
        if row['lesson']=='@introducao':row.update(module=1,lessonTitle='Introdução e arquitetura',stepTitle='Protocolos e implantação')
        else:
            l=lessons[row['lesson']];row.update(module=l['module'],lessonTitle=l['title'],stepTitle=l['steps'][row['step']-1]['title'])
    (ROOT/'research/illustration-additions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'site/illustrations.js').write_text('/* Figuras suplementares selecionadas por passo, com proveniência. */\n(()=>{const rows='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';window.LEAP.illustrationAdditions=rows;rows.forEach(row=>{if(row.lesson==="@introducao"){(window.LEAP.introFigures??=[]).push(row);return;}const lesson=window.LEAP.lessons.find(l=>l.slug===row.lesson);if(!lesson)throw Error(row.lesson);const step=lesson.steps[row.step-1];(step.additionalFigures??=[]).push(row);});})();\n',encoding='utf-8')
    used={row['path'] for row in rows}
    for file in target.iterdir():
        if file.is_file() and file.resolve().parent==target.resolve() and 'assets/supplements/'+file.name not in used:file.unlink()
    previews=ROOT/'.publication/illustration-review';previews.mkdir(exist_ok=True)
    for start in range(0,len(rows),12):
        selected=rows[start:start+12];sheet=Image.new('RGB',(1500,340*((len(selected)+2)//3)),'#10152c');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(selected):
            x=i%3*500;y=i//3*340;im=Image.open(ROOT/'site'/row['path']).convert('RGB');im.thumbnail((480,282));sheet.paste(im,(x+10,y+43));draw.text((x+10,y+8),f"{start+i}: {row['lesson']} #{row['step']}",fill='white')
        sheet.save(previews/f'sheet-{start//12}.jpg')
    print(json.dumps({'figures':len(rows),'uniqueAssets':len({r['path'] for r in rows}),'steps':len({(r['lesson'],r['step']) for r in rows}),'lessons':len({r['lesson'] for r in rows})}),flush=True)


if __name__=='__main__':main()

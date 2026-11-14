"""Create fictional study data and an independent Decimal-based expected result file."""
import base64,csv,json,mimetypes,subprocess
from decimal import Decimal,ROUND_HALF_EVEN
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site/assets/examples';OUT.mkdir(parents=True,exist_ok=True)
script="global.window={};require('./site/content.js');require('./site/module3.js');console.log(JSON.stringify(window.LEAP.module3Rows));"
rows=json.loads(subprocess.check_output(['node','-e',script],cwd=ROOT,encoding='utf-8'))
headers=['ID','Nome','Quantidade','Preco','Grupo']
values=[[r[k] for k in ['id','nome','quantidade','preco','grupo']] for r in rows]
def workbook(file,sheet,headers,values):
    book=Workbook();tab=book.active;tab.title=sheet;tab.append(headers)
    for row in values:tab.append(row)
    tab.freeze_panes='A2';tab.auto_filter.ref=tab.dimensions
    for cell in tab[1]:cell.fill=PatternFill('solid',fgColor='171C35');cell.font=Font(color='FFFFFF',bold=True)
    for row in tab.iter_rows(min_row=2):
        for cell in row:
            if cell.row%2==0:cell.fill=PatternFill('solid',fgColor='EFEBFA')
    for col in tab.columns:
        from openpyxl.utils import get_column_letter
        tab.column_dimensions[get_column_letter(col[0].column)].width=min(55,max(18,max(len(str(c.value or '')) for c in col)+3))
    info=book.create_sheet('Leia-me');info.append(['Origem','Exemplo autoral fictício do caderno local. Não é exercício oficial.']);info.append(['Contrato','Quantidade inteira positiva; preço com vírgula decimal sem milhar; BASICO 5%, PREMIUM 10%.']);info.append(['Arredondamento','Ponto médio para o par, em centavos.']);info.append(['Execução','Arquivos não foram executados no Leapwork.']);info.column_dimensions['A'].width=20;info.column_dimensions['B'].width=110
    book.save(OUT/file)
def csvfile(file,head,values):
    with (OUT/file).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f,delimiter=';');writer.writerow(head);writer.writerows(values)
workbook('modulo3-entradas.xlsx','Casos',headers,values)
csvfile('modulo3-entradas.csv',headers,values)
(OUT/'modulo3-resposta.json').write_text(json.dumps({'origem':'Amostra autoral fictícia; não é resposta de uma chamada HTTP real.','registros':rows},ensure_ascii=False,indent=2),encoding='utf-8')
expected=[]
for r in rows:
    if int(r['quantidade'])<=0:expected.append([r['id'],r['nome'].strip(),'REJEITADO','','','','Quantidade deve ser um inteiro positivo.']);continue
    subtotal=Decimal(r['preco'].replace(',','.'))*int(r['quantidade'])*100
    discount=5 if r['grupo'].strip().upper()=='BASICO' else 10
    total=(subtotal*(100-discount)/100).quantize(Decimal(1),rounding=ROUND_HALF_EVEN)
    expected.append([r['id'],r['nome'].strip(),'ACEITO',int(subtotal),discount,int(total),'Contrato de entrada atendido.'])
expected_headers=['ID','NomeNormalizado','Status','SubtotalCentavos','DescontoPercentual','TotalCentavos','Motivo']
csvfile('modulo3-esperados.csv',expected_headers,expected)
workbook('modulo3-resultados.xlsx','Resultados',expected_headers,[])
assert [row[5] for row in expected]==[3781,3375,'',10]
assets={}
for file in OUT.glob('modulo3-*'):
    assets['assets/examples/'+file.name]={'name':file.name,'mime':mimetypes.guess_type(file.name)[0] or 'application/octet-stream','data':base64.b64encode(file.read_bytes()).decode('ascii')}
(ROOT/'site/module3-files.js').write_text('/* Cópias incorporadas dos exemplos para download offline via Blob. */\nwindow.LEAP.module3FileData='+json.dumps(assets)+';\n',encoding='utf-8')
print(json.dumps({'inputRows':len(rows),'accepted':3,'rejected':1,'files':5}))

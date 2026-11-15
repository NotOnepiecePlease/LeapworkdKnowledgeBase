# Caderno de estudo Leapwork

Base de conhecimento local em português para estudar automação com Leapwork. Edição v1.1.0, com os módulos 1, 2, 3 e 4 preparados para estudo.

## Baixar e começar a estudar

1. Acesse a [última release](https://github.com/NotOnepiecePlease/LeapworkdKnowledgeBase/releases/latest).
2. Em **Assets**, baixe **LeapworkKnowledgeBase-v1.1.0-completo.zip** para ter o caderno e os 48 vídeos offline (aproximadamente 1,1 GB). O arquivo **essencial.zip** contém as aulas, imagens, GIFs e laboratório, sem os vídeos locais.
3. Extraia **todo o ZIP** para uma pasta no computador. No Windows, clique com o botão direito e escolha **Extrair tudo**. Não abra o caderno de dentro do ZIP.
4. Abra a pasta extraída e dê dois cliques em **Abrir caderno.cmd** no Windows. No macOS e Linux, abra **site/index.html** no navegador.
5. Comece pelo módulo **01**, siga as aulas, responda às revisões e marque seu progresso. O módulo **03** também oferece um laboratório interativo com arquivos de exemplo.

Não é necessário instalar Node, Python, servidor ou Leapwork para consultar o material. Para executar os fluxos de automação propostos, será necessário ter acesso ao Leapwork. Use um navegador moderno, como Edge, Chrome ou Firefox.

**Escolha do download:** o pacote completo funciona offline, inclusive os vídeos. No essencial e no código-fonte, use os links para assistir aos vídeos originais na internet; o player de arquivo local exige o pacote completo. Os arquivos automáticos **Source code (zip/tar.gz)** do GitHub também não incluem os vídeos.

**Atualizações e notas:** antes de trocar de versão ou mover a pasta, use **Exportar minhas anotações**. As notas e o progresso ficam no navegador e dependem do endereço local; uma nova pasta ou outro navegador pode apresentar um histórico separado. A exportação é uma cópia de segurança para consulta e não deve ser tratada como importação automática.

### Se algo não abrir

- **Página sem imagens ou estilos:** extraia novamente o ZIP inteiro, preservando as subpastas.
- **Vídeo não carrega:** confirme que baixou o pacote completo e que `videos` fica ao lado de `site`, com os arquivos MP4 dentro. No pacote essencial, use o link do vídeo original.
- **Atalho não abre no seu sistema:** abra `site/index.html` diretamente pelo navegador.
- **Notas não aparecem:** use o mesmo navegador e a mesma pasta em que estudou; confira a cópia exportada das anotações.

## Sumário do conteúdo e próximos módulos

| Módulo | Estado nesta versão | Conteúdo |
| --- | --- | --- |
| Introdução | Disponível | Arquitetura: Flow, Controller e Agent |
| 01 · Fundamentos | Disponível: 15 aulas | Web (6): primeiro fluxo, sub-flows, formulários, leitura, listas e páginas móveis. Desktop (3): fluxo inicial, contatos com planilha e integração com Web. Virtual (6): imagens, OCR, cliques, teclado e áreas relativas |
| 02 · Automação avançada | Disponível: 32 aulas | 29 exemplos Web: autenticação, DOM, controles, esperas, arquivos, hover, frames, rolagem, alertas, abas, notificações e tabelas. Mais 3 aulas Desktop: listas, localizadores dinâmicos e dados entre janelas |
| 03 · Dados e manipulação | Disponível: 19 aulas | Excel, ODBC, HTTP/API, arquivos, comandos, e-mail, condições, repetições, cálculos, texto, datas, variáveis, geradores, clipboard, esperas e C#. Inclui laboratório local |
| 04 · Administração, monitoramento e controle | Disponível: 16 aulas | Controller, usuários, permissões, conexões, retenção, Agents, Run Lists, retry, agendamentos, relatórios, dashboards, auditoria, histórico, restauração e transferência de ativos. Inclui dois laboratórios locais |
| 05 · Boas práticas, integração e ciclo de testes | Planejado; ainda sem aulas | Expansão posterior do material de estudo |

O módulo 5 ainda não tem data de entrega. As tabelas abaixo detalham todas as aulas disponíveis. Ao todo são **82 aulas, 363 etapas, 14 GIFs, 48 vídeos e 48 termos de glossário**, além de revisões, busca, notas e marcação de progresso. No módulo 3, uma aula acompanha um vídeo oficial e as outras 18 são estudos de documentação com exemplos autorais. As 16 aulas do módulo 4 são baseadas em documentação; não são vídeos novos.

## Obter o código-fonte

```sh
git clone https://github.com/NotOnepiecePlease/LeapworkdKnowledgeBase.git
cd LeapworkdKnowledgeBase
```

Depois, abra `site/index.html`. O repositório mantém o site, os materiais de referência e os scripts de manutenção. Os MP4 são distribuídos separadamente no pacote completo da release para manter o histórico do Git menor. Não há etapa de build para estudar.

Para preparar novos pacotes a partir de uma cópia com os vídeos locais, execute `python scripts/package_release.py --version v1.1.0`. Os ZIPs e o arquivo de verificação SHA-256 serão gerados em `dist/`. A publicação usa `scripts/publish_release.ps1`, com Git e GitHub CLI autenticado; os arquivos são verificados antes do envio.

## Créditos e origem

Este é um caderno de estudo independente em português, sem afiliação oficial com a Leapwork. Vídeos, capturas e imagens de documentação têm origem nas fontes oficiais indicadas em cada aula e continuam pertencendo aos respectivos titulares. As licenças das fontes tipográficas acompanham os arquivos em `site/assets/fonts`. O repositório não concede uma licença geral sobre materiais de terceiros.

## Abrir o site

Dê dois cliques em **Abrir caderno.cmd**. Ele abre `site/index.html` no navegador padrão.
Também é possível abrir `site/index.html` diretamente no Edge, Chrome ou outro navegador moderno.

Não precisa instalar pacotes, iniciar servidor, criar conta ou instalar o Leapwork para consultar o caderno. Mantenha as pastas `site` e `videos` juntas nesta pasta principal. Aulas, imagens, busca, revisões e vídeos funcionam sem internet; links externos exigem conexão.

## Temas e leitura

Use o botão com lua/sol no canto superior direito para alternar entre **Claro** e **Escuro**. A escolha fica salva neste navegador; antes da primeira escolha, o site acompanha o tema do sistema. O controle de tema usa uma chave própria e preserva as anotações e marcações existentes.

A paleta utiliza navy, lavanda, rosa e ciano, inspirada na referência visual fornecida. Os textos principais dos passos têm 18 px no computador e 17 px em telas pequenas, com maior entrelinha. Títulos usam Outfit e textos usam Manrope. As fontes e suas licenças OFL estão incluídas localmente; não há requisições externas para carregá-las.

Os passos têm cartões individuais, 32 px de separação no computador, cabeçalhos maiores e blocos distintos para explicação, imagem e observação. As seções têm mais espaço e o texto possui largura limitada para leitura. As capturas e os GIFs originais mantêm suas cores.

## Conteúdo disponível

- Introdução à arquitetura: Flow, Controller e Agent.
- Módulo 1: seis aulas Web, três Desktop e seis Virtual, além da introdução à arquitetura. Módulo 2: 29 assuntos Web e três aulas Desktop disponíveis, além da referência à aula de listas do módulo 1.
- 82 aulas nos quatro módulos, com 363 etapas, 250 usos de imagens de referência e 14 GIFs controláveis.
- 48 vídeos locais com áudio e acesso aos trechos indicados nas etapas.
- Esquemas didáticos, conceitos, objetivos e pontos de atenção.
- Exercícios autorais sem instalação e propostas de prática posterior com Leapwork.
- Duas questões de revisão por aula, com correção e explicação.
- Glossário de 48 termos.
- Busca nas aulas, etapas, pontos de atenção e glossário, com suporte a acentos.
- Marcação de aulas revisadas, anotações por aula e exportação das notas.
- Referências por aula, horários originais e diferenças de interface sinalizadas.
- Layout responsivo, ampliação de imagens e impressão das aulas.

As anotações e marcações são salvas neste navegador e neste endereço local. Limpar os dados do navegador ou trocar de navegador pode removê-las. Use **Exportar minhas anotações** para manter uma cópia em arquivo.

## Recorte atual e expansão

O módulo 1 reúne a introdução e todos os quinze vídeos selecionados nas seções Web, Desktop e Virtual do treinamento oficial. O material de estudo está preparado; os fluxos não foram executados no Leapwork e os exercícios do portal oficial não foram reproduzidos. A navegação separa as três tecnologias e o progresso conta as quinze aulas.

| Aula no caderno | Assunto | Aula na playlist | ID do vídeo |
| --- | --- | --- | --- |
| 01 | Primeiro fluxo web | 1 | d9m4N9sxFT0 |
| 02 | Sub-flows e reutilização | 2 | 9IdcfvVSKAc |
| 03 | Formulários e controles web | 4 | qHp1RY9AQds |
| 04 | Leitura de textos e números | 5 | M-y1MxK3_Dw |
| 05 | Listas de elementos | 6 | pZAVmupXWhE |
| 06 | Páginas web móveis | 7 | aGduKxCIZAk |
| 07 | Seu primeiro fluxo desktop | 1 | -51LTRplY48 |
| 08 | Criar contatos a partir de uma planilha | 3 | TXWo3qK9Oy8 |
| 09 | Automatizar entre desktop e web | 6 | 23YBj_t1EjA |
| 10 | Começar a automação virtual | 1 | ynF7HY2ux_c |
| 11 | Reconhecer imagens na tela | 2 | sJ3Fa3kSiJg |
| 12 | Ler textos e números por OCR | 3 | qGGNbk0UY-0 |
| 13 | Clicar por imagem e por texto | 4 | fO6aVmNKUCc |
| 14 | Digitar e controlar teclas | 6 | akmkQk8sc40 |
| 15 | Usar posições e áreas relativas | 7 | rK8qIFccfbk |

A seleção segue os links da página oficial: Web 1, 2, 4, 5, 6 e 7; Desktop 1, 3 e 6; Virtual 1, 2, 3, 4, 6 e 7. As playlists incluem outros vídeos, por isso a numeração original tem saltos. Aulas 01–06 são Web; 07–09, Desktop; 10–15, Virtual.

## Módulo 2 completo para estudo

Entre pelo seletor **02 · Automação avançada** ou pelo menu lateral. Há 32 aulas com progresso próprio, separadas em controles e interações; conteúdo dinâmico e esperas; imagens e arquivos; DOM, frames e tabelas; navegação e autenticação; alertas e notificações; Desktop avançado.

A coleção Testing the Internet está integralmente adaptada: **29 de 29 vídeos** com aulas em português, passos ligados aos horários, imagens, conceitos, cuidados, exercícios autorais e revisão. A página também inclui as três aulas Desktop selecionadas no treinamento oficial. A aula de listas do módulo 1 é reutilizada por referência. A fonte oficial não apresenta uma seção separada de vídeos Virtual no módulo 2.

| Aula | Assunto | Aula original | Vídeo |
| --- | --- | --- | --- |
| 01 | Autenticação básica HTTP | Testing the Internet 1 | AL_LQQ4yMLc |
| 02 | Detectar imagens quebradas | Testing the Internet 2 | xAl2LfFKxj0 |
| 03 | Escolher estratégias no DOM | Testing the Internet 3 | lsGjkso3Rbg |
| 04 | Marcar e desmarcar checkboxes | Testing the Internet 4 | lb78WgJ0-wo |
| 05 | Arrastar e soltar elementos web | Testing the Internet 5 | suIDRArjQEk |
| 06 | Tratar elementos que aparecem ou somem | Testing the Internet 6 | 3M0KO_fi8WY |
| 07 | Selecionar opções por valor, texto ou índice | Testing the Internet 7 | r8IH1LYegOo |
| 08 | Localizar conteúdo que muda a cada carga | Testing the Internet 8 | gERnZ6rN1VQ |
| 09 | Esperar a remoção de um controle | Testing the Internet 9 | TCcN6YORYC0 |
| 10 | Esperar um elemento ficar visível | Testing the Internet 10 | YP3TJrud2BY |
| 11 | Esperar um elemento ser adicionado | Testing the Internet 11 | c56VBmlFSC0 |
| 12 | Percorrer links de download | Testing the Internet 12 | Cd4rHHq2OZY |
| 13 | Enviar um arquivo e verificar a confirmação | Testing the Internet 13 | bM5smmLOsBs |
| 14 | Verificar um menu durante a rolagem | Testing the Internet 14 | Xw2nXTOe9NE |
| 15 | Autenticar por formulário e teclado | Testing the Internet 15 | _t-g5jxOdno |
| 16 | Revelar e validar conteúdo ao passar o mouse | Testing the Internet 16 | 5SALJ43raC4 |
| 17 | Editar conteúdo dentro de um iframe | Testing the Internet 17 | I4rIpx-xlic |
| 18 | Explorar rolagem infinita com limite | Testing the Internet 18 | vbz5ckcdb-Y |
| 19 | Aceitar e cancelar alertas JavaScript | Testing the Internet 19 | oke1UlnrP0c |
| 20 | Enviar uma tecla e validar a resposta | Testing the Internet 20 | 47VeVtNuyFk |
| 21 | Escolher localizadores em um DOM grande | Testing the Internet 21 | SiZZut-jgiY |
| 22 | Capturar conteúdo em frames aninhados | Testing the Internet 22 | c3aFyb7pRIE |
| 23 | Ler e registrar notificações variáveis | Testing the Internet 23 | 36KXvQRsMq4 |
| 24 | Selecionar uma nova janela ou aba | Testing the Internet 24 | Mg-1NKCuf3g |
| 25 | Conferir a página após um redirecionamento | Testing the Internet 25 | I_BUzm8rJ0I |
| 26 | Encontrar uma imagem após mudanças de posição | Testing the Internet 26 | N8utEzbs2SM |
| 27 | Encontrar um item que muda de posição na lista | Testing the Internet 27 | X9Em1PtM9XU |
| 28 | Manter a identidade da linha após ordenar a tabela | Testing the Internet 28 | B98UeOK1CTU |
| 29 | Localizar elementos apesar de variações no texto | Testing the Internet 29 | lBcRNry3bo8 |
| 30 | Listas e soma no desktop | Desktop UI Automation 4 | HWUVg1tTclg |
| 31 | Campos dinâmicos no localizador | Desktop UI Automation 5 | 3ALOfIs_OTY |
| 32 | Dados entre janelas desktop | Desktop UI Automation 7 | J-ui6FyDkXg |

As três aulas Desktop agora aparecem como 30, 31 e 32 para manter a sequência de estudo após os 29 assuntos Web. Os endereços das aulas, suas notas e as marcações foram preservados. O catálogo relaciona cada vídeo à aula local e mantém acesso ao original para verificação.

A conferência visual identificou `Failed` no encerramento de trechos dos vídeos de dropdown e tabela ordenável, apesar da narração de sucesso. As aulas sinalizam a diferença, sem atribuir uma causa não demonstrada. A aula de iframe descreve a página TinyMCE efetivamente exibida no vídeo. Critérios simplificados, como Y ≥ 0 para menu flutuante e índice de rolagem, têm suas limitações explicadas.

Os exercícios 3, 4 e 5 do portal oficial voltaram a retornar erro de carregamento. Mantivemos os links; seus enunciados não foram reproduzidos. Todos os exercícios locais continuam identificados como autorais. Os fluxos não foram executados no Leapwork, que ainda não está instalado.

### GIFs e captura corrigida

A imagem escurecida do passo 3 do primeiro fluxo foi substituída por um quadro claro da configuração Password, com GIF de 11 segundos mostrando a ação. Há também GIFs de estratégias DOM, linhas desktop, campo dinâmico, transferência entre janelas, iteração de contatos, ponto de interação visual, atalhos de teclado, região relativa, arraste Web, mudança de visibilidade, hover e imagem que muda de posição.

As animações são extraídas dos vídeos locais com FFmpeg, carregadas apenas quando você escolhe **Reproduzir animação** e podem ser paradas para voltar ao quadro de referência. Os horários do GIF, do quadro e do trecho original permanecem identificados. Nenhum GIF começa automaticamente. As notas e o progresso usam a mesma chave de armazenamento da versão anterior.

Conteúdo futuro, identificado como planejado:

- Módulo 5: boas práticas, integração e revisão do ciclo de testes.

## Módulo 3: dados e manipulação

Entre por **03 · Dados e manipulação**. O caderno organiza 19 aulas: uma acompanha o vídeo oficial **Data Driven Automation Demo** (80 segundos) e 18 são estudos baseados na documentação. Não são 19 vídeos oficiais. O progresso deste módulo é independente, sem alterar notas e marcações dos anteriores.

Os estudos abrangem os 29 blocos das quatro categorias indicadas pelo treinamento: Data-Driven (9), Logic (15), Variables (2) e Generators (3). Offset Position e Offset Area também retomam a aula de posições e áreas do módulo 1. A tabela de cobertura no site liga cada bloco ao estudo e à sua documentação.

| Aula do caderno | Assunto | Base |
| --- | --- | --- |
| 01 | Um fluxo, vários conjuntos de dados | Vídeo oficial |
| 02 | Ler uma planilha com intervalo e iteração | Documentação + exemplo autoral |
| 03 | Escrever resultados no Excel | Documentação + exemplo autoral |
| 04 | Usar dados de um banco por ODBC | Documentação + exemplo autoral |
| 05 | Consultar uma API e validar sua resposta | Documentação + exemplo autoral |
| 06 | Fornecer, compactar e guardar arquivos | Documentação + exemplo autoral |
| 07 | Consumir a saída de um comando | Documentação + exemplo autoral |
| 08 | Preparar uma notificação por e-mail | Documentação + exemplo autoral |
| 09 | Comparar valores e escolher caminhos | Documentação + exemplo autoral |
| 10 | Controlar repetições e interrupções | Documentação + exemplo autoral |
| 11 | Calcular sem confundir texto e número | Documentação + exemplo autoral |
| 12 | Normalizar texto e extrair padrões | Documentação + exemplo autoral |
| 13 | Gerar datas e aplicar deslocamentos | Documentação + exemplo autoral |
| 14 | Guardar valores com o escopo correto | Documentação + exemplo autoral |
| 15 | Gerar números e senhas de teste | Documentação + exemplo autoral |
| 16 | Transferir texto pela área de transferência | Documentação + exemplo autoral |
| 17 | Usar esperas e preparar o estado das janelas | Documentação + exemplo autoral |
| 18 | Reconhecer quando usar lógica C# | Documentação + exemplo autoral |
| 19 | Laboratório: validar, calcular e registrar | Documentação + exemplo autoral |

### Visuais e laboratório local

O vídeo tem três capturas selecionadas e um GIF de parametrização. Os estudos de documentação usam imagens originais dos blocos, com proporção preservada, ampliação e referência em cada figura. Foram armazenadas 29 imagens de blocos em `site/assets/docs`; alguns estudos usam mais de uma imagem. Não são capturas de uma execução local no Leapwork.

O laboratório permite alterar quatro registros fictícios e acompanhar validação, subtotal, desconto e total. Ele roda apenas no navegador, sem servidor, chamadas externas ou instalação do Leapwork. Os arquivos são autorais: planilha de entradas, CSV de entradas, JSON fictício, CSV de resultados esperados e modelo Excel de relatório. Os botões usam cópias incorporadas em Blob para garantir download ao abrir o site por `file://`.

Contrato do laboratório: quantidade inteira positiva; preço com vírgula decimal sem separador de milhar; grupos BASICO (5%) e PREMIUM (10%); nomes sem espaços externos; cálculo em centavos com arredondamento de ponto médio para o par. Os quatro exemplos produzem três aceitações e uma rejeição esperada por quantidade zero. Os totais aceitos são 3781, 3375 e 10 centavos. Os resultados de referência foram gerados independentemente com Decimal em Python e comparados ao simulador.

O simulador não executa nem emula o motor Leapwork. A conversão dos campos, a execução dos blocos e a validação dos fluxos no programa permanecem como prática posterior. Os exercícios oficiais 1 a 5 não foram reproduzidos porque o portal retornou Loading / CSS Error; o site mantém o link para verificação.

## Módulo 4: administração, monitoramento e controle

Entre por **04 · Administração e controle** no seletor de módulos ou no menu lateral. As **16 aulas** têm 64 passos de estudo, 32 questões com explicação, exercícios autorais, referências por etapa, notas e progresso independente. O material cobre os nove assuntos centrais indicados pelo treinamento: administração, Remote Agent, Run Lists, Schedules, Reporting, Dashboards, histórico, restauração e exportação/importação.

| Aula | Assunto |
| --- | --- |
| 01 | Identificar o Controller e os recursos do ambiente |
| 02 | Organizar usuários, equipes e permissões |
| 03 | Preparar conexões, chaves e notificações |
| 04 | Preservar evidências e planejar a retenção |
| 05 | Conferir padrões de execução e captura |
| 06 | Preparar e verificar um Agent remoto |
| 07 | Organizar fluxos em Run Lists e passos |
| 08 | Definir repetição sem esconder falhas |
| 09 | Planejar horários, distribuição e filas |
| 10 | Investigar resultados com relatório, vídeo e log |
| 11 | Montar dashboards com contexto e comparação |
| 12 | Correlacionar auditoria, mudanças e diagnóstico |
| 13 | Registrar mudanças e consultar o histórico |
| 14 | Escolher Only Flow, Full Restore ou Full Copy |
| 15 | Exportar, importar e conferir dependências |
| 16 | Laboratório: planejar, observar e recuperar |

O treinamento não indica uma coleção própria de vídeos para este módulo. As aulas são estudos autorais em português com base na documentação oficial, com 12 imagens de interface e 34 referências locais de consulta. Algumas dessas referências já eram usadas no caderno. As imagens preservam a interface de origem e podem ser ampliadas. As diferenças de versão e de edição são sinalizadas no conteúdo.

### Laboratórios sem instalação

- **Distribuição:** compara todos os fluxos em cada Agent, divisão de carga e primeiro disponível. Para quatro fluxos e dois Agents, os volumes planejados são 8, 4 e 4. A divisão visual usa rodízio didático; não promete a atribuição exata nem a duração real do Leapwork. Considera recursos disponíveis e fluxos compatíveis.
- **Restauração:** compara Only Flow (lógica antiga e Locators atuais), Full Restore (ambos antigos) e Full Copy (cópia da versão escolhida, preservando o atual). Cada comparação começa do mesmo exemplo fictício, sem acumular ações anteriores.

A ficha JSON exportável guarda as escolhas atuais e o texto do exercício. Não é um fluxo importável no Leapwork. O rascunho do laboratório não é salvo automaticamente; use o download ou as anotações persistidas da aula. Nenhuma dessas atividades conecta máquinas, executa fluxos, envia notificações ou acessa sistemas externos.

Os artigos de suporte sobre histórico, restauração, transferência e exercícios retornaram tela de carregamento/erro CSS na consulta. Os links originais foram preservados, e as funções são estudadas pelas páginas atuais da documentação oficial. Os enunciados oficiais não foram reproduzidos. Recursos especializados de administração têm referências complementares para consulta conforme a implantação. A prática real no Leapwork continua pendente de acesso ao programa.

## Fontes e preparação

- Estrutura do curso: https://leapwork.com/learning-center/self-paced-training/#h-module-1-introduction-to-leapwork-and-web-desktop-virtual-testing
- Entrada da documentação: https://docs.leapwork.com/leapwork-flow/latest/what-is-leapwork/architecture-overview
- Playlist: https://www.youtube.com/playlist?list=PL4qgJwtW1RjaCW32VlVtL4PBMVx67FjCY

Foram armazenadas 118 páginas da documentação, abrangendo arquitetura, automação, dados e administração. Algumas páginas são índices de categorias. As referências utilizadas estão nas aulas e na página Fontes. Snapshots de consulta ficam em `research/docs`, com suas datas de coleta originais. A cobertura e as ressalvas do módulo 4 estão em `research/module4-sources.json`.

O texto editorial foi preparado a partir das legendas originais em inglês, das capturas conferidas e da documentação. O YouTube limitou as requisições de traduções automáticas; elas não foram usadas como base do material. O download dos vídeos e a extração de capturas nesta etapa não consumiram créditos do vidIQ.

A documentação atual usa o Elegance Design, introduzido em 2025.3, enquanto a primeira aula mostra uma edição 2022.3. O caderno sinaliza diferenças relevantes. Os esquemas são simplificações didáticas e as capturas são imagens reais dos vídeos.

O usuário ainda não tem o Leapwork instalado. Os fluxos não foram executados no Leapwork durante esta preparação. As aulas distinguem estudo e raciocínio de prática que exige o programa. Os exercícios do caderno são autorais, sem serem apresentados como reprodução dos exercícios oficiais.

## Organização dos arquivos

| Caminho | Conteúdo |
| --- | --- |
| `site/index.html` | Página inicial e estrutura |
| `site/styles.css` | Estrutura e comportamentos de layout |
| `site/appearance.css` | Paletas light/dark, tipografia e novo espaçamento |
| `site/assets/fonts` | Manrope, Outfit, CSS incorporado e licenças OFL |
| `site/app.js` | Navegação, busca, vídeos, revisão, notas e progresso |
| `site/content.js` | Seis aulas Web do módulo 1 |
| `site/module1-extra.js` | Três aulas Desktop e seis Virtual do módulo 1 |
| `site/module2.js` | Primeiras seis aulas do módulo 2 e correção visual do login |
| `site/module2-extra.js` | 26 aulas adicionais, grupos de assunto e notas de conferência |
| `site/module3.js` | 19 estudos, referências, entradas e metadados do módulo 3 |
| `site/module3-view.js` | Página do módulo, laboratório e download offline |
| `site/module3-files.js` | Cópias incorporadas dos cinco arquivos de exemplo |
| `site/module4.js` | 16 aulas, 32 questões e termos do glossário de administração e controle |
| `site/module4-view.js` | Visão geral, cobertura, laboratórios e exportação da ficha JSON |
| `site/module4.css` | Estilos dos laboratórios, com temas e layout responsivo |
| `site/catalog.js` | Catálogo dos 29 exemplos web e estado de preparação |
| `site/media.js` | Durações verificadas dos vídeos locais |
| `site/assets/frames` | Quadros de referência por vídeo e segundo |
| `site/assets/animations` | 14 GIFs derivados dos vídeos |
| `site/assets/docs` | Imagens originais da documentação para o módulo 3 |
| `site/assets/examples` | Arquivos fictícios XLSX, CSV e JSON do laboratório |
| `research/animations-manifest.json` | Vídeo, intervalo e tamanho de cada GIF |
| `videos` | Vídeos MP4, legendas VTT, metadados e índice da playlist |
| `frames` | Captura do teste inicial |
| `research/docs` | Referências das páginas de documentação consultadas |
| `research/course-content.json` | Cópia estruturada do conteúdo entregue |
| `research/module2-sources.json` | Cobertura oficial, vídeos, legendas e ressalvas de conferência |
| `research/module2-shots.json` | Horários das capturas adicionais do módulo 2 |
| `research/module3-sources.json` | Cobertura e origem dos estudos do módulo 3 |
| `research/module3-documents.json` | Fontes das imagens e dimensões originais |
| `research/module4-sources.json` | Cobertura do treinamento, referências e limitações do módulo 4 |
| `research/module4-documents.json` | 34 referências e origem das 12 imagens do módulo 4 |
| `research/media-manifest.json` | Durações, codecs, dimensões e tamanhos dos vídeos |
| `research/contact-sheets` | Folhas de contato usadas na conferência visual |
| `research/qa` | Relatório dos testes e capturas do site |
| `scripts` | Utilitários de coleta, extração e verificação |
| `tools` | Dependências locais de yt-dlp para Python |

Os vídeos ocupam aproximadamente 1060 MB e os GIFs, 28.9 MB. O site só carrega um vídeo quando você abre o player.

## Verificações executadas

- Módulo 4: 185 verificações de navegador aprovadas em `scripts/check_module4.py`, incluindo as 16 aulas e revisões, referências, imagens, busca, progresso independente, preservação e exportação das notas anteriores, os dois laboratórios, validação de entradas, download da ficha JSON, temas e larguras de 1440, 768 e 390 px. Nenhuma requisição externa ou erro de JavaScript nos fluxos testados. Relatório em `research/qa/module4-report.json`.

- Sintaxe JavaScript conferida com `node --check`.
- Referências de imagens, vídeos, documentos e limites dos horários conferidos por `scripts/finalize_content.py`.
- 810 verificações de navegador aprovadas com Playwright/Chromium: 189 gerais, 50 do módulo 1, 50 do módulo 2, 33 de aparência, 128 da coleção Web, 175 do módulo 3 e 185 do módulo 4. O site foi aberto diretamente como arquivo local.
- Conferidos ambos os temas, persistência da preferência, fontes offline, preservação das notas e larguras de 1905, 1280, 768 e 390 px. Contraste das combinações de texto principal, secundário e acento sobre suas superfícies conferido acima de 4,5:1 nos dois temas.
- Conferidos busca, entrada segura de texto, rotas, imagens das 82 aulas, ampliação, notas persistidas, exportação, marcação de progresso, respostas de revisão e reprodução de trecho local.
- Layout conferido em computador (1440 px) e tela pequena (390 px), sem transbordamento horizontal nas páginas testadas.
- Nenhum erro de JavaScript nos fluxos testados. Relatórios em `research/qa`: `browser-report.json`, `module1-report.json`, `module2-report.json`, `appearance-report.json`, `module2-completion-report.json` e `module3-report.json`.

Os utilitários de manutenção usam Python, FFmpeg, Node e bibliotecas disponíveis neste ambiente. O site pronto não depende dessas ferramentas para funcionar. O teste de navegador usa um contexto isolado e efêmero; não modifica o perfil pessoal.


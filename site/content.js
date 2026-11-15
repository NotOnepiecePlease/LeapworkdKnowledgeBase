/* Conteúdo em português; durações verificadas nos vídeos locais. */
window.LEAP = {
  "updated": "14/11/2026",
  "course": "https://leapwork.com/learning-center/self-paced-training/#h-module-1-introduction-to-leapwork-and-web-desktop-virtual-testing",
  "docsBase": "https://docs.leapwork.com/leapwork-flow/latest/",
  "modules": [
    [
      "01",
      "Fundamentos de automação",
      "Introdução · Web · Desktop · Virtual"
    ],
    [
      "02",
      "Automação avançada",
      "Web, desktop e ambientes virtuais"
    ],
    [
      "03",
      "Dados e manipulação",
      "Testes orientados a dados"
    ],
    [
      "04",
      "Administração e controle",
      "Monitoramento, execução e versões"
    ],
    [
      "05",
      "Boas práticas e integração",
      "APIs e ciclo de testes"
    ]
  ],
  "glossary": [
    [
      "Flow",
      "Fluxo",
      "Sequência visual de ações, decisões e verificações que compõe uma automação.",
      "primeiro-fluxo"
    ],
    [
      "Building block",
      "Bloco",
      "Unidade que executa uma ação, fornece dados ou controla o caminho do fluxo.",
      "primeiro-fluxo"
    ],
    [
      "Canvas",
      "Área de desenho",
      "Espaço em que os blocos e suas conexões são organizados.",
      "primeiro-fluxo"
    ],
    [
      "Green connector",
      "Conector verde",
      "Define a sequência de execução: qual ação acontece depois.",
      "primeiro-fluxo"
    ],
    [
      "Blue connector",
      "Conector azul",
      "Transporta valores e propriedades entre blocos; não substitui a conexão de execução.",
      "sub-flows"
    ],
    [
      "Sub-flow",
      "Subfluxo",
      "Componente reutilizável que reúne blocos e pode receber parâmetros.",
      "sub-flows"
    ],
    [
      "Value Input",
      "Parâmetro de entrada",
      "Bloco usado dentro de um subfluxo para receber um valor do fluxo chamador.",
      "sub-flows"
    ],
    [
      "Locator",
      "Localizador",
      "Estratégia usada para identificar um elemento na página; a imagem no bloco é uma referência visual.",
      "listas"
    ],
    [
      "DOM",
      "Estrutura da página",
      "Árvore de elementos HTML que representa a página no navegador.",
      "listas"
    ],
    [
      "Strategy Editor",
      "Editor de estratégias",
      "Ferramenta para examinar, ajustar e validar o localizador de um elemento.",
      "listas"
    ],
    [
      "Await DOM change",
      "Espera pela estabilidade do DOM",
      "Adia a busca até que a estrutura da página fique estável conforme as opções do bloco.",
      "primeiro-fluxo"
    ],
    [
      "Source element",
      "Elemento de origem",
      "Restringe uma busca ao interior de um elemento já encontrado, como uma linha de tabela.",
      "listas"
    ],
    [
      "Use occurrence / All",
      "Ocorrência / Todas",
      "Permite escolher uma correspondência ou processar todas as correspondências encontradas.",
      "listas"
    ],
    [
      "Count",
      "Quantidade",
      "Total de correspondências encontradas; não é o mesmo que o número lido de um texto.",
      "leitura"
    ],
    [
      "Find format",
      "Formato de extração",
      "Padrão que delimita a parte dinâmica de um texto ou número a extrair.",
      "leitura"
    ],
    [
      "Activity Log",
      "Registro de atividades",
      "Histórico dos blocos executados, mensagens e resultados, usado junto ao vídeo da execução.",
      "primeiro-fluxo"
    ],
    [
      "Pass / Fail / Done",
      "Estados de término",
      "Pass encerra com sucesso, Fail com falha, e Done com resultado neutro.",
      "primeiro-fluxo"
    ],
    [
      "Device type",
      "Tipo de dispositivo",
      "Configuração do navegador que seleciona um perfil de emulação de dispositivo.",
      "mobile"
    ],
    [
      "Viewport",
      "Área visível",
      "Dimensões da área de exibição da página; influencia a disposição responsiva dos elementos.",
      "mobile"
    ]
  ],
  "lessons": [
    {
      "slug": "primeiro-fluxo",
      "number": "01",
      "originalLesson": "1",
      "video": "d9m4N9sxFT0",
      "duration": "8:37",
      "read": "12 min",
      "title": "Seu primeiro fluxo web",
      "eyebrow": "Do primeiro bloco à primeira verificação",
      "description": "Entenda como um login vira um fluxo visual, como lidar com uma página lenta e como provar que a execução funcionou.",
      "objectives": [
        "Ler a ordem de execução pelas conexões verdes.",
        "Distinguir uma ação de uma verificação.",
        "Investigar uma falha com vídeo e Activity Log."
      ],
      "concepts": [
        [
          "Uma ação por bloco",
          "Abrir o navegador, digitar e clicar são ações distintas. A conexão verde entre os blocos estabelece a ordem dessas ações."
        ],
        [
          "Sucesso precisa de evidência",
          "Chegar ao fim dos cliques não prova que houve login. O exemplo procura um elemento da sessão autenticada antes de encerrar com Pass."
        ],
        [
          "Tempo também faz parte do teste",
          "Um elemento pode existir na aplicação e ainda não estar disponível quando a automação tenta usá-lo. A investigação deve considerar o estado da página naquele instante."
        ]
      ],
      "flow": [
        "Start",
        "Start Web Browser",
        "Type Web Text",
        "Click Web Element",
        "Find Web Element",
        "Pass"
      ],
      "flowNote": "Esquema resumido: o vídeo repete blocos de digitação e clique para e-mail, senha e confirmações.",
      "steps": [
        {
          "time": 32,
          "image": 45,
          "title": "Crie um fluxo com um nome reconhecível",
          "text": "No menu New, escolha Flow e dê um nome que descreva o objetivo, como “Validar login”. O fluxo começa pelo bloco Start. Antes de gravar, pense no que precisa acontecer e na evidência que comprovará o resultado.",
          "observe": "A captura mostra a criação do fluxo no painel esquerdo. O nome será sua referência para encontrar e manter essa automação depois.",
          "caption": "Criação e nomeação do fluxo no painel Flows."
        },
        {
          "time": 50,
          "image": 100,
          "title": "Abra o gravador e inicie o navegador",
          "text": "Arraste a saída verde de Start e escolha Start Recorder. No controle de gravação, use a opção para iniciar um navegador. Selecione Chrome, informe a URL da aplicação de estudo e confirme. O navegador deve fazer parte do fluxo, em vez de depender de uma janela aberta manualmente.",
          "observe": "No diálogo Start Web Browser, identifique o campo de URL e a escolha do navegador. O gravador captura ações; depois você ainda poderá revisar os blocos gerados.",
          "caption": "Configuração do navegador durante a gravação."
        },
        {
          "time": 114,
          "image": 145,
          "title": "Capture os campos e os botões do login",
          "text": "Capture o campo de usuário e use Type Web Text para inserir o e-mail. Capture Next com Click Web Element. Repita a digitação para a senha e configure Type como Password para mascarar o valor exibido. Em seguida, registre os botões de entrada e as confirmações mostradas pela aplicação.",
          "observe": "A tela está no modo de captura sobre a etapa de senha. O campo alvo precisa ser identificado pelo localizador; a miniatura do bloco ajuda a reconhecê-lo visualmente.",
          "caption": "Captura do campo de senha na tela de login."
        },
        {
          "time": 241,
          "image": 250,
          "title": "Investigue a falha antes de mudar o fluxo",
          "text": "Ao executar, o exemplo falha no bloco que digita a senha: o elemento ainda não havia carregado. Leia a mensagem no Activity Log e compare com o vídeo da execução. Um erro de localização pode decorrer de uma espera insuficiente, mas também de um localizador incorreto ou de uma página inesperada.",
          "observe": "O bloco com borda vermelha marca o ponto da falha. O registro e a tela gravada permitem verificar o que estava disponível naquele momento.",
          "caption": "Falha no bloco de senha, com vídeo e registro de atividades."
        },
        {
          "time": 290,
          "image": 300,
          "title": "Configure a espera e teste novamente",
          "text": "Edite o bloco Type Web Text da senha, expanda suas propriedades e habilite Await DOM change como demonstrado. Salve e execute novamente. Essa opção aguarda estabilidade do DOM antes da busca; ela não garante, sozinha, que qualquer elemento será encontrado.",
          "observe": "O bloco expandido reúne as propriedades de digitação e espera. Na interface atual, várias opções aparecem no Inspector; procure o nome da propriedade, não apenas sua posição na tela.",
          "caption": "Propriedades expandidas do bloco Type Web Text."
        },
        {
          "time": 322,
          "image": 365,
          "title": "Verifique o login e defina o resultado",
          "text": "Depois do login, use Find Web Element para encontrar um sinal da sessão autenticada. No vídeo, esse sinal são as iniciais do usuário no topo da aplicação. Acrescente Pass depois da verificação. Esse critério é específico do exemplo: em outra aplicação, escolha uma evidência confiável de que a sessão correta foi aberta.",
          "observe": "A aplicação autenticada aparece no navegador enquanto o gravador é usado para capturar a evidência. Evite escolher um elemento que também exista antes do login.",
          "caption": "Página autenticada usada para selecionar uma evidência de login."
        },
        {
          "time": 423,
          "image": 470,
          "title": "Use o registro para entender a execução",
          "text": "Execute o fluxo completo. Selecione uma entrada do Activity Log para relacionar o bloco, a mensagem e o instante da gravação. Confira se o caminho chegou à verificação esperada e ao bloco de término, em vez de concluir apenas pela aparência final da página.",
          "observe": "A captura mostra o registro de execução e o vídeo sincronizado com o bloco destacado. Essa relação é a base da depuração visual no Leapwork.",
          "caption": "Inspeção de um passo pelo Activity Log e pelo vídeo da execução."
        }
      ],
      "pitfalls": [
        [
          "“Não encontrou” não identifica a causa",
          "Confira o estado da página, o navegador utilizado, o localizador e as esperas. A mesma mensagem pode ter origens diferentes."
        ],
        [
          "Mascarar não é uma política completa de credenciais",
          "O tipo Password oculta a exibição no bloco. Não use dados reais nas suas anotações ou nas capturas de estudo."
        ],
        [
          "Pass sem verificação enfraquece o teste",
          "O resultado deve depender de uma evidência relevante para o objetivo do fluxo."
        ]
      ],
      "exercise": {
        "title": "Desenhe um login no papel",
        "tasks": [
          "Liste as ações necessárias para entrar em uma aplicação que você conhece.",
          "Escolha um elemento que só apareça após o login.",
          "Marque onde uma página lenta poderia interromper o fluxo."
        ],
        "answer": "Um roteiro possível é abrir a URL → preencher usuário → avançar → preencher senha → entrar → localizar uma evidência da sessão → Pass. As esperas pertencem aos pontos em que o próximo elemento pode ainda não estar pronto."
      },
      "practice": "Quando tiver acesso ao Leapwork, reproduza o roteiro em uma aplicação de teste autorizada. Revise os blocos gerados e só considere o exercício concluído depois de verificar a sessão e o resultado no log.",
      "quiz": [
        {
          "q": "Qual conexão define qual bloco executa depois?",
          "options": [
            "A verde.",
            "A azul.",
            "A miniatura do elemento."
          ],
          "correct": 0,
          "why": "A verde conduz a execução. A azul transmite valores e propriedades."
        },
        {
          "q": "O login terminou sem erro de clique. Isso basta para aprovar o teste?",
          "options": [
            "Sim, todos os cliques funcionaram.",
            "Não; é preciso verificar uma evidência do resultado."
          ],
          "correct": 1,
          "why": "Um fluxo de teste precisa conferir seu objetivo, como a presença de um elemento da sessão autenticada."
        }
      ],
      "docs": [
        [
          "Como os fluxos são desenhados",
          "working-with-leapwork/designing-automation-flows"
        ],
        [
          "Type Web Text e opções de espera",
          "building-blocks/web/type-web-text"
        ],
        [
          "Find Web Element",
          "building-blocks/web/find-web-element"
        ],
        [
          "Estados de término",
          "building-blocks/start-stop"
        ]
      ]
    },
    {
      "slug": "sub-flows",
      "number": "02",
      "originalLesson": "2",
      "video": "9IdcfvVSKAc",
      "duration": "9:32",
      "read": "11 min",
      "title": "Sub-flows e reutilização",
      "eyebrow": "Escreva a lógica uma vez. Reutilize com outros dados.",
      "description": "Transforme o login em um componente reutilizável e entenda como parâmetros e conexões azuis reduzem a duplicação.",
      "objectives": [
        "Reconhecer uma sequência que merece virar subfluxo.",
        "Separar a lógica de login dos valores de entrada.",
        "Acompanhar a execução dentro de um subfluxo."
      ],
      "concepts": [
        [
          "Reutilizar reduz manutenção",
          "Se dez fluxos copiam o mesmo login, uma mudança pode exigir dez correções. Um subfluxo concentra a lógica compartilhada."
        ],
        [
          "Parâmetros tornam o componente flexível",
          "O fluxo chamador fornece e-mail e senha; o componente reutiliza a sequência. Assim, a lógica deixa de depender de um único conjunto de valores."
        ],
        [
          "Execução e dados são caminhos diferentes",
          "A conexão verde indica quando o subfluxo executa. As conexões azuis fornecem os valores usados nas suas entradas."
        ]
      ],
      "flow": [
        "Start Web Browser",
        "Sign In (sub-flow)",
        "Find Web Element",
        "Pass"
      ],
      "flowNote": "E-mail e senha entram no Sign In por conexões azuis. O navegador é aberto pelo fluxo chamador neste exemplo.",
      "steps": [
        {
          "time": 104,
          "image": 125,
          "title": "Selecione apenas a lógica que será compartilhada",
          "text": "Partindo do login da aula anterior, selecione os blocos de entrada de usuário, senha e confirmações. Clique com o botão direito e escolha Create Sub-flow. Dê um nome claro, como Sign In. A seleção define a responsabilidade do componente.",
          "observe": "O diálogo de nomeação aparece sobre os blocos selecionados. No exemplo, abrir o navegador e validar o login permanecem fora do conjunto reutilizável.",
          "caption": "Nomeação do componente criado a partir dos blocos selecionados."
        },
        {
          "time": 179,
          "image": 185,
          "title": "Insira o subfluxo em outro fluxo",
          "text": "Crie um novo fluxo e abra o menu de blocos. Na categoria Sub-flows, escolha Sign In. Prepare a janela de navegador esperada pelo componente e conecte a execução. Reutilizar significa chamar a mesma definição, em vez de copiar novamente seus blocos internos.",
          "observe": "A categoria Sub-flows lista o componente criado. Antes de reutilizá-lo, reconheça quais condições precisam existir na entrada, como o navegador já aberto.",
          "caption": "Subfluxo disponível no menu de adição de blocos."
        },
        {
          "time": 235,
          "image": 295,
          "title": "Adicione parâmetros com Value Input",
          "text": "Abra Edit Sub-flow. Adicione Value Input na categoria Module input and output e renomeie para Email. Conecte sua saída azul ao valor de texto do bloco que digita o usuário. Repita com um parâmetro Password ligado ao bloco de senha.",
          "observe": "A captura mostra o bloco Email e seu conector azul durante a configuração. O parâmetro representa um dado recebido; a sequência de cliques continua sendo controlada pelos conectores verdes.",
          "caption": "Criação da entrada Email dentro do subfluxo."
        },
        {
          "time": 330,
          "image": 340,
          "title": "Confira o contrato do componente",
          "text": "Salve o subfluxo e volte ao fluxo principal. Agora o bloco Sign In expõe Email e Password. Essas entradas formam um contrato simples: quem chama fornece os dados e o componente executa a lógica usando esses valores.",
          "observe": "O Sign In mostra os dois campos de entrada no fluxo chamador. Uma alteração compartilhada deve ser revisada considerando os outros fluxos que usam a mesma definição.",
          "caption": "Email e Password expostos no bloco Sign In."
        },
        {
          "time": 347,
          "image": 420,
          "title": "Forneça os dados pelo fluxo principal",
          "text": "O vídeo usa Set Text para fornecer cada valor e conecta a saída azul ao parâmetro correspondente. No bloco que guarda a senha, seleciona o tipo Password para mascarar a exibição. Também seria possível preencher as entradas diretamente; fontes externas de dados serão estudadas em outro recorte.",
          "observe": "As conexões azuis saem de Set Text e chegam ao Sign In. Confira o destino de cada uma para não trocar usuário e senha.",
          "caption": "Dados fornecidos ao subfluxo por blocos Set Text."
        },
        {
          "time": 466,
          "image": 480,
          "title": "Depure os blocos internos pelo registro",
          "text": "Execute o fluxo completo. No Activity Log, selecione uma mensagem de um bloco interno. O vídeo demonstra que um duplo clique nessa entrada abre a prévia do subfluxo e destaca o bloco relacionado. Use isso para distinguir falhas na chamada de falhas dentro do componente.",
          "observe": "O log inclui ações internas, mesmo que o canvas principal mostre apenas Sign In. Um componente compacto continua sendo inspecionável.",
          "caption": "Inspeção da execução de um componente reutilizável pelo log."
        }
      ],
      "pitfalls": [
        [
          "Copiar blocos não cria reutilização compartilhada",
          "A cópia duplica a lógica. O subfluxo mantém uma definição usada em vários lugares."
        ],
        [
          "O componente tem pré-condições",
          "Neste exemplo, o navegador já precisa estar aberto. Nomeie e documente essa expectativa."
        ],
        [
          "Uma mudança pode afetar vários testes",
          "Ao editar o subfluxo, revise os fluxos dependentes e teste os cenários relevantes."
        ]
      ],
      "exercise": {
        "title": "Defina as entradas de um componente",
        "tasks": [
          "Imagine três fluxos que começam com o mesmo login.",
          "Descreva o que é igual nos três e o que varia.",
          "Escreva quais entradas o subfluxo deve receber e o que precisa existir antes da chamada."
        ],
        "answer": "A sequência de navegação pode ser compartilhada; os valores de usuário e senha variam. Email e Password são entradas. Neste desenho, a janela da aplicação já deve estar aberta. A verificação do resultado permanece explícita no fluxo chamador."
      },
      "practice": "Com o Leapwork disponível, transforme uma sequência de teste em subfluxo e use dois conjuntos de dados fictícios. Confira as conexões e acompanhe uma execução por dentro do componente.",
      "quiz": [
        {
          "q": "Qual bloco cria uma entrada de valor dentro de um subfluxo?",
          "options": [
            "Value Input.",
            "Pass.",
            "Click Web Element."
          ],
          "correct": 0,
          "why": "Value Input expõe um parâmetro que o fluxo chamador pode preencher."
        },
        {
          "q": "Uma conexão azul fornece a ordem de execução?",
          "options": [
            "Sim.",
            "Não, ela transporta dados."
          ],
          "correct": 1,
          "why": "Ordem de execução e passagem de dados são funções distintas."
        }
      ],
      "docs": [
        [
          "Criar e parametrizar subfluxos",
          "working-with-leapwork/designing-automation-flows/sub-flows"
        ],
        [
          "Value Input",
          "building-blocks/module-input-and-output/value-input"
        ],
        [
          "Conectores e desenho de fluxos",
          "working-with-leapwork/designing-automation-flows"
        ]
      ]
    },
    {
      "slug": "formularios",
      "number": "03",
      "originalLesson": "4",
      "video": "qHp1RY9AQds",
      "duration": "8:41",
      "read": "12 min",
      "title": "Formulários e controles web",
      "eyebrow": "Escolha o bloco de acordo com o controle",
      "description": "Explore listas suspensas, alternadores, campos de texto e botões de opção usando o formulário de processamento do Dynamics 365.",
      "objectives": [
        "Escolher entre clicar, digitar e selecionar.",
        "Distinguir seleção por texto, valor e índice.",
        "Reconhecer por que limpar um campo muda o resultado."
      ],
      "concepts": [
        [
          "Controles parecidos podem exigir ações diferentes",
          "Um campo de texto recebe digitação; uma lista seleciona uma opção; um alternador pode ser acionado por clique. Observe o comportamento e a estrutura do controle."
        ],
        [
          "Texto não é o mesmo que valor",
          "O rótulo visível, o atributo value e a posição na lista podem diferir. A estratégia de seleção precisa corresponder ao que você informou."
        ],
        [
          "O estado inicial importa",
          "Um campo preenchido ou um alternador já ligado muda o efeito de uma ação. Planeje o estado esperado antes de executar."
        ]
      ],
      "flow": [
        "Sign In",
        "Set Web Dropdown",
        "Click Web Element",
        "Type Web Text",
        "Set Web Radio Button",
        "Confirmar"
      ],
      "flowNote": "Resumo do formulário: existem cliques intermediários para abrir a recorrência e confirmar os diálogos.",
      "steps": [
        {
          "time": 38,
          "image": 160,
          "title": "Prepare a página e acrescente blocos manualmente",
          "text": "O vídeo parte de um fluxo que já autentica e chega ao painel Generate invoice batch processing do D365. Com o navegador aberto por Start Web Browser, os blocos podem ser acrescentados diretamente no canvas, sem gravar toda a sequência de novo.",
          "observe": "O fluxo já possui passos anteriores e um Sign In. Você também verá Read Excel, vindo de outra aula da playlist; essa preparação não é um requisito para entender os controles aqui.",
          "caption": "Fluxo existente com um bloco Set Web Dropdown em configuração."
        },
        {
          "time": 111,
          "image": 205,
          "title": "Escolha uma opção em uma lista suspensa",
          "text": "Adicione Set Web Dropdown e capture o controle Filter by. Expanda Action e observe Set by value, Set by text e Set by index. Abra Edit web element e valide o alvo. O exemplo escolhe Set by text e informa Start date, conforme o texto exibido na aplicação.",
          "observe": "O Strategy Editor permite examinar atributos e validar o elemento. O índice depende da posição; o texto depende do rótulo; o valor depende do atributo correspondente.",
          "caption": "Inspeção do controle e de seus atributos no Strategy Editor."
        },
        {
          "time": 234,
          "image": 260,
          "title": "Capture o alternador como elemento clicável",
          "text": "O exemplo muda Consolidate by customer de No para Yes com Click Web Element. Adicione o bloco, use Capture new web element e selecione o alternador. Ao planejar um teste repetível, verifique também o estado inicial: um clique cego pode desligar um controle que já estava ligado.",
          "observe": "O alvo do bloco de clique está sendo capturado. Essa etapa registra a ação; a confirmação de que o estado ficou correto é uma verificação separada.",
          "caption": "Captura do alternador que será acionado por clique."
        },
        {
          "time": 272,
          "image": 330,
          "title": "Digite a descrição e limpe o conteúdo anterior",
          "text": "Use Type Web Text para preencher Task description. Informe um nome de teste, como Task Demo 1. Habilite Clear field para remover o conteúdo existente antes de inserir o novo texto. Sem essa opção, um valor prévio pode se misturar à entrada desejada.",
          "observe": "A captura mostra o campo de valor do bloco de digitação. O vídeo explica a opção Clear field logo nessa etapa; ela deve fazer parte do seu raciocínio sobre o estado inicial.",
          "caption": "Preenchimento da descrição pelo bloco Type Web Text."
        },
        {
          "time": 353,
          "image": 400,
          "title": "Selecione o padrão de recorrência",
          "text": "Use Click Web Element para abrir Recurrence. Adicione Set Web Radio Button, capture uma das opções do grupo e configure a forma de seleção. O exemplo explora Set by text; confirme o rótulo na página, em vez de confiar numa palavra reconhecida automaticamente pela legenda.",
          "observe": "O bloco de rádio aparece expandido e a miniatura mostra uma opção de recorrência. Radio buttons representam uma escolha dentro de um grupo.",
          "caption": "Configuração de Set Web Radio Button para o grupo de recorrência."
        },
        {
          "time": 407,
          "image": 495,
          "title": "Confirme os diálogos e observe a mensagem",
          "text": "Acrescente os cliques nos botões OK para salvar a recorrência e o processamento. A aplicação exibe uma mensagem informando que o trabalho entrou na fila. Nesta aula, o vídeo termina com Pass; a próxima aula acrescenta a leitura dessa mensagem para verificar o resultado.",
          "observe": "A notificação aparece no topo da aplicação. Conseguir clicar em OK e conseguir comprovar o processamento são etapas diferentes do teste.",
          "caption": "Mensagem exibida após confirmar o processamento no Dynamics 365."
        }
      ],
      "pitfalls": [
        [
          "Índice é sensível à ordem",
          "Uma opção pode mudar de posição quando a aplicação muda. Escolha a estratégia apropriada para o controle."
        ],
        [
          "Clique em alternador depende do estado",
          "Conheça o estado inicial e confira o resultado esperado após a ação."
        ],
        [
          "Uma notificação deve ser validada",
          "A aula seguinte transforma a mensagem visual em dado que o fluxo pode verificar."
        ]
      ],
      "exercise": {
        "title": "Monte um mapa de controles",
        "tasks": [
          "Classifique um formulário em texto, dropdown, rádio, alternador e botão.",
          "Para cada campo, escolha um bloco e um valor de teste.",
          "Descreva como verificar que os dados foram aceitos após confirmar."
        ],
        "answer": "Texto → Type Web Text; dropdown → Set Web Dropdown; rádio → Set Web Radio Button; ação de botão → Click Web Element. Para o alternador, considere seu estado. Uma mensagem de confirmação lida e comparada é uma possível evidência final."
      },
      "practice": "No Leapwork, abra uma página de teste pelo fluxo e configure cada tipo de controle. Evite aplicar o exercício em um formulário de produção que crie registros reais.",
      "quiz": [
        {
          "q": "“Set by text” usa qual informação?",
          "options": [
            "A posição da opção.",
            "O texto visível da opção.",
            "O endereço da página."
          ],
          "correct": 1,
          "why": "A seleção por texto usa o rótulo exibido; por valor usa o atributo subjacente e por índice usa a posição."
        },
        {
          "q": "Qual opção evita concatenar um texto ao conteúdo anterior do campo?",
          "options": [
            "Clear field.",
            "Count.",
            "Device type."
          ],
          "correct": 0,
          "why": "Clear field limpa o campo antes de inserir o texto."
        }
      ],
      "docs": [
        [
          "Set Web Dropdown",
          "building-blocks/web/set-web-dropdown"
        ],
        [
          "Type Web Text",
          "building-blocks/web/type-web-text"
        ],
        [
          "Set Web Radio Button",
          "building-blocks/web/set-web-radio-button"
        ],
        [
          "Click Web Element",
          "building-blocks/web/click-web-element"
        ]
      ]
    },
    {
      "slug": "leitura",
      "number": "04",
      "originalLesson": "5",
      "video": "M-y1MxK3_Dw",
      "duration": "8:20",
      "read": "12 min",
      "title": "Leitura de textos e números",
      "eyebrow": "Transforme o que aparece na tela em uma verificação",
      "description": "Leia uma mensagem de confirmação, extraia sua parte variável e compare um total exibido com a quantidade de elementos encontrados.",
      "objectives": [
        "Usar Text found e Number found como dados.",
        "Diferenciar Find format de Filter.",
        "Comparar um número exibido com Count."
      ],
      "concepts": [
        [
          "Ler e validar são operações relacionadas",
          "Ler captura um valor da interface. Validar aplica um critério a esse valor e decide qual caminho deve executar."
        ],
        [
          "Formato extrai; filtro restringe",
          "Find format delimita a parte que interessa no texto. Filter exige uma condição, como conter uma expressão esperada."
        ],
        [
          "Número lido e contagem não são a mesma coisa",
          "Get Web Number lê um valor apresentado. Count informa quantos elementos corresponderam ao localizador. O teste pode confrontar as duas fontes."
        ]
      ],
      "flow": [
        "Get Web Number",
        "Find Web Element",
        "Compare",
        "Pass / Fail"
      ],
      "flowNote": "A saída Number found alimenta Value A; Count alimenta Value B. As conexões verdes também precisam conduzir a execução até Compare.",
      "steps": [
        {
          "time": 43,
          "image": 85,
          "title": "Leia a mensagem e registre o texto encontrado",
          "text": "Continue a partir do formulário anterior. Substitua o término provisório por Get Web Text e capture a notificação. Adicione Log Message e ligue Text found à mensagem por um conector azul. Execute o trecho para observar o conteúdo que foi realmente retornado.",
          "observe": "A notificação está no topo do D365. Ao escolher o alvo, prefira o elemento da mensagem em vez de uma região grande que misture textos sem relação.",
          "caption": "Notificação que será lida pelo bloco Get Web Text."
        },
        {
          "time": 92,
          "image": 150,
          "title": "Extraia apenas o trecho variável",
          "text": "Expanda Get Web Text e use Find format. No exemplo, a mensagem contém um prefixo, o nome da tarefa e um sufixo informando a inclusão na fila. O formato mantém as partes fixas e marca o trecho variável. A documentação atual ilustra o uso de [TEXT] para essa parte.",
          "observe": "O bloco está aberto na propriedade Find format. O formato deve acompanhar o idioma e o texto da mensagem real; o exemplo em inglês não deve ser aplicado literalmente a uma interface em português.",
          "caption": "Edição do formato usado para extrair o nome da tarefa."
        },
        {
          "time": 168,
          "image": 180,
          "title": "Valide o conteúdo com um filtro",
          "text": "Configure Filter como Contains e informe o nome esperado. Para evitar repetir um valor fixo, o vídeo propõe passar ao filtro o mesmo dado usado na descrição da tarefa. Se o texto adequado não for encontrado, trate a saída Not found; quando a condição é satisfeita, continue pelo caminho de sucesso.",
          "observe": "O menu de filtro mostra opções como Starts with, Ends with e Contains. O filtro deve representar o que você quer provar, não apenas algo que costuma aparecer na mensagem.",
          "caption": "Opções de filtragem de texto no Get Web Text."
        },
        {
          "time": 205,
          "image": 320,
          "title": "Leia o total sem prender o localizador ao número",
          "text": "No segundo cenário, informe a conta do cliente e capture o cartão Active billing schedules com Get Web Number. Edite sua estratégia: remova o número variável do critério de localização e preserve o rótulo estável. Assim, o alvo pode continuar sendo encontrado quando o total mudar.",
          "observe": "O Strategy Editor mostra um critério que inclui o número atual. O objetivo é localizar o cartão pela sua identidade e extrair o número depois.",
          "caption": "Localizador do cartão de total em revisão no Strategy Editor."
        },
        {
          "time": 359,
          "image": 390,
          "title": "Conte as linhas que correspondem ao status",
          "text": "Use Find Web Element para localizar o status Active da tabela. Ajuste a estratégia para que ela encontre as correspondências desejadas. O vídeo remove uma restrição de ocorrência no editor; valide a seleção e examine os resultados, em vez de assumir que todas as linhas relevantes foram incluídas.",
          "observe": "O indicador do editor mostra várias correspondências. A contagem refere-se aos elementos encontrados nessa página e estratégia; paginação ou carregamento parcial precisam ser considerados em outros cenários.",
          "caption": "Múltiplos status Active encontrados pelo localizador."
        },
        {
          "time": 414,
          "image": 435,
          "title": "Compare as duas fontes e trate os resultados",
          "text": "Adicione Compare. Conecte Number found do cartão a Value A e Count dos elementos a Value B. Configure a comparação de igualdade e ligue o caminho verdadeiro a Pass e Incorrect a Fail. Ao executar, confira no log os valores usados, não apenas o resultado final.",
          "observe": "A imagem mostra os blocos de leitura, localização e comparação em montagem. As duas conexões azuis fornecem os valores; os caminhos de execução definem o que acontece com o resultado.",
          "caption": "Ligação de Number found e Count ao bloco Compare."
        }
      ],
      "pitfalls": [
        [
          "Não localize pelo número que deseja medir",
          "Um total variável dentro do localizador torna a busca dependente do resultado anterior."
        ],
        [
          "Um total pode ter outro escopo",
          "O cartão pode representar todos os registros, enquanto a tabela mostra apenas uma página ou um filtro. Confira o significado dos dados."
        ],
        [
          "Separadores numéricos importam",
          "Na prática, revise Decimal separator e 1000 separator no Get Web Number para o idioma dos valores apresentados."
        ]
      ],
      "exercise": {
        "title": "Compare duas evidências",
        "tasks": [
          "Imagine um cartão com “4 ativos” e quatro linhas de status Active.",
          "Explique qual valor vem de Get Web Number e qual vem de Count.",
          "Decida o resultado esperado se a tabela passar a mostrar apenas três linhas."
        ],
        "answer": "Number found pode retornar 4 do cartão. Count pode retornar 4 dos elementos de status encontrados. A igualdade passa. Se Count for 3, a comparação falha; antes de concluir um defeito, confira filtros, paginação e o escopo do cartão."
      },
      "practice": "Com o programa disponível, leia uma mensagem de teste, aplique um filtro e encaminhe explicitamente o caso de texto ausente. Depois compare uma contagem com um valor exibido.",
      "quiz": [
        {
          "q": "Qual saída informa quantos elementos combinam com um localizador?",
          "options": [
            "Number found.",
            "Count.",
            "Text found."
          ],
          "correct": 1,
          "why": "Count é a quantidade de correspondências. Number found é o valor numérico lido da página."
        },
        {
          "q": "Por que retirar o número variável de uma estratégia de localização?",
          "options": [
            "Para continuar identificando o cartão quando o total mudar.",
            "Para sempre retornar zero."
          ],
          "correct": 0,
          "why": "A identificação do cartão deve depender de atributos estáveis, e não do valor que será medido."
        }
      ],
      "docs": [
        [
          "Get Web Text: formatos e filtros",
          "building-blocks/web/get-web-text"
        ],
        [
          "Get Web Number: formatos numéricos",
          "building-blocks/web/get-web-number"
        ],
        [
          "Find Web Element: Count",
          "building-blocks/web/find-web-element"
        ],
        [
          "Compare",
          "building-blocks/logic/compare"
        ]
      ]
    },
    {
      "slug": "listas",
      "number": "05",
      "originalLesson": "6",
      "video": "pZAVmupXWhE",
      "duration": "8:29",
      "read": "13 min",
      "title": "Listas de elementos",
      "eyebrow": "Da célula capturada à leitura de todas as linhas",
      "description": "Explore o DOM de uma tabela, amplie a seleção para várias linhas e busque uma célula dentro de cada linha encontrada.",
      "objectives": [
        "Distinguir table, tr, th e td.",
        "Configurar a iteração com All.",
        "Entender o escopo de Source element e a saída Completed."
      ],
      "concepts": [
        [
          "Uma tabela é uma estrutura",
          "table contém a tabela; tr representa uma linha; th identifica uma célula de cabeçalho; td identifica uma célula de dados. Para ler uma coluna em várias linhas, primeiro identifique o conjunto de linhas."
        ],
        [
          "Capturar um exemplo é o começo",
          "A captura inicial pode fixar um texto ou uma posição. Para processar uma coleção, a estratégia deve representar o conjunto desejado."
        ],
        [
          "O escopo muda a busca",
          "Ao fornecer uma linha como Source element, a busca seguinte pode procurar a célula dentro daquela linha, em vez de repetir uma busca na página inteira."
        ]
      ],
      "flow": [
        "Find Web Element · All",
        "Get Web Text · célula",
        "Log Message"
      ],
      "flowNote": "Para cada linha: a saída principal dispara e Found element fornece a linha atual. Completed representa o término da coleção; conecte o resultado final a partir desse caminho.",
      "steps": [
        {
          "time": 137,
          "image": 200,
          "title": "Abra a tabela e capture uma célula de referência",
          "text": "O vídeo usa a página Challenging DOM do site The Internet. Abra-a com Start Web Browser e adicione Find Web Element. Como o cursor captura células com mais facilidade que linhas inteiras, comece por uma célula e abra Edit web element.",
          "observe": "A primeira captura aponta para um td com texto específico. Esse alvo ainda não representa a linha inteira nem todas as linhas da tabela.",
          "caption": "Captura inicial de uma célula como ponto de partida."
        },
        {
          "time": 193,
          "image": 255,
          "title": "Suba até a linha e amplie a estratégia",
          "text": "No Strategy Editor, clique em Validate para executar o localizador e carregar a estrutura disponível. Na árvore DOM, encontre o tr que contém a célula e capture a linha. Remova a restrição que prende a estratégia a uma única linha. Valide novamente e percorra as correspondências para conferir o conjunto selecionado.",
          "observe": "O editor mostra a árvore da tabela e a estratégia de linha. Evite remover condições demais e acabar incluindo cabeçalhos ou linhas de outra tabela.",
          "caption": "Inspeção da estrutura de linhas e do localizador no editor."
        },
        {
          "time": 291,
          "image": 305,
          "title": "Configure All para percorrer as ocorrências",
          "text": "No Find Web Element, escolha All em Use occurrence. A saída principal será disparada para cada correspondência, e Found element fornecerá a linha atual. Current index permite acompanhar a iteração; Completed indica quando a coleção terminou.",
          "observe": "A captura mostra o menu de ocorrência. Count informa o tamanho do conjunto; ele não substitui o processamento de cada item.",
          "caption": "Seleção das ocorrências a percorrer no bloco de localização."
        },
        {
          "time": 329,
          "image": 355,
          "title": "Forneça a linha como Source element",
          "text": "Acrescente Get Web Text e conecte Found element de Find Web Element a Source element. Quando a leitura usa a linha inteira como origem sem delimitar uma célula, o texto pode reunir vários campos da mesma linha. Use o log para observar esse resultado antes de refinar a busca.",
          "observe": "As conexões azul e verde ligam localização e leitura. O log mostra os dados de cada linha, ajudando a identificar se o alvo ficou amplo demais.",
          "caption": "Leitura inicial do conteúdo de cada linha encontrada."
        },
        {
          "time": 357,
          "image": 415,
          "title": "Restrinja a leitura à célula desejada",
          "text": "Capture a quarta célula e revise sua estratégia. No vídeo, a estratégia original inclui a quinta linha da tabela. Como Source element já fornece uma linha, remova a parte que fixa tbody e tr e mantenha a seleção relativa da célula desejada. Valide o comportamento em mais de uma linha.",
          "observe": "A estratégia em revisão ainda mostra a referência à linha e à quarta célula. O passo seguinte remove a dependência da linha capturada para tornar a leitura reutilizável durante a iteração.",
          "caption": "Revisão da estratégia de célula para retirar a referência fixa à linha."
        },
        {
          "time": 440,
          "image": 455,
          "title": "Registre os valores e finalize após a coleção",
          "text": "Conecte Text found a Log Message. Execute e confira se o log contém um valor da coluna desejada para cada linha, na ordem processada. Ao montar seu fluxo completo, use Completed para o término após todas as linhas. Um Pass no caminho de cada item encerraria o teste cedo demais.",
          "observe": "O fluxo mostra o ciclo de localização e leitura, com mensagens por item no log. A finalização por Completed é uma orientação prática complementar ao trecho demonstrado.",
          "caption": "Valores extraídos por linha no registro de atividades."
        }
      ],
      "pitfalls": [
        [
          "Texto fixo pode selecionar só uma linha",
          "Critérios ligados ao conteúdo de uma célula podem impedir que a estratégia cubra a coleção."
        ],
        [
          "A busca da célula precisa respeitar o escopo",
          "Se a linha já vem de Source element, uma referência absoluta à quinta linha pode produzir resultados incorretos."
        ],
        [
          "Não finalize na primeira ocorrência",
          "Reserve Pass para o resultado final, depois que a coleção terminar e os critérios do teste forem satisfeitos."
        ]
      ],
      "exercise": {
        "title": "Percorra uma pequena tabela mentalmente",
        "tasks": [
          "Desenhe três linhas com as colunas nome, cidade e status.",
          "Escolha a coluna cidade e descreva como acessá-la em cada linha.",
          "Explique a diferença entre o caminho de cada ocorrência e Completed."
        ],
        "answer": "Primeiro encontre as três linhas com uma estratégia comum e All. Para cada linha atual, use-a como Source element e leia sua segunda célula. A saída principal ocorre três vezes; Completed é o caminho de continuação após terminar a coleção."
      },
      "practice": "No Leapwork, use a página de exemplo referenciada nesta aula e leia uma coluna. Confira as correspondências no editor antes da execução e valide a quantidade de entradas produzidas no log.",
      "quiz": [
        {
          "q": "Qual tag representa uma linha de tabela?",
          "options": [
            "td",
            "tr",
            "th"
          ],
          "correct": 1,
          "why": "tr representa a linha; td é uma célula de dados e th é uma célula de cabeçalho."
        },
        {
          "q": "Para que serve Source element neste cenário?",
          "options": [
            "Para limitar a busca da célula à linha atual.",
            "Para abrir outro navegador.",
            "Para terminar o teste."
          ],
          "correct": 0,
          "why": "O elemento de origem define o escopo da busca seguinte."
        }
      ],
      "docs": [
        [
          "Find Web Element: All e Completed",
          "building-blocks/web/find-web-element"
        ],
        [
          "Get Web Text: Source element",
          "building-blocks/web/get-web-text"
        ],
        [
          "Strategy Editor",
          "working-with-leapwork/strategy-editor"
        ]
      ],
      "extra": [
        [
          "Tabela usada no vídeo",
          "https://the-internet.herokuapp.com/challenging_dom"
        ]
      ]
    },
    {
      "slug": "mobile",
      "number": "06",
      "originalLesson": "7",
      "video": "aGduKxCIZAk",
      "duration": "6:56",
      "read": "10 min",
      "title": "Páginas web móveis",
      "eyebrow": "O mesmo raciocínio em outra dimensão de tela",
      "description": "Configure a emulação de dispositivo no navegador e acompanhe um teste de busca com leitura numérica e comparação.",
      "objectives": [
        "Distinguir página web móvel de aplicativo nativo.",
        "Reconhecer o papel de Device type.",
        "Construir um critério numérico explícito para o teste."
      ],
      "concepts": [
        [
          "O alvo é uma página no navegador",
          "Esta aula trata de mobile web: uma página acessada com um perfil móvel. O roteiro não é um treinamento de automação de aplicativos nativos."
        ],
        [
          "Emulação tem um alcance definido",
          "Um perfil altera características do navegador, como dimensões e agente de usuário. Um teste emulado não comprova sozinho o comportamento em todo aparelho real."
        ],
        [
          "Reutilize a lógica e confira os alvos",
          "Digitar, clicar, ler e comparar continuam úteis. Um layout responsivo pode mudar controles e localizadores, então revise as correspondências no novo perfil."
        ]
      ],
      "flow": [
        "Start Web Browser · dispositivo",
        "Type Web Text",
        "Click Web Element",
        "Get Web Number",
        "Compare",
        "Pass / Fail"
      ],
      "flowNote": "O exemplo pesquisa por Lego e verifica se o total excede 2500. Esse número é um critério do vídeo, não uma expectativa atual garantida para a Amazon.",
      "steps": [
        {
          "time": 82,
          "image": 135,
          "title": "Configure o navegador e o tipo de dispositivo",
          "text": "Adicione Start Web Browser, escolha Chrome e informe a URL. Expanda Device type. O vídeo apresenta perfis de aparelhos e uma opção Other para personalizar dimensões, pixel ratio e user agent. A documentação atual chama a opção personalizada de Custom e descreve Device type para Chrome.",
          "observe": "O bloco expandido mostra os campos de perfil e dimensões. Nesta captura o menu está numa etapa de configuração personalizada, antes da execução com o perfil escolhido.",
          "caption": "Opções de dispositivo no bloco Start Web Browser."
        },
        {
          "time": 141,
          "image": 160,
          "title": "Observe o layout com o perfil móvel",
          "text": "Selecione o perfil do exemplo, Apple iPhone 7, e execute a abertura do navegador. A página passa a ser exibida numa área estreita. Observe onde ficaram busca, menus e resultados antes de registrar ações. A forma visual pode mudar com o perfil e com a versão atual do site.",
          "observe": "A página aparece em uma região estreita com uma anotação do próprio vídeo identificando a visualização do iPhone 7. Isso demonstra a apresentação emulada, não um aparelho físico conectado.",
          "caption": "Página da Amazon exibida no perfil móvel do exemplo."
        },
        {
          "time": 186,
          "image": 200,
          "title": "Registre a busca no layout móvel",
          "text": "Inicie o gravador a partir do navegador. Capture o campo de busca com Type Web Text, informe Lego e aplique. Em seguida, capture o ícone de pesquisa com Click Web Element. Os blocos de interação são os mesmos usados na automação web anterior.",
          "observe": "O menu de blocos está aberto sobre a busca. Se o layout esconder o campo atrás de um menu, a sequência precisa incluir a abertura desse menu antes da digitação.",
          "caption": "Seleção do bloco de digitação no campo de busca móvel."
        },
        {
          "time": 232,
          "image": 245,
          "title": "Capture o número de resultados",
          "text": "Após pesquisar, localize a informação de quantidade e capture-a com Get Web Number. Salve e feche o gravador. Confira se o elemento escolhido realmente contém o total desejado, e não outro número como preço, paginação ou quantidade de filtros.",
          "observe": "A captura mostra a seleção de Get Web Number na área de resultados. A posição desse total pertence à versão da página exibida no vídeo.",
          "caption": "Captura da informação numérica após a busca."
        },
        {
          "time": 254,
          "image": 280,
          "title": "Expresse o critério na comparação",
          "text": "Ligue Number found a Value A de Compare. Informe 2500 em Value B e configure Greater than, com interpretação numérica compatível com A. Encaminhe o caso verdadeiro a Pass e o caso incorreto a Fail. A comparação deve refletir o critério que você deseja testar.",
          "observe": "O Compare está expandido e mostra o método de comparação. Um teste de limite precisa definir o que fazer quando o valor é igual ao limite; Greater than não inclui a igualdade.",
          "caption": "Configuração da comparação com o limite de resultados do exemplo."
        },
        {
          "time": 306,
          "title": "Repita com outro perfil e avalie a evidência",
          "text": "O vídeo executa novamente com outro aparelho selecionado. Ao revisar seu teste, confira o elemento de busca, o total extraído e o caminho da comparação em cada perfil. Não conclua compatibilidade geral com base apenas em duas execuções demonstradas.",
          "observe": "Use o trecho vinculado para acompanhar a troca de perfil. Em uma execução real, resultados comerciais e o layout da Amazon podem variar; um site de teste controlado oferece dados mais previsíveis."
        }
      ],
      "pitfalls": [
        [
          "Não confunda emulação com validação de aparelho real",
          "Defina se o objetivo é conferir o layout emulado ou comprovar comportamento em um ambiente físico específico."
        ],
        [
          "O limite do vídeo não é um dado atual",
          "A quantidade de resultados de uma busca muda. Não use 2500 como promessa sobre o serviço hoje."
        ],
        [
          "Há diferença entre vídeo e documentação",
          "O vídeo cita Chrome e Edge; a referência atual de Start Web Browser descreve Device type para Chrome. Para este roteiro, use Chrome e confira a versão instalada."
        ]
      ],
      "exercise": {
        "title": "Especifique um teste responsivo",
        "tasks": [
          "Escolha dois tamanhos de tela para uma busca em uma página de exemplo.",
          "Defina a ação, o dado que será lido e o critério de aprovação.",
          "Anote uma limitação de executar o teste apenas em emulação."
        ],
        "answer": "Por exemplo: abrir dois perfis → buscar o mesmo termo → ler o total → confirmar que o valor é maior que zero. Isso verifica a jornada nesses perfis emulados; não garante características de todos os navegadores ou dispositivos reais."
      },
      "practice": "Quando tiver o Leapwork, reproduza a jornada em um ambiente de teste com dados previsíveis. Execute em dois perfis e revise as evidências individualmente.",
      "quiz": [
        {
          "q": "O teste mostrado nesta aula automatiza o quê?",
          "options": [
            "Uma página web em um perfil móvel emulado.",
            "Um aplicativo nativo instalado no telefone."
          ],
          "correct": 0,
          "why": "A jornada é executada no navegador com emulação de dispositivo."
        },
        {
          "q": "Com Greater than 2500, o valor 2500 atende ao critério?",
          "options": [
            "Sim.",
            "Não."
          ],
          "correct": 1,
          "why": "Greater than exige um valor estritamente maior. Igualdade precisaria de outro critério."
        }
      ],
      "docs": [
        [
          "Start Web Browser: Device type",
          "building-blocks/web/start-web-browser"
        ],
        [
          "Get Web Number",
          "building-blocks/web/get-web-number"
        ],
        [
          "Compare",
          "building-blocks/logic/compare"
        ]
      ]
    }
  ]
};

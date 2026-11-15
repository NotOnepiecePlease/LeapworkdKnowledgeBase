"""Gera fichas editoriais em português a partir do inventário público conferido."""
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PREFIX='https://docs.leapwork.com/leapwork-flow/latest/'
SECTIONS={
 'What is Leapwork?':'Visão geral e arquitetura','Download and install':'Download e instalação',
 'Working with Leapwork':'Uso da ferramenta','Building Blocks':'Catálogo de blocos',
 'Administration':'Administração','Leapwork Public REST APIs':'API REST',
 'Customer Portal':'Portal do cliente','Release Notes':'Notas de versão'
}
# Resumos autorais. Os artigos originais continuam na fonte; não são espelhados no site.
SUMMARIES={
 'what-is-leapwork':'Apresenta a automação visual por fluxos reutilizáveis e a separação entre ações e verificações. É a entrada para entender a arquitetura antes de escolher instalação e licenciamento.',
 'what-is-leapwork/architecture-overview':'Distingue Flow, Controller e Agent, os canais de comunicação e as implantações local, híbrida e em nuvem. Explica a diferença entre SQLite na edição Platform e SQL Server na Enterprise, além da infraestrutura gerenciada quando aplicável.',
 'what-is-leapwork/licensing-and-deployment':'Relaciona modelos de implantação e licenças aos componentes disponíveis. Use a comparação para identificar responsabilidades por infraestrutura, recursos contratados e condições de execução antes de dimensionar um ambiente.',
 'download-and-install':'Organiza os caminhos de obtenção, verificação de requisitos e instalação. Escolha o guia pela edição e pelo modelo de implantação, em vez de executar um procedimento de outra configuração.',
 'download-and-install/download':'Relaciona matriz de atualização, requisitos e obtenção do instalador. A sequência ajuda a escolher uma versão compatível e consultar suas mudanças antes de modificar o ambiente.',
 'download-and-install/download/upgrade-matrix':'Concentra versões principais e de serviço, destaques e links para notas completas. Serve ao planejamento de atualização; uma versão mais nova ainda precisa ser confrontada com os requisitos e a implantação atual.',
 'download-and-install/download/system-requirements':'Reúne requisitos e ambientes qualificados. Confira sistema operacional, drivers e pré-requisitos na tabela vigente e teste mudanças em ambiente controlado; não use a lista histórica de outro guia como garantia de suporte atual.',
 'download-and-install/download/download-leapwork':'Explica como obter instaladores oficiais no Customer Portal e acessar versões e notas de lançamento. Diferencia versões principais e de serviço para apoiar a escolha do pacote correto.',
 'download-and-install/installation':'Ajuda a escolher o roteiro de instalação por edição, avaliação e implantação. A localização de Controller e Agents e as responsabilidades da equipe precisam estar definidas antes de seguir um procedimento.',
 'download-and-install/installation/leapwork-cloud':'Orienta a instalação local do Flow e a conexão com Controller e Agents hospedados no serviço de nuvem. A conexão depende dos dados e pré-requisitos fornecidos para o ambiente contratado.',
 'download-and-install/installation/leapwork-trial':'Descreve instalação e ativação da avaliação, seleção dos componentes e primeiros acessos. A avaliação não deve ser confundida com a instalação de uma infraestrutura Enterprise definitiva.',
 'download-and-install/installation/leapwork-platform':'Descreve os componentes da edição Platform e o armazenamento SQLite incorporado. Compare os requisitos publicados com a lista vigente de ambientes qualificados antes de instalar ou atualizar.',
 'download-and-install/installation/leapwork-enterprise':'Detalha a implantação Enterprise, separação de componentes, rede e banco SQL Server. O licenciamento do banco não está incluído no do Leapwork; infraestrutura e acessos precisam ser planejados com a equipe responsável.',
 'download-and-install/installation/offline-installation':'Apresenta o fluxo de instalação e ativação sem acesso direto à internet na máquina de destino. A obtenção e a transferência do pacote e dos dados de ativação fazem parte do procedimento específico.',
 'download-and-install/installation/silent-installation':'Explica instalação silenciosa por MSI, parâmetros e registros de instalação. Use valores do ambiente e trate licença e credenciais fora de scripts compartilhados; os comandos da fonte são exemplos, não instruções prontas para qualquer máquina.',
 'download-and-install/installation/mobile-installation-guide':'Reúne preparação da automação móvel em iOS e Android, dispositivos e provedores. Mobile exige conexões e configuração próprias; testar páginas Web em tamanho móvel não equivale a automatizar um aplicativo nativo.',
 'download-and-install/installation/leapwork-on-azure-marketplace-installation':'Descreve o caminho Enterprise pelo Azure Marketplace e os requisitos de assinatura, funções e licença. O procedimento depende dos acessos e recursos da organização no Azure.',
 'download-and-install/installation/install-leapwork-flow-from-the-command-line':'Apresenta o instalador CLI com executável e ZIP correspondentes, seleção de componentes e operações de instalar, atualizar, reparar e remover. Confira parâmetros e responsabilidades administrativas antes de automatizar a instalação.',
 'working-with-leapwork':'Reúne os recursos de criação, organização, execução, análise e manutenção. Use o índice para sair da visão geral e localizar o guia da operação específica.',
 'working-with-leapwork/introducing-leapwork-flow':'Apresenta o editor visual, blocos, gravadores e consulta de resultados. Ajuda a reconhecer as áreas da interface e a relação entre construir um fluxo e verificar sua execução.',
 'working-with-leapwork/organizing-your-work':'Explica a árvore de pastas e ativos: fluxos, sub-flows, arquivos, elementos capturados e coleções de imagens. Uma estrutura explícita facilita encontrar dependências e componentes reutilizáveis.',
 'working-with-leapwork/designing-automation-flows':'Detalha construção, conexões, execução e colaboração no canvas. Inclui histórico e as diferenças entre restaurar somente a lógica, restaurar lógica e Locators ou recuperar em uma cópia.',
 'working-with-leapwork/designing-automation-flows/flows':'Lista ações do menu de um fluxo, incluindo edição, execução, uso, histórico, transferência e organização. Distingue o ativo de automação de seus elementos e dependências.',
 'working-with-leapwork/designing-automation-flows/sub-flows':'Explica como extrair, organizar, parametrizar e reutilizar componentes. Entradas e saídas de valor e execução compõem o contrato que os fluxos consumidores precisam respeitar.',
 'working-with-leapwork/designing-automation-flows/ai-flow-builder':'Apresenta a criação e a análise assistidas por instruções em linguagem natural. As propostas precisam de revisão e teste: o recurso não configura automaticamente todos os acessos nem conhece regras de negócio não informadas.',
 'working-with-leapwork/storage-overview':'Explica armazenamento de definições, anexos e artefatos no modelo de serviço. A página destaca a disponibilidade para Cloud Agents; não se deve presumir suporte equivalente em Agents locais.',
 'working-with-leapwork/agents-overview':'Descreve tipos de Agent, cadastro, autenticação, conexão e seleção dos recursos de execução. As capacidades variam entre Remote Agent, Cloud e provedores de teste; uma conexão válida não comprova o funcionamento da aplicação.',
 'working-with-leapwork/agents-overview/scheduling-assistant':'Apresenta a visualização de disponibilidade e uso dos Agents para planejar agendamentos. Use o contexto de ocupação para revisar conflitos e capacidade antes de aumentar a frequência das execuções.',
 'working-with-leapwork/run-lists':'Explica agrupamento de fluxos em passos, condições, cópia, transferência e retry. Copiar a lista mantém referências aos fluxos; alterar um fluxo compartilhado pode afetar mais de uma lista.',
 'working-with-leapwork/run-lists/schedules':'Relaciona gatilho, fuso, recorrência, distribuição de Agents, variáveis, ações e conflitos. Diferencia repetir todos os fluxos em cada Agent, repartir a coleção e usar o primeiro recurso disponível.',
 'working-with-leapwork/run-lists/understanding-the-flow-report':'Descreve o PDF de uma execução agendada, com identificação, contexto, versão e quadros relevantes. Confira disponibilidade e configuração do recurso; ele não deve ser presumido em toda prévia manual.',
 'working-with-leapwork/reporting':'Explica agrupamento e filtro dos resultados, exportação e investigação por vídeo, canvas e Activity log. Cor e estado resumem o resultado; a causa exige consultar a execução correta e suas evidências.',
 'working-with-leapwork/dashboards':'Apresenta widgets de tendência, maior incidência de falhas e distribuição dos resultados. Período e filtros de fluxos, Agents e listas definem a população efetivamente exibida.',
 'working-with-leapwork/wip-smart-recorder':'Explica a gravação interativa, com seleção de ações e construção posterior dos blocos. As ações escolhidas acontecem durante a gravação; revise o fluxo gerado e acrescente verificações do resultado esperado.',
 'working-with-leapwork/smart-mobile-recorder':'Descreve gravação de ações em aplicativos móveis após configurar conexão e dispositivo. Distingue interações por elementos e imagens e gera os blocos para posterior revisão.',
 'working-with-leapwork/d365-fusion-recorder':'Apresenta o gravador voltado ao Dynamics 365 Finance and Operations no navegador. O contexto de captura e os blocos Fusion são específicos dessa tecnologia e precisam ser revistos antes de reutilização.',
 'working-with-leapwork/salesforce-fusion-recorder':'Explica gravação de processos Salesforce na versão Web usando o gravador específico. Não se aplica a aplicativos Desktop ou sessões virtuais; o fluxo gerado ainda precisa de validação.',
 'working-with-leapwork/teams':'Explica a separação e a colaboração entre equipes no mesmo Controller, com seleção de equipe e ativos correspondentes. Confira o contexto ativo antes de editar ou compartilhar recursos.',
 'working-with-leapwork/workflow-management':'Relaciona estados, responsáveis, revisão e publicação à governança dos fluxos. Um estado editorial descreve o processo de manutenção; não substitui a evidência de execução de um caso.',
 'working-with-leapwork/microsoft-ado-test-plan-integration':'Descreve importação e sincronização de casos e planos ADO, execução, publicação de resultados e registro de bugs. Confira elegibilidade e diferencie sincronizar existentes de importar novos casos.',
 'working-with-leapwork/strategy-editor':'Explica como inspecionar e ajustar estratégias de localização. A finalidade é reconhecer a identidade do elemento em situações variáveis, sem depender apenas de um índice ou posição aparentemente convenientes.',
 'working-with-leapwork/fix-and-update-elements-directly-in-fusion-recorder':'Apresenta correção e atualização de elementos pelo contexto do Fusion Recorder. Confira o alvo e o impacto da alteração nos passos que reutilizam o elemento antes de considerar o fluxo reparado.',
 'working-with-leapwork/ocr-engine-selection-guide':'Compara OCR 3.0 e Neural Processor em velocidade e tratamento de interfaces visuais. A escolha depende da tela e da configuração; os nomes podem diferir dos motores mostrados nos vídeos antigos do caderno.',
 'working-with-leapwork/nested-dropdowns-in-dynamics-365-finance-and-operations':'Explica controles dependentes no D365 F&O, como uma opção que muda após a seleção de outra. O suporte descrito exige versão compatível e configuração do gravador/bloco pertinente.',
 'working-with-leapwork/bulk-actions-in-flow':'Reúne operações sobre vários ativos para reduzir manutenção repetitiva. Confira seleção, alcance e consequências antes de aplicar uma ação em lote a recursos compartilhados.',
 'working-with-leapwork/await-dom-change-and-await-requests-in-fusion-blocks':'Distingue aguardar mudanças no DOM e aguardar requisições nos blocos Fusion. Escolher a condição de prontidão correta ajuda a evitar que a próxima ação ocorra antes da atualização necessária.',
 'working-with-leapwork/git-version-control':'Organiza os guias de versionamento Git, configuração de provedores e diagnóstico de sincronização. Esse recurso é configurado no Leapwork e não é ativado ao baixar o caderno do GitHub.',
 'working-with-leapwork/git-version-control/use-git-versioning-for-flows-and-subflows':'Explica o mapeamento de equipe e repositório, credenciais, migração e consulta de versões Git. A migração tem limites e consequências sobre histórico e relatórios; confira-os antes de habilitar o recurso.',
 'working-with-leapwork/git-version-control/set-up-github-for-git-versioning':'Descreve preparação do repositório GitHub, acesso de equipe e credenciais para versionar fluxos. A conta precisa de permissão real para escrever, e as regras do repositório devem permitir a operação esperada.',
 'working-with-leapwork/git-version-control/set-up-azure-devops-for-git-versioning':'Orienta preparação de repositório e credenciais Azure DevOps para versionamento Git. Esse uso é distinto da integração ADO que relaciona casos e resultados de teste.',
 'working-with-leapwork/git-version-control/set-up-bitbucket-cloud-for-git-versioning':'Explica preparação de workspace, repositório e tokens compatíveis com Bitbucket Cloud. Confira os tipos de token aceitos na versão, em vez de reutilizar um mecanismo antigo de autenticação.',
 'working-with-leapwork/git-version-control/check-git-sync-status-and-resolve-upload-failures':'Diferencia Success, Error, Warning e Deprecated e orienta investigação da fila e dos acessos. Salvar uma versão e confirmar seu envio são verificações separadas.',
 'working-with-leapwork/leapwork-update-center':'Apresenta distribuição centralizada de pacotes aos componentes conectados e acompanhamento do estado. Atualização e rollback dependem de pacote, papel administrativo e contexto compatíveis.',
 'administration':'Organiza configurações de Controller, identidade, segurança, integração, padrões, licença e diagnóstico. A disponibilidade de cada ajuste depende das permissões, edição e implantação.',
 'administration/controller-settings':'Explica identificação e conexão dos Controllers. Cada Controller é independente em licença e acesso; confira o ambiente selecionado antes de qualquer alteração.',
 'administration/user-management':'Descreve contas locais, acesso por diretório/SSO e papéis de usuário. O acesso efetivo também depende de Privileges Settings e das configurações de identidade do ambiente.',
 'administration/emergency-admin-user':'Documenta a conta administrativa de emergência, sua configuração e políticas. É um procedimento do responsável pela instalação, a ser conhecido e validado sem modificar credenciais durante o estudo.',
 'administration/team-management':'Explica criação e edição de equipes Enterprise. Remover um integrante é diferente de excluir a equipe: a exclusão tem consequências permanentes sobre os ativos associados.',
 'administration/wip-security':'Apresenta complexidade, tamanho e expiração de senha para contas geridas no Leapwork. Mudanças nessa política afetam usuários e precisam considerar a administração de acesso do ambiente.',
 'administration/privileges-settings':'Permite ajustar execução por Readers, scripts de agendamentos e capacidades de Contributors. Confira as opções efetivas; o nome do papel sozinho não descreve todas as permissões.',
 'administration/workflow-stettings':'Configura comentários de alteração, estados de revisão e comportamento ao editar ativos publicados. A política torna a intenção e o responsável pelas mudanças mais rastreáveis.',
 'administration/api-access-keys':'Descreve criação administrativa de chaves e seleção de escopos da API. A chave representa um acesso de integração e deve ser guardada fora de código, imagens e logs compartilhados.',
 'administration/e-mail-settings':'Explica os protocolos e dados necessários para notificações, com SMTP e OAuth. Testar conexão e confirmar recebimento são evidências diferentes, e o suporte aos botões varia por protocolo.',
 'administration/proxy-settings':'Centraliza a configuração de proxy do componente pertinente. Uma URL acessível no navegador pessoal não demonstra acesso equivalente no contexto do Controller ou da execução.',
 'administration/database-decryption-keys':'Explica a chave necessária para acessar dados SQLite recuperados em outro Controller. Sua guarda integra o plano de recuperação e não deve ser confundida com uma chave da API.',
 'administration/database-management':'Apresenta correções específicas de revisões e conectores de sub-flows após atualizações. Esses recursos de manutenção não equivalem a backup ou recuperação integral do ambiente.',
 'administration/default-flow-settings':'Reúne padrões de gravação, duração, OCR, navegação e outras tecnologias. Distingue escolher um padrão de aplicar uma mudança aos fluxos existentes por atualização em lote.',
 'administration/wip-web-settings':'Explica a limitação de estratégias de captura Salesforce e sua contagem. A configuração descrita é específica; não representa todos os ajustes possíveis de qualquer automação Web.',
 'administration/wip-capture-settings':'Configura tempo de inspeção, busca de navegador e comportamento de captura. Limites de captura não são os mesmos limites da execução de um bloco ou do fluxo inteiro.',
 'administration/retention-policies':'Distingue retenção de resultados, vídeos, temporários, auditoria e versões, com escopos de equipe ou globais. A limpeza precisa preservar as evidências ainda necessárias à investigação.',
 'administration/license-management':'Apresenta recursos da licença e ações de consulta, atualização e desativação. Uma licença corresponde a um Controller; retirar a última licença pode impedir o acesso ao ambiente.',
 'administration/audit-log':'Permite filtrar e exportar eventos administrativos e de execução por período e contexto. Não é o mesmo registro que o Activity log dos blocos de um run específico.',
 'administration/other-settings':'Reúne preferências adicionais, como a solicitação de feedback. Separe uma preferência de interface das configurações que alteram acesso ou execução.',
 'administration/connections':'Organiza integrações de identidade, mobile, serviços e provedores externos. Escolha o tipo correspondente ao objetivo e confira conta, rede e permissões do serviço envolvido.',
 'administration/connections/headspin-server-connection':'Configura acesso a dispositivos móveis disponibilizados pelo HeadSpin, usando os dados do provedor. Requer assinatura e credenciais próprias, além de permissão administrativa no Leapwork.',
 'administration/connections/appium-server-connection':'Conecta a um servidor Appium acessível ao Leapwork para automação móvel. O servidor e os dispositivos precisam estar preparados; cadastrar a conexão não instala essa infraestrutura.',
 'administration/connections/saucelabs-server-connection':'Descreve conexão Sauce Labs com datacenter, host e credenciais para testes móveis. Confira capacidade e contexto do provedor antes de associar a um caso.',
 'administration/connections/browserstack-server-connection':'Configura acesso móvel ao BrowserStack, com credenciais e capacidades opcionais. O dispositivo e as propriedades escolhidos precisam corresponder ao cenário de teste.',
 'administration/connections/lambdatest-server-connection':'Descreve a conexão móvel identificada na fonte como TestMu AI, anteriormente LambdaTest. Confira o nome exibido, endpoint e credenciais do serviço na versão utilizada.',
 'administration/connections/azure-active-directory-server-connection':'Orienta a conexão com Entra ID/Azure AD por registro de aplicativo e identidade corporativa. O acesso ao diretório deve ser preparado com a administração da organização.',
 'administration/connections/lightweight-directory-server':'Descreve conexão LDAP para usuários e grupos de diretório. A fonte alerta que alternar entre AD e LDAP tem consequências sobre usuários existentes e não deve ser tratado como troca inofensiva.',
 'administration/connections/wip-microsoft-graph-sharepoint-connection':'Configura Microsoft Graph/SharePoint para acesso a arquivos Excel no serviço. Tenant, aplicativo e autorização precisam permitir o acesso ao arquivo pretendido.',
 'administration/connections/single-sign-on-sso-connection':'Apresenta o fluxo de configuração SSO entre a equipe de TI, o provedor de identidade e Leapwork. Centralizar autenticação é diferente de configurar atribuição de papéis por grupos.',
 'administration/connections/azure-devops-ado-server-connections':'Descreve URL, PAT e permissões para integrar casos e resultados ADO. Essa credencial externa não substitui AccessKey da API do Controller.',
 'administration/wip-azure-devops-connections':'Reúne ajustes da integração Azure DevOps e dos campos usados ao registrar bugs. Confira a conexão e o mapeamento exigido pelo projeto de destino.',
 'administration/mobile-configuration':'Define o contexto móvel que os blocos e gravadores utilizarão. A conexão ao serviço e a configuração do dispositivo são pré-requisitos distintos.',
 'administration/active-directory-settings':'Explica integração por florestas ou domínios específicos e suas consequências. Desabilitar descoberta pode remover acessos e vínculos; revise o impacto antes de alterar um ambiente real.',
 'administration/diagnostics':'Apresenta coleta de logs e informações de prontidão por componente e período. Escolher alvos e janela pertinentes reduz ruído e ajuda a relacionar o diagnóstico ao incidente.',
 'public-rest-apis':'Apresenta a API v4 no Controller, sua base e autenticação por AccessKey. Uma chamada atendida não comprova que um run terminou ou que seus itens passaram.',
 'public-rest-apis/api-endpoints':'Disponibiliza a especificação OpenAPI. O catálogo complementar deste caderno inclui todas as operações do arquivo consultado, seus parâmetros e esquemas de retorno, sem executar chamadas.',
 'customer-portal':'Organiza os guias públicos do Customer Portal: licença, downloads, suporte, uso e serviços adicionais. Consultar estes artigos não significa acessar os dados privados de uma conta.',
 'customer-portal/what-is-customer-portal':'Apresenta o portal de relacionamento e serviços para clientes. Licenças, utilização, solicitações e suporte são reunidos num contexto de conta autenticada.',
 'customer-portal/add-ons':'Descreve solicitação e ativação de Cloud Agents, Cloud Blocks e AI Blocks e seus estados. A presença de um bloco na documentação não comprova que o recurso está ativo no tenant.',
 'customer-portal/data-sharing':'Explica os tipos de informações de conta e utilização compartilhados pelo portal. Consulte os campos e sua finalidade para entender o contexto da coleta; o caderno não envia dados ao portal.',
 'customer-portal/downloads':'Reúne acesso a instaladores estáveis, utilitários, links e versões arquivadas. Relacione o pacote escolhido às notas de versão e aos requisitos antes de distribuí-lo à equipe de instalação.',
 'customer-portal/my-cases':'Explica como acompanhar casos de suporte, seus estados, comentários e novas solicitações. Um relato com contexto e evidências ajuda a tornar a investigação reproduzível.',
 'customer-portal/my-licenses':'Apresenta identificação, estado e utilização das licenças, incluindo possibilidades de ativação offline. Os dados reais dependem da conta autenticada e não estão incluídos neste caderno.',
 'customer-portal/reports-section':'Descreve painéis de licenças, atividade e resultados no portal. Diferencie essas métricas de serviço do relatório detalhado de um fluxo no Flow.',
 'release-notes':'Relaciona os lançamentos publicados no menu consultado. As fichas seguintes registram o recorte da varredura; não representam uma promessa de que futuras versões manterão os mesmos recursos.',
 'release-notes/leapwork-flow-major-release-2026-3':'Destaca versionamento Git, instalador CLI, modernização de runtime para .NET 10 e ajustes de IA e aplicações empresariais. Planeje compatibilidade e atualização pelos requisitos e detalhes da versão.',
 'release-notes/leapwork-flow-major-release-2026-2':'Reúne melhorias de criação assistida, produtividade, integração, armazenamento e diagnóstico. A família 2026 também atualiza nomes de produtos; diferencie Flow de Play ao consultar outro material.',
 'release-notes/leapwork-flow-service-release-2026-1-130':'Apresenta uma versão de serviço voltada a confiabilidade, armazenamento, agendamento e blocos Fusion. Consulte os detalhes e requisitos antes de tratá-la como equivalente à versão principal anterior.',
 'release-notes/leapwork-flow-major-release-version-2026-1':'Reúne mudanças em criação assistida, recursos de IA, governança e escala. A versão dos vídeos do treinamento pode ser anterior; compare a função e a documentação, não apenas a posição visual dos controles.'
}

CATEGORIES={
 'ai-blocks':('Inteligência artificial','Ações, extração, geração, transformação e validação com IA. Revise contrato, resultado e disponibilidade do recurso; uma resposta gerada não é evidência suficiente de correção.'),
 'cloud':('Processamento de documentos na nuvem','Conversão e extração de conteúdo e metadados de arquivos. A fonte condiciona o uso à ativação de Cloud Blocks no tenant e sinaliza recursos experimentais.'),
 'data-driven':('Fontes e saída de dados','Arquivos, planilhas, banco, comandos e HTTP alimentam fluxos ou recebem resultados. Confira formato, acesso no contexto de execução e comportamento de falha.'),
 'debugging':('Observação e diagnóstico','Comentários, mensagens, capturas e medidas de tempo ajudam a compreender o fluxo. Um log registra uma observação e não aprova automaticamente a regra testada.'),
 'desktop-ui':('Aplicações Desktop','Elementos e janelas de aplicações Windows são identificados para interação e leitura. Verifique a janela ativa e a identidade do controle.'),
 'dynamics-365':('Dynamics 365 Finance and Operations','Blocos especializados para login, captura, controles e validação no D365 F&O. Requerem contexto e versão compatíveis com a tecnologia Fusion.'),
 'electron-blocks':('Aplicações Electron','Inicialização, janelas, elementos, dados e eventos em aplicações Electron. Distingue o processo da aplicação do contexto de janela em uso.'),
 'error-handling':('Tratamento de erros','Define uma resposta global a erros não tratados pelo caminho específico de um bloco. Planeje diagnóstico e recuperação sem transformar falha em aprovação implícita.'),
 'generators':('Geração de entradas','Fornece valores numéricos, senhas e datas. Registre o que precisa ser reproduzível e não confunda aleatoriedade com unicidade garantida.'),
 'green-screen':('Terminais e mainframe','Interage com sessões, campos, tabelas e cursor de terminais. Uma sessão precisa existir antes da conexão; os blocos são distintos da automação por imagem da janela.'),
 'image-and-text-recognition':('Imagens e OCR','Localiza imagens e textos e extrai valores visíveis. Região, resolução e motor influenciam o resultado; leia também o guia atual de escolha de OCR.'),
 'logic':('Lógica e transformação','Controla caminhos, repetições, cálculos, texto, datas e recursos auxiliares. Confira tipos, saídas de conclusão e caminhos de erro.'),
 'mobile':('Aplicações móveis','Conecta dispositivos e instala, inicia e controla aplicações e telas móveis. Precisa de conexão e configuração específicas de iOS ou Android.'),
 'module-input-and-output':('Contratos de componentes','Entradas e saídas distinguem dados de caminhos de execução. Um sub-flow reutilizável precisa deixar explícito o que recebe e o que devolve.'),
 'mouse-and-keyboard':('Mouse e teclado','Ações por imagem, texto, posição e teclas atuam na interface visível. Confira foco, alvo e estado da sessão antes de enviar entradas.'),
 'multi-factor-authenticator':('Autenticação multifator','Inclui geração de código TOTP quando a conta e o provedor permitem configuração compatível. O segredo precisa ser protegido e o procedimento depende da política de identidade.'),
 'salesforce':('Salesforce','Blocos especializados para login, campos, seleção e validação de elementos Salesforce. Use o contexto da aplicação e confira requisitos de autenticação e versão.'),
 'sap':('SAP','Sessões, ações, textos e tabelas SAP exigem configuração adequada do aplicativo. Valide o contexto da sessão e o resultado após cada operação.'),
 'setting-values':('Valores explícitos','Cria entradas de texto, número, data, posição e área para outros blocos. Definir um valor não executa por si só uma ação na aplicação.'),
 'start-stop':('Início e resultado do fluxo','Start inicia o caminho; Pass, Fail e Done expressam encerramentos distintos. Done não deve ser interpretado como Passed.'),
 'system':('Sessão e contexto do Agent','Consulta informações da execução e controla login, bloqueio e encerramento da sessão do Agent. A sessão Windows é distinta da conta usada no editor.'),
 'variables':('Estado compartilhado','Define e lê valores com escopo. O tempo de vida e o contexto de uma variável influenciam o isolamento entre execuções.'),
 'web':('Navegador e aplicações Web','Inicialização, navegação, leitura, controles, cookies e scripts no navegador. Confira a janela em uso e a correspondência do elemento com o registro correto.')
}

SPECIAL={
 'AI Action':'Executa uma tarefa descrita por instruções usando o recurso de IA. Confira a intenção, o contexto e o resultado observável antes de reutilizar a ação.',
 'AI Extract':'Extrai informações a partir do conteúdo fornecido com auxílio de IA. Defina o formato de saída e confira os valores antes de alimentar uma decisão.',
 'AI Generate':'Gera conteúdo ou dados de teste conforme as instruções configuradas. Valide formato e adequação das entradas; o resultado não se torna correto apenas por ter sido gerado.',
 'AI Transform':'Transforma o conteúdo informado de acordo com instruções. Compare a saída com o contrato de formato e preserve a entrada necessária à investigação.',
 'AI Validate':'Avalia uma condição por instruções de validação assistida. Escreva critérios observáveis e confira o comportamento em exemplos positivos e negativos.',
 'AI Vision Extract':'Extrai informações visuais com IA a partir do contexto de imagem indicado. Confira região e formato dos valores retornados.',
 'AI Vision Validate':'Avalia uma condição visual com IA. Compare o critério com o conteúdo da imagem e trate resultados divergentes explicitamente.',
 'Convert to JSON':'Converte formatos estruturados compatíveis em JSON. Confira o formato da origem e o contrato da saída antes de repassar os dados.',
 'Convert to PDF':'Converte um arquivo compatível para PDF. O artefato retornado precisa ser salvo pelo mecanismo pertinente quando o objetivo é obter um arquivo local.',
 'Convert to Text':'Transforma documentos compatíveis em texto. Confira se o formato e o conteúdo da origem atendem aos requisitos da conversão.',
 'Document Information':'Extrai metadados de um documento, como autoria, datas e quantidade de páginas. Use os campos retornados numa comparação explícita.',
 'Extract Document Text':'Extrai texto de documentos e imagens compatíveis com OCR. A leitura depende do formato e da qualidade da origem.',
 'Command-line':'Executa um comando no contexto configurado e disponibiliza seu retorno. Confira código e conteúdo retornados, sem presumir sucesso apenas porque o comando foi iniciado.',
 'Compress File':'Compacta o arquivo indicado. Confira origem, destino e existência do artefato resultante.',
 'Database':'Executa uma operação de banco pela conexão ODBC configurada. Confira consulta, acesso, colunas e comportamento quando não há dados ou ocorre erro.',
 'HTTP Request':'Envia uma requisição HTTP e fornece dados da resposta. Separe ausência de resposta, estado HTTP e validação do conteúdo retornado.',
 'Read Excel':'Lê linhas e colunas de uma planilha definida por origem e intervalo. Diferencie a saída por linha, a conclusão da leitura e o tratamento de falha.',
 'Write Excel':'Grava valores em colunas de um intervalo Excel. Confira método por índice ou acréscimo para evitar atualização da linha errada ou duplicação de resultados.',
 'Save File':'Salva o conteúdo recebido em File Input no armazenamento gerenciado pelo Leapwork, com nome gerado automaticamente. A referência não exige um caminho manual de destino; confira o artefato desta execução e trate Not saved.',
 'Send E-Mail':'Prepara e envia uma mensagem conforme as propriedades e a configuração de comunicação. Confirme destinatário e evidência de entrega no cenário de teste.',
 'Set File':'Fornece uma referência de arquivo para outras operações do fluxo. O caminho ou origem precisa estar disponível ao componente que o utilizará.',
 'Comment':'Documenta a intenção ou organização do fluxo sem substituir uma ação ou verificação funcional.',
 'Log Message':'Registra uma mensagem para acompanhar valores e contexto da execução. Evite incluir segredos ou dados desnecessários.',
 'Log Screenshot':'Registra uma captura visual para diagnóstico. A imagem precisa ser relacionada ao caso e ao instante pertinente.',
 'Stopwatch':'Mede tempo no fluxo para apoiar observação e comparação. Defina exatamente qual intervalo está sendo medido.',
 'Any Error':'Define o caminho global de erro do fluxo ou sub-flow. A referência limita a um handler por contexto e descreve propagação ao pai quando o sub-flow não possui tratamento próprio.',
 'Generate date/time':'Fornece a data e a hora atuais do sistema da execução, além dos seus componentes. Para um teste com instante fixo, use uma data-base controlada em vez de tratar o relógio atual como uma entrada fixa.',
 'Generate Number':'Produz valores numéricos conforme as opções configuradas. Uma geração aleatória não garante identidade exclusiva entre execuções.',
 'Generate Password':'Gera uma senha conforme os critérios disponíveis. Confira requisitos do teste sem registrar um segredo real em evidências compartilhadas.',
 'Break Iteration':'Interrompe uma iteração conforme a lógica conectada. Diferencie saída antecipada de término normal do conjunto.',
 'C# Code':'Executa uma extensão C# no fluxo com campos e referências configurados. Use o template compatível com a versão e teste entrada válida e erro.',
 'Calculate':'Calcula uma expressão a partir dos valores fornecidos. Confira tipos, unidades e arredondamento antes de validar o resultado.',
 'Change Text':'Transforma texto pelas opções configuradas. Preserve significado e formato necessários ao contrato do caso.',
 'Close Windows':'Tenta encerrar janelas conforme as propriedades configuradas. A ausência da janela não comprova o sucesso funcional da operação anterior.',
 'Compare':'Compara valores e direciona a execução pelo resultado. Tipos e método de comparação precisam refletir a regra pretendida.',
 'Get Clipboard':'Lê o conteúdo da área de transferência. Confirme que o dado pertence à operação atual e ao contexto correto.',
 'Set Clipboard':'Define o conteúdo da área de transferência para uso posterior. Planeje o isolamento quando outros processos usam o mesmo recurso.',
 'Loop':'Controla repetições e sua conclusão. Defina limites e caminhos de saída para evitar laços sem término previsto.',
 'Offset Area':'Calcula uma área relativa a uma referência. Confira dimensões e coordenadas antes de usar a área em ações visuais.',
 'Offset Position':'Calcula uma posição relativa a uma referência. A relação geométrica precisa continuar válida no contexto da tela.',
 'Offset Date/Time':'Aplica um deslocamento à data/hora de referência. Confira unidade, calendário e fronteiras do caso.',
 'Regular Expression':'Extrai ou reconhece padrões de texto com expressão regular. Trate ausência e múltiplas correspondências em vez de assumir um único resultado.',
 'Switch':'Escolhe um caminho por comparação com os casos definidos. No match trata entradas que não correspondem a nenhum caso.',
 'Wait':'Pausa a execução por um intervalo. O tempo decorrido não comprova que a aplicação atingiu o estado necessário.',
 'Execution Input':'Define uma entrada de execução de um componente. Não é uma entrada de dados.',
 'Execution Output':'Expõe um caminho de execução de saída de um componente. Nomeie o significado de cada resultado para seus consumidores.',
 'Value Input':'Recebe um valor no contrato de um componente. Defina significado, tipo e momento em que ele será usado.',
 'Value Output':'Expõe um valor produzido por um componente. Confira como ele se relaciona ao caminho de execução.',
 'Time-based one-time password':'Gera um código TOTP com segredo e configuração compatíveis com a identidade de teste. A fonte alerta sobre restrições de provedores; não é um mecanismo para contornar autenticação.',
 'Start':'Marca o início do caso e pode preparar o estado de janelas conforme a ação escolhida. Defina esse comportamento antes de conectar as etapas.',
 'Done':'Encerra o caso sem classificá-lo como Passed ou Failed. Uma integração precisa interpretar esse estado conforme sua política.',
 'Fail':'Encerra o caso no estado Failed, com contexto de diagnóstico quando configurado.',
 'Pass':'Encerra o caso no estado Passed. A lógica anterior precisa ter realizado as verificações que sustentam essa classificação.',
 'Get Agent Session':'Fornece informações do fluxo, da lista e do Agent em execução. Os valores podem apoiar logs e decisões de contexto.',
 'Lock':'Bloqueia a sessão Desktop da conta usada no Agent. Não equivale a um mecanismo genérico de bloqueio de variáveis ou recursos compartilhados.',
 'Login':'Efetua login de sistema na máquina do Agent com a identidade configurada. É distinto do login no editor ou na aplicação testada.',
 'Logout':'Encerra a sessão de sistema no Agent conforme a configuração. Considere o impacto nas ações e recursos que ainda dependem dessa sessão.',
 'Connect to Session':'Conecta a uma sessão de terminal já ativa. Iniciar a aplicação de terminal e conectar à sessão são etapas diferentes.',
 'Disconnect from Session':'Desconecta o acesso à sessão de terminal, sem fechar o próprio aplicativo de terminal.',
 'Get Cursor Location':'Lê a posição do cursor no contexto do terminal para orientar as operações seguintes.',
 'Set Cursor Location':'Posiciona o cursor no terminal conforme as coordenadas fornecidas.',
 'Get Field':'Obtém um campo da tela de terminal. Confira a identidade e o formato do campo antes de usar o retorno.',
 'Get Value':'Lê o valor indicado no contexto de terminal. Diferencie o conteúdo do campo de sua posição na tela.',
 'Hit Key':'Envia uma tecla à sessão de terminal conectada. Confira o foco e o estado da sessão.',
 'Read Table':'Lê a tabela indicada no terminal. Confira colunas, limites e conclusão da leitura.',
 'Write Table':'Escreve dados na tabela de terminal configurada. Valide destino e dados antes da gravação.',
 'Switch Session':'Troca a sessão de terminal usada pelo fluxo. As ações seguintes precisam corresponder à sessão selecionada.',
 'Mobile Action':'Executa uma ação de interação no elemento móvel configurado. Confirme o alvo no dispositivo e o resultado após a ação.',
 'Mobile Device Navigation':'Aciona navegação do dispositivo móvel conforme a opção selecionada. Diferencie navegação do sistema e da aplicação.',
 'Mobile Drawing Action':'Executa uma ação de desenho na tela móvel. Confira coordenadas, região e estado da aplicação.',
 'Mobile Image Action':'Interage com a tela móvel por uma referência de imagem. A referência precisa corresponder ao dispositivo e ao estado visual.',
 'Mobile Screen Action':'Executa a ação configurada sobre a tela móvel. Confira orientação e coordenadas pertinentes ao dispositivo.',
 'SAP Action':'Executa uma ação na interface SAP configurada. Sessão, elemento e resultado esperado precisam estar definidos.',
 'Validate SAP':'Verifica uma condição no contexto SAP e expõe o resultado para o fluxo. Confira a regra e os dados usados na comparação.',
 'Run Web Javascript':'Executa JavaScript no contexto do navegador. Confira janela, elementos e valores retornados; usar script não elimina a necessidade de verificação.'
}

VERBS={'Click':'Clica','Close':'Fecha','Collapse':'Recolhe','Drag':'Arrasta','Expand':'Expande','Find':'Localiza','Get':'Lê','Invoke':'Aciona','Select':'Seleciona','Set':'Define','Start':'Inicia','Toggle':'Alterna','Update':'Atualiza','Use':'Seleciona','Log':'Registra','Handle':'Trata','Hover':'Move o ponteiro sobre','Type':'Digita','Install':'Instala','Uninstall':'Desinstala','Connect':'Conecta','Disconnect':'Desconecta','Read':'Lê','Write':'Grava'}
TARGETS={'Element':'o elemento','Position':'a posição','Text':'o texto','Number':'o número','Attribute':'o atributo','Selection':'a seleção','Window Details':'os detalhes da janela','Window':'a janela','Element Value':'o valor do elemento','Application':'a aplicação','Application Details':'os detalhes da aplicação','File Upload':'o envio de arquivo','Checkbox':'o checkbox','Dropdown':'a opção da lista','Radio Button':'a opção do grupo','Alert':'o alerta','Screenshot':'uma captura da tela','Image':'a imagem','Cursor Location':'a posição do cursor','Device':'o dispositivo','Orientation':'a orientação','Area':'a área','Date/Time':'a data/hora','Cookie':'o cookie','Cookies':'os cookies','Browser':'o navegador','Browser Details':'os detalhes do navegador','Row':'a linha','Element Text':'o texto do elemento','Element Dropdown':'a opção da lista','Toggle Button':'o controle de alternância','Element Checkbox':'o checkbox','Element Combo Box':'o combo box','Element Panel State':'o estado do painel','Panel State':'o estado do painel','Session':'a sessão','Table':'a tabela','SAP Table':'a tabela SAP'}


SPECIAL.update({
 'Electron File Upload':'Envia um arquivo pelo controle de upload da aplicação Electron. Confira caminho acessível e confirmação da aplicação após a seleção.',
 'Set Green Screen Value':'Define o valor no campo de terminal configurado. Confira o alvo e o formato aceito na sessão conectada.',
 'Get text':'Extrai texto da região visual por reconhecimento. Confira área, motor e conteúdo antes de usar a leitura.',
 'Connect to Mobile Device':'Conecta ao dispositivo móvel segundo a configuração escolhida. A conexão e a disponibilidade da aplicação são requisitos separados.',
 'Drag Mouse':'Executa arraste com o mouse entre os alvos configurados. Confira origem, destino e estado da tela.',
 'Press Key':'Pressiona a tecla configurada na sessão com foco. Planeje a liberação quando a ação exigir manter uma tecla pressionada.',
 'Release Key':'Libera a tecla configurada após uma ação de pressão. Use em conjunto com o estado esperado da sessão.',
 'Scroll Wheel':'Envia rolagem pela roda do mouse. Confira foco, direção e a condição que indica o conteúdo pretendido.',
 'Set Element Radio Button':'Define a opção do grupo de seleção no contexto Salesforce. Confira elemento e estado resultante.',
 'Close SAP':'Encerra o contexto SAP conforme a configuração do bloco. Preserve evidências e considere sessões ainda em uso.',
 'SAP Get Text':'Lê texto do elemento SAP configurado. Relacione o valor retornado ao caso e à sessão corretos.',
 'Start SAP':'Inicia a aplicação SAP conforme a configuração. Confira os pré-requisitos e o contexto de sessão antes das ações seguintes.',
 'Start SAP Session':'Abre a sessão SAP configurada. Distingue iniciar uma aplicação de estabelecer a sessão usada pelo caso.',
 'Set Variable':'Define um valor de variável no escopo configurado. Considere duração e compartilhamento entre execuções.',
 'Get Variable':'Lê o valor de uma variável e trata a ausência conforme a configuração. Um valor padrão não comprova inicialização anterior.',
 'Use Browser Window':'Seleciona a janela ou aba de navegador que os blocos seguintes utilizarão. Confira identidade antes de ler ou clicar.',
 'Web File Upload':'Seleciona um arquivo para envio pelo controle Web. O caminho precisa estar acessível no ambiente da execução e o recebimento deve ser verificado.'
})


def clean(value):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',value).replace('\u200e','')).strip()


def block_summary(title,path):
    title=clean(title)
    if title in SPECIAL:return SPECIAL[title]
    category=path.split('/')[1]
    short=re.sub(r'^(D365|Salesforce) ','',title)
    if short in ['Login','Close Browser']:
        return ('Autentica na aplicação' if short=='Login' else 'Fecha o navegador da aplicação')+' no contexto '+('D365 F&O' if category=='dynamics-365' else 'Salesforce')+'. Confira a sessão e a configuração do bloco antes de continuar.'
    if short in ['Validate and Get','Get and Validate Element']:
        return 'Valida e obtém informações do elemento no contexto da aplicação. Configure o alvo e a condição esperada e trate uma divergência explicitamente.'
    if title=='Navigate Web':return 'Controla a navegação por URL, histórico, atualização ou nova aba conforme Navigation mode. Confira o modo, a janela e o destino; Refresh page atualiza a página atual.'
    if title=='Clear Web Cookies':return 'Remove cookies do contexto Web conforme a configuração. Considere o efeito sobre autenticação e estado do teste.'
    words=short.split(' ',1)
    if len(words)!=2 or words[0] not in VERBS:raise ValueError('Resumo de bloco não mapeado: '+title+' '+path)
    verb,target=words
    target=re.sub(r'\b(Web|UI|Electron|Mobile|Green Screen)\s*','',target).strip()
    target=TARGETS.get(target)
    if not target:raise ValueError('Alvo de bloco não mapeado: '+title+' '+path)
    tech=CATEGORIES[category][0].lower()
    return f'{VERBS[verb]} {target} no contexto de {tech}. Confira as propriedades do alvo, as saídas disponíveis e o efeito observado antes de continuar o caso.'


def main():
    inventory=json.loads((ROOT/'research/documentation-inventory.json').read_text(encoding='utf-8'))
    tree=json.loads((ROOT/'research/documentation-navigation.json').read_text(encoding='utf-8'))
    baseline=json.loads((ROOT/'research/enrichment-baseline.json').read_text(encoding='utf-8'))
    course=json.loads((ROOT/'research/course-content.json').read_text(encoding='utf-8'))
    existing={url.rstrip('/'):True for url in baseline['sourceUrls']}
    children={}
    def visit(node,parent=None):
        path=node['path'].removeprefix('/leapwork-flow/latest/')
        children[path]=[n['path'].removeprefix('/leapwork-flow/latest/') for n in node.get('children',[])]
        for n in node.get('children',[]):visit(n,path)
    for node in tree:visit(node)
    pages=[]
    for p in inventory['pages']:
        path=p['url'].removeprefix(PREFIX);doc=json.loads((ROOT/p['cacheFile']).read_text(encoding='utf-8'))
        bits=path.split('/');category=bits[1] if len(bits)>1 and bits[0]=='building-blocks' else None
        if path in SUMMARIES:summary=SUMMARIES[path]
        elif path=='building-blocks':summary='Catálogo organizado por tecnologia e função. As fichas distinguem o propósito de cada bloco; propriedades e exemplos completos permanecem na documentação oficial.'
        elif category in CATEGORIES and len(bits)==2:summary=CATEGORIES[category][1]
        elif category in CATEGORIES:summary=block_summary(p['title'],path)
        else:raise ValueError('Página sem revisão editorial: '+path)
        related=[l['slug'] for l in course['lessons'] if path in [ref[1] for ref in l['docs']]]
        notes=[]
        if 'experimental feature' in doc['text'].lower():notes.append('A fonte identifica o recurso como experimental; confira mudanças e disponibilidade antes de adotá-lo.')
        if category=='multi-factor-authenticator':notes.append('A página contém uma restrição específica sobre a configuração de segredo no Okta; confira o texto vigente e a política de identidade.')
        if path=='building-blocks/logic/c-sharp-code':notes.append('Esta página usa o contexto 2026.1 e descreve .NET 8. As notas 2026.3 anunciam .NET 10; confirme o runtime e as dependências da instalação. Consulte também Release Notes → 2026.3.')
        if path=='administration/database-decryption-keys':notes.append('O procedimento descrito trata SQLite; não generalize o mesmo mecanismo para toda implantação SQL Server.')
        fields=[]
        if category and len(bits)>2:
            body=doc['text'].split('Building block parameters')[-1]
            lines=[clean(x) for x in body.splitlines() if clean(x)]
            for i,line in enumerate(lines):
                if i and line.startswith(':') and 1<len(lines[i-1])<65 and lines[i-1] not in ['Block header','Note','Notes','Example','Parameters','(when available)'] and lines[i-1] not in fields:fields.append(lines[i-1])
        pages.append({'path':path,'title':clean(p['title']),'section':p['section'],'sectionTitle':SECTIONS[p['section']],'category':category,'summary':summary,'notes':notes,'source':p['url'],'retrievedAt':p['retrievedAt'],'headings':[clean(x) for x in doc['headings']][:10],'fieldHints':fields[:10],'children':children.get(path,[]),'related':related,'previouslyConsulted':p['url'].rstrip('/') in existing,'kind':'indice' if children.get(path) else 'referencia','imagesAvailable':len(doc['images'])})
    spec=json.loads((ROOT/'research/module5-api-spec.json').read_text(encoding='utf-8'))
    operations=[]
    for path,methods in spec['paths'].items():
        for method,op in methods.items():
            if method not in ['get','put','post','delete','patch']:continue
            params=[{'name':v['name'],'location':v['in'],'required':v.get('required',False),'type':v.get('schema',{}).get('format') or v.get('schema',{}).get('type','')} for v in op.get('parameters',[])]
            schemas=[]
            for response in op.get('responses',{}).values():
                for media in response.get('content',{}).values():
                    schema=media.get('schema',{});ref=schema.get('$ref') or schema.get('items',{}).get('$ref')
                    if ref and ref.split('/')[-1] not in schemas:schemas.append(ref.split('/')[-1])
            operations.append({'method':method.upper(),'path':path,'title':op.get('summary',''),'parameters':params,'schemas':schemas,'responses':list(op.get('responses',{})),'bodyRequired':op.get('requestBody',{}).get('required',False),'bodySchemas':list(op.get('requestBody',{}).get('content',{}))})
    report={'consultedAt':inventory['completedAt'],'scope':inventory['scope'],'pages':pages,'operations':operations,'sections':[{'id':n['path'].removeprefix('/leapwork-flow/latest/'),'title':n['title'],'label':SECTIONS[n['title']],'count':sum(p['section']==n['title'] for p in pages)} for n in tree],'counts':{'pages':len(pages),'previouslyConsulted':sum(p['previouslyConsulted'] for p in pages),'newSources':sum(not p['previouslyConsulted'] for p in pages),'operations':len(operations),'unavailable':inventory['unavailable']}}
    (ROOT/'site/documentation-data.js').write_text('/* Fichas editoriais de consulta; fontes oficiais e data de varredura por página. */\nwindow.LEAP.documentation = '+json.dumps(report,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    (ROOT/'research/documentation-editorial.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report['counts']),flush=True)


if __name__=='__main__':main()

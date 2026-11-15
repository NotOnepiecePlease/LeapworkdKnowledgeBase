# Revisão de pertinência · v1.3.1

A revisão confrontou os **427 passos das 98 aulas**, os **336 usos de imagens** da versão preparada v1.3.0 e as **338 fichas** da biblioteca. O catálogo de 83 operações permanece vinculado ao contrato OpenAPI. A conferência é editorial: não houve execução dos fluxos no Leapwork.

**Resultado:** 12 usos de imagem removidos, sete capturas substituídas e três reposicionadas. Permanecem 324 usos de imagem no caderno, incluindo a introdução. Das inclusões da varredura, 73 permanecem após a revisão, usando 64 arquivos distintos. São 315 passos ilustrados e 112 sem imagem.

## Critérios

- A imagem deve mostrar o objeto, campo, ação ou evidência pedido no próprio passo.
- Estar no mesmo artigo ou assunto não basta.
- Uma legenda não torna pertinente uma imagem de outra operação.
- Configuração visível, valores e versão devem corresponder ao texto; divergências exigem correção ou remoção.
- Exercício autoral não é execução comprovada.

Os 83 passos que tiveram alteração incluem legendas e metadados de proveniência; isso não significa 83 erros factuais. O registro JSON mantém a versão exata revisada de cada aula, passo, ficha e imagem.

## Imagens removidas

- **Módulo 3 · Reconhecer quando usar lógica C# · passo 2**: O editor mostra erros de compilação e código de exemplo; não demonstra um template pronto e compatível.
- **Módulo 4 · Identificar o Controller e os recursos do ambiente · passo 2**: O exemplo de licença está vencido desde 2018 e não comprova os recursos efetivamente disponíveis no ambiente de estudo.
- **Módulo 4 · Identificar o Controller e os recursos do ambiente · passo 4**: Refresh License altera a licença; o passo planeja conta, Controller e teste de acesso.
- **Módulo 4 · Preparar conexões, chaves e notificações · passo 1**: A tela específica de Appium não corresponde à escolha genérica de uma conexão para o cenário.
- **Módulo 4 · Definir repetição sem esconder falhas · passo 2**: A barra da Run List não mostra a configuração de sobrescrita de retry no Schedule.
- **Módulo 4 · Planejar horários, distribuição e filas · passo 2**: Flow sequence mostra ordem de execução, não as três modalidades de distribuição entre Agents.
- **Módulo 4 · Correlacionar auditoria, mudanças e diagnóstico · passo 2**: FILTER VALUES exibe datas, não o filtro de ativo ou usuário ensinado neste passo.
- **Módulo 2 · Selecionar uma nova janela ou aba · passo 1**: O quadro mostra a aba já aberta e não o link Click here que o passo manda capturar.
- **Módulo 3 · Consultar uma API e validar sua resposta · passo 1**: A captura mostrava Method = POST, enquanto o exercício instrui uma chamada GET.
- **Módulo 3 · Normalizar texto e extrair padrões · passo 1**: A captura mostrava Substring, enquanto o passo instrui Trim.
- **Módulo 4 · Registrar mudanças e consultar o histórico · passo 2**: O canvas do fluxo não mostrava Version History; foi retirado e substituído, nesse passo, pela tabela já selecionada para a aula.
- **Módulo 4 · Escolher Only Flow, Full Restore ou Full Copy · passo 2**: A tabela de versões não mostrava as opções Only Flow, Full Restore e Full Copy comparadas no texto.

## Capturas substituídas

- **Módulo 3 · Ler uma planilha com intervalo e iteração · passo 1**: Substitui Cloud file por Local path, opção que o passo efetivamente ensina.
- **Módulo 3 · Reconhecer quando usar lógica C# · passo 3**: Substitui a lista de referências com avisos pela janela System Assemblies que o texto descreve.
- **Módulo 4 · Organizar fluxos em Run Lists e passos · passo 2**: Substitui a imagem do botão por sua janela de seleção, correspondente à conferência dos fluxos.
- **Módulo 5 · Isolar dados, preparar e encerrar os casos · passo 1**: Troca o exemplo de nuvem pela origem local citada no passo.
- **Módulo 5 · Desenhar a integração antes de escolher a ferramenta · passo 2**: Substitui Flow sequence pelo formulário que mostra os itens pedidos no texto.
- **Módulo 2 · Selecionar opções por valor, texto ou índice · passo 3**: O quadro de 3:03 ainda mostrava Value = 1. O de 3:09 contém Option 2 e corresponde ao passo.
- **Módulo 1 · Formulários e controles web · passo 2**: O quadro de 3:54 mostra Value = Start date, conforme a instrução; o anterior ainda mostrava End date na inspeção.

## Capturas reposicionadas

- **Módulo 3 · Escrever resultados no Excel · passo 2 → passo 1**: A imagem demonstra definir intervalo; foi movida do método de escrita para o passo que define o intervalo.
- **Módulo 4 · Preparar conexões, chaves e notificações · passo 4 → passo 3**: Move a configuração de proxy para o passo que prepara e-mail e proxy; não representa um teste de entrega.
- **Módulo 4 · Registrar mudanças e consultar o histórico · passo 3 → passo 2**: Move a tabela para a abertura do histórico e substitui o canvas que não mostrava Version History.

## Informações e fontes corrigidas

- **Módulo 4 · Identificar o Controller · passo 4:** o link principal passou de License Management para User Management. A observação agora trata conta, Controller e papel. Refresh License saiu do passo. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/administration/user-management).
- **Módulo 4 · Identificar o Controller · passo 1:** o texto passou a distinguir a seleção de Controller na entrada e Controller Settings. A captura mostra Select Controller. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/administration/controller-settings).
- **Módulo 4 · Organizar usuários · passo 4:** User Management passou a ser o link principal para as opções de identidade; as fontes específicas continuam nas figuras e referências. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/administration/user-management).
- **Módulo 3 · C# · conceitos e passo 3:** .NET 8 foi delimitado ao contexto 2026.1 da referência, com menção à migração .NET 10 anunciada nas notas 2026.3. Foi acrescentada a fonte da versão. [C# Code](https://docs.leapwork.com/leapwork-flow/latest/building-blocks/logic/c-sharp-code), [notas 2026.3](https://docs.leapwork.com/leapwork-flow/latest/release-notes/leapwork-flow-major-release-2026-3).
- **Biblioteca · Save File:** retirado o destino configurável sugerido pelo resumo; o texto agora descreve armazenamento gerenciado, nome automático e ausência de caminho manual. A aula já descrevia esse comportamento. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/building-blocks/data-driven/save-file).
- **Biblioteca · Generate date/time:** o resumo agora declara que o bloco fornece o instante atual do sistema; uma base fixa exige outra entrada. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/building-blocks/generators/generate-date-time).
- **Biblioteca · Navigate Web:** o resumo passou a abranger Navigation mode, incluindo histórico, atualização e nova aba, além de URL. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/building-blocks/web/navigate-web).
- **Módulo 5 · Azure DevOps · passo 2:** o texto passou a começar pelo menu Import → Import from ADO que aparece na captura, antes da escolha de projeto e Area Path. [Fonte](https://docs.leapwork.com/leapwork-flow/latest/working-with-leapwork/microsoft-ado-test-plan-integration).
- **Legendas:** passaram a nomear o conteúdo visível e sua limitação: uma execução isolada não mostra todas as tentativas; a cópia na árvore não exibe seus agendamentos; Never selecionado não demonstra exigência de comentário. As fontes continuam ligadas a cada figura.

## Verificação e limites

- As suítes de navegador conferem imagens, rotas, notas, filtros, laboratórios e funcionamento offline.
- `scripts/check_editorial_review.py` confere a integridade da versão revisada e as regressões conhecidas. Ele não decide automaticamente se uma imagem é pertinente.
- `research/illustration-selection.json` exige seleção explícita e justificativa por figura. A coleta de um artigo não autoriza inserir todas as suas imagens.
- `research/editorial-review.json` registra as decisões e os hashes da versão revisada. Mudanças posteriores exigem nova conferência.
- [ENRIQUECIMENTO.md](ENRIQUECIMENTO.md) localiza as inclusões que permanecem no caderno.

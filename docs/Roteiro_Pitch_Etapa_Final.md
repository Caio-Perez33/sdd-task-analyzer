# Roteiro do pitch tecnico - Etapa Final (5 minutos)

Formato pedido no enunciado: video horizontal, aproximadamente cinco minutos, com audio e camera visiveis. Deixe o repositorio, a aba Actions e o terminal abertos antes de gravar. As falas sobre CI verde e Docker devem refletir os resultados reais que aparecem na tela.

## 0:00-0:30 | Abertura

"Ola, meu nome e Caio e este e o pitch da Etapa Final do Bootcamp III. O projeto e o TaskAnalyzer. Vou demonstrar a integracao continua, a execucao isolada dos testes com Docker e como as regras de contexto ajudam a controlar os riscos do uso de inteligencia artificial no desenvolvimento."

## 0:30-2:00 | CI/CD no GitHub Actions

Mostrar a pasta `.github/workflows` e abrir `ci.yml`. Explicar que o fluxo e disparado por push e pull request, configura Python 3.11, instala pytest e executa a suite. Em seguida, mostrar uma execucao real na aba Actions. A construcao Docker so acontece depois que os testes passam.

Fala sugerida: "A automacao transforma a validacao em uma etapa repetivel. Uma falha nos testes interrompe o job dependente e impede que a construcao da imagem seja considerada aprovada. O workflow nao publica uma imagem automaticamente; nesta atividade ele valida o codigo e a imagem."

## 2:00-3:30 | Containerizacao

No terminal, na raiz do projeto, executar:

```bash
docker compose run --build --rm testes
```

Mostrar o resultado real do pytest. Abrir `Dockerfile` e `docker-compose.yml`, destacando a imagem `python:3.11-slim`, a execucao como usuario sem privilegios, a ausencia de persistencia e o comando padronizado. Se houver falha no Docker, nao afirme que a demonstracao passou; mostre a mensagem e explique que ela precisa ser corrigida antes da entrega.

Fala sugerida: "O Docker empacota o ambiente com a versao do Python e as dependencias declaradas. O Compose permite executar a suite com um comando, reduzindo diferencas entre maquinas."

## 3:30-4:25 | Governanca, alucinacoes e revisao humana

Mostrar `CONTEXT_RULES.md`, `specs/task_analyzer_spec.md` e `docs/AI_PROMPT_LOG.md`. Explicar que a IA esta limitada ao contrato, que dependencias externas e persistencia nao sao permitidas e que os testes verificam as regras principais. Apresentar os riscos analisados: inventar uma biblioteca, alterar a formula de atraso, ignorar datas invalidas ou dividir por zero. Distinguir riscos avaliados de eventuais erros realmente observados durante a implementacao.

Fala sugerida: "O uso de IA nao elimina a responsabilidade do desenvolvedor. A especificacao limita a solucao, os testes tornam o comportamento verificavel e a revisao humana confere o diff antes do merge."

## 4:25-5:00 | Conclusao

Mostrar a estrutura final e a situacao real do workflow. "A entrega combina contrato de negocio, testes automatizados, CI, imagem Docker e registro de governanca. Antes da submissao, confirme que o build esta verde, que o comando Docker terminou com todos os testes aprovados e que o relatorio PDF foi incluido na plataforma. Obrigado."

## Antes de publicar

- Confirme que a branch foi enviada e que o workflow realmente terminou em verde.
- Confirme que `docker compose run --build --rm testes` terminou com oito testes aprovados.
- Grave na horizontal, confira som/camera e veja o video uma vez antes de publica-lo como Publico ou Nao listado.
- Insira o URL real do YouTube na plataforma de entrega. Nao use URL inventada ou placeholder.

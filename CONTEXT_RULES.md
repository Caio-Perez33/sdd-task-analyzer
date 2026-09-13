# CONTEXT_RULES.md - TaskAnalyzer

## Objetivo
Este arquivo define as regras de contexto que devem orientar qualquer agente de IA envolvido na geração do código do módulo TaskAnalyzer. A especificação SDD e estes limites devem ser tratados como contrato para a implementação.

## 1. Diretrizes arquiteturais (obrigatórias)
1. Usar Python 3.11 ou superior.
2. Utilizar type hints em todas as funções e métodos.
3. Seguir PEP 8 e boas práticas de código limpo.
4. Manter funções pequenas, coesas e com responsabilidade única (SRP).
5. Usar documentação no padrão Google Docstrings para módulos, classes, funções e parâmetros.
6. Utilizar logs estruturados com o módulo padrão `logging`.
7. Tratar exceções de forma específica, com mensagens claras e objetivas.
8. Manter código legível e manutenível, com nomes descritivos.
9. Separar responsabilidades (SRP) e evitar lógica em scripts quando a responsabilidade puder ficar em módulos/funções reutilizáveis.

## 2. Proibições explícitas (regras restritivas)
1. Não utilizar bibliotecas externas não autorizadas.
2. Não alterar os cenários de teste fornecidos pela especificação.
3. Não modificar a estrutura de pastas definida para o projeto.
4. Não persistir dados em arquivos ou bancos de dados.
5. Não alterar a assinatura (nome e parâmetros) das funções públicas sem autorização.
6. Não gerar código sem testes correspondentes para novas funcionalidades.
7. Não inserir código duplicado ou desnecessário.
8. Não assumir comportamentos que não estejam especificados no contrato de negócio.
9. Não comentar código em excesso; comentários devem existir apenas quando necessários para esclarecer uma decisão ou regra não óbvia.
10. Não retornar valores diferentes do contrato definido.

## 3. Regras de interação com IA
1. Fornecer sempre o contexto completo antes de solicitar geração ou alteração de código.
2. Validar se a IA compreendeu o contrato antes de gerar código.
3. Solicitar explicações quando houver dúvidas na solução.
4. Revisar criticamente todo código gerado antes de aceitar a implementação.
5. Rejeitar respostas que violem estas proibições ou o contrato.

## 4. Contrato do TaskAnalyzer
A IA deve respeitar integralmente a especificação em `specs/task_analyzer_spec.md`, incluindo entradas, saídas, regras de negócio, restrições e cenários de aceite.

## 5. Princípio de homologação
Código gerado por IA não é automaticamente aceito. A decisão final permanece sob revisão humana, com execução dos testes automatizados, conferência do contrato, análise da qualidade e validação de violações.

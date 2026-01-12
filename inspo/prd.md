Contexto do Projeto

O projeto atualmente possui integração com o SINASC, focada em análises agregadas e espaciais.
Agora estamos implementando um módulo independente para o SIM (Sistema de Informações sobre Mortalidade), cujo foco é análise transversal (cross-sectional) baseada em microdados de óbitos.

A unidade de análise é o óbito individual, e o objetivo é permitir testes estatísticos acoplados diretamente às análises exploratórias, sem depender de geoprocessamento ou cálculo de taxas populacionais.

Objetivo Geral

Implementar um submódulo estatístico do SIM que permita testar associações, diferenças entre grupos e medidas epidemiológicas básicas, utilizando variáveis categóricas e numéricas do dicionário oficial do SIM.

O módulo deve ser genérico, reutilizável, bem tipado e extensível, evitando repetição de código.

Organização Esperada

Criar a seguinte estrutura:

sim/
 ├── stats/
 │    ├── categorical.py
 │    ├── numeric.py
 │    ├── proportions.py
 │    ├── epi.py
 │    ├── models.py
 │    └── utils.py


Cada função deve:

receber um DataFrame

aceitar filtros opcionais

validar tipos de variáveis

retornar resultados em formato estruturado (dict ou dataclass)

1️⃣ Testes para Variáveis Categóricas × Categóricas
Implementar em categorical.py
a) Qui-quadrado de independência

Entrada: duas variáveis categóricas

Gerar:

tabela de contingência

estatística χ²

graus de liberdade

p-valor

resíduos padronizados

Rejeitar automaticamente se frequências esperadas forem muito baixas (ou emitir warning)

b) Teste exato de Fisher

Aplicável apenas a tabelas 2×2

Selecionado automaticamente quando necessário

c) Cramér’s V

Calcular como tamanho de efeito para testes qui-quadrado

Retornar junto com o χ²

2️⃣ Testes para Variável Numérica × Variável Categórica
Implementar em numeric.py
a) Teste t de Student

Dois grupos

Checar normalidade e homocedasticidade (ou documentar limitações)

b) Mann–Whitney U

Alternativa não paramétrica ao t-test

Deve ser o default se normalidade não for satisfeita

c) ANOVA

Numérica vs variável categórica com ≥3 níveis

d) Kruskal–Wallis

Alternativa não paramétrica à ANOVA

Retornar estatística e p-valor

3️⃣ Testes de Proporções
Implementar em proportions.py
a) Teste z para proporções

Comparar proporções entre dois grupos

Entrada: variável binária + variável de agrupamento

b) Intervalo de confiança para proporção

IC 95% (Wilson ou normal)

Retornar proporção, IC inferior e superior

4️⃣ Medidas Epidemiológicas Clássicas
Implementar em epi.py
a) Odds Ratio (OR)

Para tabelas 2×2

Retornar:

OR

IC 95%

p-valor (via qui-quadrado ou Fisher)

b) Risco Relativo (RR)

Calcular RR e IC 95%

Documentar pressupostos

5️⃣ Modelos Estatísticos Simples
Implementar em models.py
a) Regressão logística binária

Desfecho binário

Permitir múltiplas covariáveis

Retornar:

coeficientes

OR ajustados

IC 95%

p-valores

b) Regressão logística multinomial (opcional)

Para desfechos com >2 categorias

Implementação mínima, bem documentada

6️⃣ Utilitários e Validações
Implementar em utils.py

Detecção de tipo de variável (categórica vs numérica)

Conversão segura de idade codificada

Tratamento explícito de valores ignorados (ex: 9)

Funções auxiliares para filtros e estratificações

Padronização de output

7️⃣ Requisitos Técnicos

Usar bibliotecas padrão do ecossistema Python (pandas, numpy, scipy, statsmodels)

Não acoplar o módulo a Streamlit ou UI

Código testável e documentado

Nenhuma lógica específica de SINASC deve ser reutilizada aqui

O módulo deve funcionar apenas com microdados do SIM

8️⃣ Resultado Esperado

Ao final, o módulo deve permitir chamadas como:

chi2_test(df, "SEXO", "CAUSABAS")
mann_whitney(df, "IDADE", "SEXO")
odds_ratio(df, "SEXO", "SUICID")
logistic_regression(df, y="HOMICID", X=["SEXO", "IDADE", "ESC"])


Com resultados retornados em objetos estruturados, prontos para uso em dashboards ou relatórios.

9️⃣ Princípio Norteador

SINASC → análise ecológica e espacial
SIM → análise individual, transversal e estatística
# AJA · Inteligência Artificial & Machine Learning

| Integrante | RM |
|---|---|
| Guilherme Santos Nunes | RM558989 |
| Kaique Rodrigues Zaffarani | RM556677 |
| Pedro Josué Pereira Almeida | RM554913 |

Global Solution 2026.2 · CitizenTech · Engenharia de Software · FIAP

---

## O projeto AJA

O **AJA** é uma plataforma de participação cidadã que transforma relatos da comunidade em propostas
fundamentadas de melhoria da infraestrutura do bairro. O primeiro recorte é a **acessibilidade para
pessoas com deficiência visual e auditiva no Parque Doroteia**, zona sul de São Paulo.

A jornada é simples para quem participa:
1. o morador relata uma barreira (foto, localização, texto ou áudio);
2. o relato vira um **tópico**, que reúne relatos parecidos, evidências locais, dados públicos e
   referências técnicas;
3. a comunidade apoia, confirma a observação ou acrescenta evidências;
4. o AJA consolida um **dossiê** para o órgão responsável;
5. o AJA acompanha o protocolo até a resposta, e depois da intervenção a comunidade avalia se a melhoria
   atendeu às necessidades.

O trabalho de organizar a demanda e cobrar a resposta fica com a plataforma, e não com o cidadão.

## Ficha da CitizenTech

| Campo | Descrição |
|---|---|
| **Nome** | AJA |
| **Cidade e bairro** | São Paulo, Parque Doroteia (Subprefeitura Cidade Ademar, zona sul) |
| **Cidadão beneficiado** | Pessoas com deficiência visual e auditiva que circulam a pé pelo bairro |
| **Problema, em uma frase** | Pessoas com deficiência visual e auditiva do Parque Doroteia enfrentam barreiras nas calçadas e travessias, e relatar e acompanhar a solução junto à Prefeitura é trabalhoso e pouco acessível. |
| **Como funciona** | O morador relata a barreira, o relato vira um tópico com evidências, a comunidade apoia ou confirma, o AJA gera um dossiê para o órgão responsável e acompanha o protocolo até a resposta. |
| **O que cada parte faz** | **Dados:** coleta e recorte de pedidos reais do SP156 sobre barreiras para pedestres.<br>**Modelo:** um XGBoost estima se um pedido será finalizado pela Prefeitura em até 30 dias.<br>**Leitura para o cidadão:** a previsão vira expectativa de prazo e prioridade de acompanhamento no AJA. |
| **Indicador de impacto** | Barreiras mapeadas; % de demandas com protocolo aberto; tempo médio até a resposta do órgão; nota dada por pessoas com deficiência depois da intervenção |
| **ODS conectados** | ODS 11 (meta 11.7: espaços públicos seguros e acessíveis, inclusive para pessoas com deficiência), ODS 10 (meta 10.2: inclusão independente de deficiência), ODS 9 (infraestrutura de qualidade e inclusiva) |

## Esta entrega: IA & ML

**Pergunta de ML:** um pedido ao SP156 sobre barreira para pedestres será finalizado em até 30 dias?

**Dados:** 120.248 pedidos reais do SP156, do Portal de Dados Abertos da Prefeitura de São Paulo,
abertos de jan/2020 a set/2026.

**Modelo:** XGBoost.
- 24 combinações de 3 hiperparâmetros, com validação cruzada temporal só no treino (2020–2024).
- Teste em 2025–2026: ROC-AUC de **0,831**, contra 0,794 de um baseline simples.

**Achado principal:**
- pedidos de **obstáculo na calçada** (acessibilidade) levam em mediana **266 dias** para serem
  finalizados, e só 7% saem em até 30 dias;
- pedidos de manutenção de calçada pública levam 12 dias.

| Entregável | Onde |
|---|---|
| Notebook executado | [`ml/notebook_sp156_tempo_resposta.ipynb`](ml/notebook_sp156_tempo_resposta.ipynb) |
| Relatório | [`ml/RELATORIO_ML.md`](ml/RELATORIO_ML.md) |
| Fonte, link e período dos dados | [`ml/dados/README.md`](ml/dados/README.md) |
| Dependências | [`ml/requirements.txt`](ml/requirements.txt) |
| Vídeo (até 5 min) | *link a incluir* |

## Como esta atividade agrega ao AJA

- **Expectativa realista:** ao registrar uma barreira, o cidadão vê quanto tempo pedidos parecidos
  costumam levar na Prefeitura.
- **Acompanhamento ativo:** quando a chance de resposta rápida é baixa, o tópico já nasce com lembretes,
  convite para a comunidade confirmar e reforçar evidências e inclusão no dossiê.
- **Tópicos fundamentados:** o que foi feito aqui com o SP156 (coletar dados públicos reais, organizar por
  tipo de barreira e região, medir o histórico de resposta) é a base que o AJA usa para montar tópicos.
  Dados oficiais se somam à opinião da comunidade, e uma barreira passa a ser tratada como um problema
  documentado, e não como uma reclamação isolada.

## Como executar

```bash
cd ml
pip install -r requirements.txt
jupyter notebook notebook_sp156_tempo_resposta.ipynb
```

O notebook lê `ml/dados/sp156_barreiras_pedestre_2020_2026.csv.gz`, que já está no repositório.
Para regenerar a base a partir dos arquivos originais da Prefeitura, rode
`python ml/dados/extrair_sp156.py` (baixa cerca de 3 GB).

## Estrutura

```
ml/
├── notebook_sp156_tempo_resposta.ipynb   notebook executado, com todos os resultados
├── RELATORIO_ML.md                       relatório
├── requirements.txt
├── dados/
│   ├── README.md                         fonte, link, período, colunas e limitações
│   ├── extrair_sp156.py                  download e recorte dos dados originais
│   └── sp156_barreiras_pedestre_2020_2026.csv.gz
└── figuras/                              gráficos gerados pelo notebook e usados no relatório
```

---

## Tecnologias

[![Python](https://img.shields.io/badge/Python_3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=flat-square)](https://xgboost.readthedocs.io)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)](https://matplotlib.org)
[![seaborn](https://img.shields.io/badge/seaborn-4C72B0?style=flat-square)](https://seaborn.pydata.org)

---

## Referências

| # | Referência | Aplicação no Projeto |
|---|---|---|
| 1 | [Prefeitura de São Paulo — Dados do SP156 (Portal de Dados Abertos)](http://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156) | Base de dados real: pedidos de 2020 a 2026 e dicionário de dados |
| 2 | [Chen, T.; Guestrin, C. (2016) — *XGBoost: A Scalable Tree Boosting System* — KDD '16](https://doi.org/10.1145/2939672.2939785) | Algoritmo de classificação escolhido |
| 3 | [Grinsztajn, L.; Oyallon, E.; Varoquaux, G. (2022) — *Why do tree-based models still outperform deep learning on typical tabular data?* — NeurIPS](https://arxiv.org/abs/2207.08815) | Justificativa para árvores em vez de MLP em dados tabulares |
| 4 | [scikit-learn — `TimeSeriesSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) | Validação cruzada temporal no treino |
| 5 | [Fawcett, T. (2006) — *An introduction to ROC analysis* — Pattern Recognition Letters, 27(8)](https://doi.org/10.1016/j.patrec.2005.10.010) | Métrica ROC-AUC e leitura da curva ROC |
| 6 | [Wilson, E. B. (1927) — *Probable inference, the law of succession, and statistical inference* — JASA, 22(158)](https://doi.org/10.1080/01621459.1927.10502953) | Intervalo de confiança das taxas por subprefeitura |
| 7 | [IBGE — Censo 2022: Características urbanísticas do entorno dos domicílios](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102168.pdf) | Contexto de calçadas, obstáculos e rampas; próximo passo do modelo |
| 8 | [Ipea — ODS 11: Cidades e Comunidades Sustentáveis](https://ipea.gov.br/ods/ods11.html) | Meta 11.7, acesso a espaços públicos acessíveis |
| 9 | [Lei nº 13.146/2015 — Lei Brasileira de Inclusão da Pessoa com Deficiência](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm) | Direito à acessibilidade em vias e espaços públicos |
| 10 | [Lei nº 13.709/2018 — LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) | Minimização de dados: endereço descartado e coordenadas arredondadas |

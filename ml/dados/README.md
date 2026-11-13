# Dados

Esta pasta é a **etapa anterior ao notebook**: a coleta e o recorte dos dados públicos. O script baixa os
arquivos originais da Prefeitura, guarda só os pedidos sobre barreiras para pedestres e descarta o
endereço exato. A limpeza para o modelo (padronizar nomes, remover cancelados, tratar censura) fica no
notebook, para que cada decisão apareça junto do seu efeito.

## Arquivo

`sp156_barreiras_pedestre_2020_2026.csv.gz` (CSV separado por vírgula, UTF-8, compactado em gzip)

- **120.248 pedidos** ao SP156 sobre barreiras no caminho do pedestre.
- Pedidos abertos de **01/01/2020 a 30/09/2026**.

## Fonte

| Item | Valor |
|---|---|
| Publicador | Prefeitura de São Paulo, Secretaria Municipal de Inovação e Tecnologia |
| Conjunto | Dados do SP156 – Solicitações |
| Link | http://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156 |
| Dicionário | “Dicionário dados abertos – SP156 2020 em diante” (no mesmo link, atualizado em 10/08/2026) |
| Arquivos usados | 25 CSVs trimestrais, do 1º tri/2020 ao 3º tri/2026 |
| Data do download | 13/11/2026 |
| Licença | dados abertos da Prefeitura de São Paulo |

Os dados são **reais e públicos**. Não usamos nenhum dado simulado.

## Como o recorte foi gerado

O script [`extrair_sp156.py`](extrair_sp156.py) baixa cada CSV trimestral e mantém apenas os 10
serviços abaixo:

| Serviço no SP156 | Pedidos |
|---|---|
| Calçada pública – solicitar manutenção | 26.470 |
| Acessibilidade – solicitar avaliação de obstáculo na calçada | 24.751 |
| Calçada particular – denunciar calçada danificada ou inexistente | 19.995 |
| Sinalização horizontal apagada (pintura de solo) – solicitar repintura | 17.821 |
| Semáforo de veículos e pedestres – sugerir ajuste de tempo | 12.804 |
| Travessia de pedestres – solicitar avaliação | 9.372 |
| Sugerir construção de calçadas em áreas públicas e praças | 3.532 |
| Guias para travessia de pedestres – solicitar rebaixamento | 3.440 |
| Guia rebaixada – solicitar fiscalização de rebaixamento irregular | 2.044 |
| Manutenção de semáforos | 19 |

```bash
pip install -r ../requirements.txt
python extrair_sp156.py
```

Os arquivos originais **não são uniformes**, e o script trata as diferenças:
- a ordem das colunas muda (algumas versões incluem “Bairro”);
- o separador alterna entre `;` e `,`;
- a codificação alterna entre Latin-1 e UTF-8;
- o 3º trimestre de 2026 usa datas no formato `mm/dd/aaaa`.

Por isso as colunas são localizadas pelo nome e o formato da data é detectado em cada arquivo.

## Colunas

| Coluna | Descrição |
|---|---|
| `data_abertura` | data de abertura do protocolo (AAAA-MM-DD) |
| `data_finalizacao` | data de fechamento do protocolo; vazia se ainda aberto |
| `data_extracao_arquivo` | data de finalização mais recente do arquivo de origem, usada como data aproximada da extração feita pela Prefeitura |
| `canal` | PORTAL, CRM (central 156), MOBILE, CHATBOT |
| `tema`, `assunto`, `servico` | classificação da Carta de Serviços |
| `status` | Finalizada, Aberto, Em Andamento ou Cancelada, na data de extração |
| `orgao` | órgão responsável **na data de extração** (não é usado no modelo) |
| `lat_aprox`, `lon_aprox` | coordenadas arredondadas para 3 casas (cerca de 100 m) |
| `subprefeitura`, `distrito` | divisão administrativa do local do pedido |
| `arquivo_origem` | nome do arquivo trimestral de origem |

## Privacidade

A base pública do SP156 não contém nome, CPF, telefone nem e-mail do solicitante. Mesmo assim, por
cuidado (a localização exata de uma denúncia de calçada pode apontar para uma residência):
- descartamos `Logradouro`, `Número` e `CEP`;
- arredondamos latitude e longitude para cerca de 100 m.

## Limitações conhecidas

- **2º trimestre de 2021:** publicado só em XLSX, não incluído.
- **2º trimestre de 2024:** o arquivo não tem a coluna “Serviço”, não incluído.
- **1º trimestre de 2021:** o arquivo publicado vem incompleto (só pedidos de janeiro chegaram ao
  recorte, 1.158 linhas).
- **1º trimestre de 2025:** o arquivo tem exatamente 1.048.575 linhas, o limite do Excel, então pode
  estar truncado na origem.
- **Status muda com o tempo:** a Prefeitura substitui os arquivos a cada atualização. Os status
  refletem a extração de cada arquivo (entre jul. e out. de 2026; o 3º trimestre de 2022 foi extraído
  em nov. de 2025). Pedidos recentes ainda abertos têm desfecho desconhecido, e o notebook trata
  isso como censura.
- **Pedido não é problema:** segundo o próprio dicionário, várias pessoas podem abrir pedidos para a
  mesma barreira, e a Prefeitura pode agir sem pedido. “Finalizada” significa protocolo encerrado,
  não necessariamente barreira removida.

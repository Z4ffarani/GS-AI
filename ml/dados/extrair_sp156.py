"""Baixa os arquivos trimestrais do SP156 e gera o recorte de barreiras para pedestres.

Fonte: Portal de Dados Abertos da Prefeitura de São Paulo
http://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156

Uso:
    python extrair_sp156.py            # gera sp156_barreiras_pedestre_2020_2026.csv.gz

Cada arquivo trimestral tem de 300 mil a 1,1 milhão de linhas de todos os temas. Entre os
trimestres mudam a ordem das colunas, o separador (; ou ,), a codificação (Latin-1 ou UTF-8)
e o formato da data (dd/mm/aaaa ou mm/dd/aaaa). Por isso as colunas são localizadas pelo nome
e o formato de data é detectado por arquivo.

Privacidade: logradouro, número e CEP são descartados; latitude e longitude são arredondadas
para 3 casas decimais (cerca de 100 m).
"""

import csv
import gzip
import io
import re
import sys
import unicodedata
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

BASE = "https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/"

# Arquivos de 2020 a 2026 publicados em CSV. O 2º trimestre de 2021 só existe em XLSX e o
# 2º trimestre de 2024 não tem a coluna "Serviço"; ambos ficam de fora (ver dados/README.md).
ARQUIVOS = """
f67fcc12-8da4-485f-92a3-d2af40cc771e/download/arquivo-final-3-trim-26.csv
368eb32d-ef25-4441-be8f-fce0146575a1/download/arquivo-final-2-trim-26.csv
75105148-4efd-48f3-8ae0-fc6c2adf7060/download/arquivo-final-1-trim-26.csv
d3a98097-8128-45d4-b8fe-21874b81c971/download/arquivo-final-4-trim-25.csv
3b1d2648-d586-40c8-819c-24fbb8005343/download/arquivo-final-3-trim-25.csv
f5df7f4a-d614-4f85-b4a0-263ec9370cd9/download/arquivo-final-2-trim-25.csv
7c5aeb58-2cad-40ba-9e9e-af1c17cc5070/download/arquivo-final-1-trim-25.csv
ed357147-f15c-4bf0-ad15-edc963a9f130/download/arquivo-final-4-trim.-2024.csv
3c12fe0a-ec4f-4a20-a987-dd177330f4ce/download/arquivo-final-3-trim.-2024.csv
787c054d-3e77-46c8-8713-e4e26eb2dd55/download/arquivo-final-1-trim.-2024.csv
33d41278-02de-417a-a99a-5e01d3d87952/download/arquivo-final-4-trim.-2023.csv
b01a9038-969e-4630-bd3a-4abe188b7259/download/arquivo-final-3-trim.-2023.csv
7978d3ba-d379-44db-993b-61b9ff406435/download/arquivo-final-2-trim.-2023.csv
d3043e41-4270-47b5-9922-9e35edd10950/download/arquivo-final-1-trim.-2023.csv
68408b82-9123-4be0-87cf-bff9096947c6/download/arquivo-final-4-trim.-2022.csv
69b1460a-a245-47fa-bbb0-51f5e57c2f28/download/arquivo-final-3-trim.-2022.csv
6de63b14-e804-44cb-9be1-e8b2971504ce/download/arquivo-final-2-trim.-2022.csv
6e6b299c-1952-433c-be06-797a2bc14fda/download/arquivo-final-1-trim.-2022.csv
a08159cf-5263-430f-a16b-8d0683c5cb4c/download/arquivo-final-4-trim.-2021.csv
9b42cbd8-3d2e-4c9f-993e-6c49e62f1818/download/arquivo-final-3-trim.-2021.csv
3014d1de-8c16-4aa1-b03a-b8434905eab1/download/arquivo-final-1-trim.-2021.csv
a96a91e1-9328-4cf2-b77b-96865c978033/download/4-trimestre-2020.csv
b9c5aabf-bfe8-4933-95df-c880ff927dc0/download/3-trimestre-2020.csv
75356e9d-585d-4aa6-ac6c-b6245624623b/download/2-trimestre-2020.csv
91745827-93ac-4ef6-9055-21cc88b0d231/download/1-trimestre-2020.csv
""".split()

# Serviços que representam barreiras no caminho do pedestre
SERVICOS = re.compile(
    "Calçada pública - solicitar manutenção"
    "|Acessibilidade - solicitar avaliação de obstáculo na calçada"
    "|Calçada particular - denunciar calçada danificada"
    "|Sugerir construção de calçadas"
    "|Guia rebaixada - solicitar fiscalização"
    "|Guias para travessia de pedestres"
    "|Semáforo de veículos e pedestres"
    "|Travessia de pedestres - Solicitar avaliação"
    "|Sinalização horizontal apagada"
    "|Manutenção de semáforos"
)

# Nome padronizado -> padrão do cabeçalho original (sem acento, minúsculo)
COLUNAS = {
    "abertura": r"^data de abertura",
    "finalizacao": r"^data de finaliza",
    "canal": r"^(meio de comunica|canal)",
    "tema": r"^tema$",
    "assunto": r"^assunto$",
    "servico": r"^servico",
    "status": r"^status",
    "orgao": r"^orgao",
    "lat": r"^latitude",
    "lon": r"^longitude",
    "subprefeitura": r"^(prefeitura operacional|subprefeitura)",
    "distrito": r"^distrito",
}


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.replace("﻿", ""))
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").strip().lower()


def decodificar(conteudo: bytes) -> str:
    try:
        return conteudo.decode("utf-8")
    except UnicodeDecodeError:
        return conteudo.decode("latin-1")


def filtrar_arquivo(texto: str, nome: str) -> pd.DataFrame:
    cabecalho = texto.split("\n", 1)[0]
    sep = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
    leitor = csv.reader(io.StringIO(texto), delimiter=sep)
    nomes = [normalizar(c) for c in next(leitor)]
    idx = {k: next((i for i, n in enumerate(nomes) if re.search(p, n)), None) for k, p in COLUNAS.items()}
    if idx["servico"] is None:
        print(f"  {nome}: sem coluna 'Serviço', ignorado")
        return pd.DataFrame()

    linhas = []
    for row in leitor:
        get = lambda k: row[idx[k]].strip() if idx[k] is not None and idx[k] < len(row) else ""
        if SERVICOS.search(get("servico")):
            linhas.append({k: get(k) for k in COLUNAS})
    df = pd.DataFrame(linhas, columns=list(COLUNAS))
    if df.empty:
        return df

    # Formato de data: dd/mm/aaaa na maioria; um arquivo usa mm/dd/aaaa
    dmy = pd.to_datetime(df.abertura, format="%d/%m/%Y", errors="coerce")
    fmt = "%m/%d/%Y" if dmy.isna().mean() > 0.2 else "%d/%m/%Y"
    df["data_abertura"] = pd.to_datetime(df.abertura, format=fmt, errors="coerce")
    df["data_finalizacao"] = pd.to_datetime(df.finalizacao, format=fmt, errors="coerce")
    # Data de extração aproximada: a finalização mais recente registrada no arquivo
    df["data_extracao_arquivo"] = df.data_finalizacao.max()
    for c in ["lat", "lon"]:
        df[c] = pd.to_numeric(df[c].str.replace(",", "."), errors="coerce").round(3)
    df["arquivo_origem"] = nome
    return df


def main(saida: str = "sp156_barreiras_pedestre_2020_2026.csv.gz") -> None:
    partes = []
    for caminho in ARQUIVOS:
        nome = caminho.rsplit("/", 1)[-1]
        print(f"baixando {nome} ...", flush=True)
        with urlopen(BASE + caminho, timeout=300) as resp:
            texto = decodificar(resp.read())
        parte = filtrar_arquivo(texto, nome)
        print(f"  {len(parte):,} pedidos no recorte")
        partes.append(parte)

    df = pd.concat(partes, ignore_index=True)
    out = pd.DataFrame({
        "data_abertura": df.data_abertura.dt.strftime("%Y-%m-%d"),
        "data_finalizacao": df.data_finalizacao.dt.strftime("%Y-%m-%d"),
        "data_extracao_arquivo": df.data_extracao_arquivo.dt.strftime("%Y-%m-%d"),
        "canal": df.canal, "tema": df.tema, "assunto": df.assunto, "servico": df.servico,
        "status": df.status, "orgao": df.orgao, "lat_aprox": df.lat, "lon_aprox": df.lon,
        "subprefeitura": df.subprefeitura, "distrito": df.distrito, "arquivo_origem": df.arquivo_origem,
    }).replace("", pd.NA)
    out = out.sort_values(["data_abertura", "servico"]).reset_index(drop=True)
    out.to_csv(saida, index=False, compression="gzip")
    print(f"{len(out):,} pedidos salvos em {saida}")


if __name__ == "__main__":
    main(*sys.argv[1:])

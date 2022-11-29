import pandas as pd 
from pathlib import Path
from datetime import datetime
import re
from io import StringIO
from typing import List


raw_data_folder = Path(__file__).parent.parent /  "raw_data/IBGE"
data_folder = Path(__file__).parent.parent /  "data/IBGE"

def verifica_linha(linha: str) -> bool:
    """Verifica se a linha do log é do formato que contém dados."""
    reg = re.compile(r"\".*\";\".*?\";\"\d+\"")
    if reg.match(linha):
        return True
    else:
        return False
    


def extract_info(file_path : Path) -> str:
    with open(file_path) as fp:
        conteudo = fp.read()
    linhas = conteudo.split("\n")
    linhas_filtradas = [x for x in linhas if verifica_linha(x)]
    return "\n".join(linhas_filtradas)

def logfile_to_database(file_path : Path) -> pd.DataFrame:
    """Lê o arquivo de log do SISAB e retorna um dataframe"""
    dados = extract_info(file_path)
    df = pd.read_csv(StringIO(dados),sep=";",thousands=".")  
    df.set_index("Cód.", inplace=True)
    return df

def consolidate_dataframes(file_list : List[Path]) -> pd.DataFrame:
    DATAFRAMES = {}
    del_nome_municipio = False
    for arquivo in file_list:
        df = logfile_to_database(arquivo)
        if del_nome_municipio:
            df.drop(columns="Município", inplace=True)
        del_nome_municipio = True
        DATAFRAMES[arquivo.stem] = df

    return pd.concat([*DATAFRAMES.values()], axis=1)


if __name__ == "__main__": 
    lista_arquivos = raw_data_folder.glob("*.log")
    DF = consolidate_dataframes(lista_arquivos)
    DF.sort_index(axis=1, inplace=True)
    DF.to_csv(data_folder / "populacao_consolidada.csv")
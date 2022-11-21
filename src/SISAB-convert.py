
import pandas as pd 
from pathlib import Path
from datetime import datetime
import re
from io import StringIO
from typing import List

data_folder = Path(__file__).parent.parent /  "raw_data/SISAB"

def ref_from_filename(file_path : Path) -> tuple: 
    filename = file_path.stem
    return filename[:4], filename[4:]

def date_from_filename(file_path : Path ) -> datetime:
    """Recebe um Path do arquivo YYYYMM.log e retorna um datetime dessa data."""
    return datetime.strptime(file_path.stem, "%Y%m")

def verifica_linha(linha: str) -> bool:
    """Verifica se a linha do log é do formato que contém dados."""
    regex = re.compile(r"\w{2};")
    if regex.match(linha):
        return True
    else:
        return False

def extract_info(file_path : Path) -> str:
    with open(file_path, encoding="iso-8859-1") as fp:
        conteudo = fp.read()
    linhas = conteudo.split("\n")
    linhas_filtradas = [x for x in linhas if verifica_linha(x)]
    return "\n".join(linhas_filtradas)
    
def logfile_to_database(file_path : Path) -> pd.DataFrame:
    """Lê o arquivo de log do SISAB e retorna um dataframe"""
    dados = extract_info(file_path)
    df = pd.read_csv(StringIO(dados), encoding="iso-8859-1",sep=";",thousands=".")
    df.drop(columns=["Unnamed: 25"],inplace=True) 
    df["referencia"] = file_path.stem
    return df
 

def consolidate_dataframes(file_list : List[Path]) -> pd.DataFrame:
    DATAFRAMES = {}
    for arquivo in file_list:
        DATAFRAMES[arquivo.stem] = logfile_to_database(arquivo)
    return pd.concat([*DATAFRAMES.values()])



if __name__ == "__main__": 
    lista_arquivos = data_folder.glob("*.log")
    DF = consolidate_dataframes(lista_arquivos)
    DF.to_csv(data_folder / "SISAB-consolidado.csv", index=False, sep=",")
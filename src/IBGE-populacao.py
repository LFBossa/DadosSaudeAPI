import re
import json
from pathlib import Path
import requests
import datetime

RAW_DATA_PATH = Path(__file__).parent.parent / "raw_data"
DATA_PATH = Path(__file__).parent.parent / "data"

def get_tabela_url(ano : int):
    return f"https://sidra.ibge.gov.br/geratabela?format=br.csv&name=tabela6579.csv&terr=NC&rank=-&query=t/6579/n6/all/v/all/p/{ano}/l/v,p,t"

def get_request_text( URL : str ) -> str:
    pedido = requests.get(URL)
    pedido.encoding = pedido.apparent_encoding
    if pedido.status_code == 200:
        return pedido.text

if __name__ == "__main__":
    thisyear = (datetime.now()).year
    ANOS = range(2013,thisyear)
    for ano in ANOS:
        print(f"Downloading {ano} data")
        conteudo = get_request_text(get_tabela_url(ano)) 
        caminho = RAW_DATA_PATH / f"IBGE/{ano}.log"
        print(f"Writing {ano} data")
        with open(caminho, "w") as fp:
            fp.write(conteudo)


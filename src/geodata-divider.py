import re
import json
from pathlib import Path
import requests

RAW_DATA_PATH = Path(__file__).parent.parent / "raw_data"
DATA_PATH = Path(__file__).parent.parent / "data"
 
# https://servicodados.ibge.gov.br/api/docs/malhas?versao=2
def extract_regex(linha : str) -> tuple:
    regex = re.compile(r"\*\s(\w{2})\s/\s(.*?)\s-\s\[geojson/geojs-(\d{2})-")
    return regex.match(linha)

def json_or_none( URL : str ) -> str:
    pedido = requests.get(URL)
    if pedido.status_code == 200:
        return json.loads(pedido.text)

def get_cidades() -> dict:
    return json_or_none("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")

def get_estados() -> dict:
    return json_or_none("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    

def get_topologia( estado_id : int) -> dict:
    URL = f"https://servicodados.ibge.gov.br/api/v2/malhas/{estado_id}?resolucao=5&formato=application/json"
    return json_or_none(URL)

if __name__ == "__main__":
    estados = get_estados()
    cidades_lista = get_cidades()
    cidades_dict = {}
    for x in cidades_lista:
        cidades_dict[str(x["id"])] = x
    for estado in estados:
        topojson = get_topologia(estado["id"])
        for x in topojson["objects"]["foo"]["geometries"]:
            ibgeid = x["properties"]["codarea"]
            x["properties"]["municipio"] = cidades_dict[ibgeid]["nome"]
        caminho = DATA_PATH / f"geodata/{estado['sigla']}.topojson"
        with open(caminho, "w") as fp:
            json.dump(topojson, fp, ensure_ascii=False) 
      
    
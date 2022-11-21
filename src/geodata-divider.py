import re
import json
from pathlib import Path

RAW_DATA_PATH = Path(__file__).parent.parent / "raw_data"
DATA_PATH = Path(__file__).parent.parent / "data"
 

def extract_regex(linha : str) -> tuple:
    regex = re.compile(r"\*\s(\w{2})\s/\s(.*?)\s-\s\[geojson/geojs-(\d{2})-")
    return regex.match(linha)

def load_codigos_estados() -> dict:
    dados_estados = {}
    with open(RAW_DATA_PATH / "geodata-br/README.md") as fp:
        for linha in fp:
            resultado = extract_regex(linha)
            if resultado:
                uf, estado, cod  = resultado.group(1,2,3)
                dados_estados[estado.strip()] = (uf, cod)
    return dados_estados

def load_brazil() -> dict:
    with open( RAW_DATA_PATH / "geodata-br/brazil-geodata-raw.geojson") as fp:
        dados = json.load(fp)
    return dados
 

if __name__ == "__main__":
    estados = load_codigos_estados()
    brazil_geojson =  load_brazil()
    estados_geojson = {key: [] for key in estados.keys()}
    for elem in brazil_geojson['features']:
        uf = elem['properties']['UF']
        estados_geojson[uf].append(elem)
    
    for key, val in estados.items():
        uf, _ = val
        modelo = {"type":"FeatureCollection", "features": [] }
        modelo["features"] = estados_geojson[key] 
        with open(DATA_PATH / "geodata" / f"{uf}.geojson" , "w") as fp:
            json.dump(modelo, fp, ensure_ascii=False)
    
    
from pathlib import Path
import requests
import json
from operator import itemgetter
import numpy as np
import pandas as pd


RAW_DATA_PATH = Path(__file__).parent.parent / "raw_data"
DATA_PATH = Path(__file__).parent.parent / "data"


def json_or_none( URL : str ) -> str:
    pedido = requests.get(URL)
    if pedido.status_code == 200:
        return json.loads(pedido.text)


def get_estados() -> dict:
    return json_or_none("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    


def calcula_centroide(siglauf : str) -> dict:
    with open(DATA_PATH / "geodata" / f"{siglauf}.topojson") as fp:
        topodata = json.load(fp)
    centroides = np.array([ elem["properties"]["centroide"] 
        for elem in topodata["objects"]["foo"]["geometries"]
    ])
    mediana_long = np.median(centroides[:,0])
    mediana_lat = np.median(centroides[:,1])
    return {"lat": mediana_lat, "long": mediana_long}

def load_sisab() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "SISAB/SISAB-consolidado.csv", sep=",")


def estados_por_regiao() -> dict:
    estados = get_estados()
    REGIOES = []
    for uf in estados:
        labels = ["id", "sigla", "nome"]
        dados = itemgetter(*labels)(uf) 
        uf0 = dict(zip(labels, dados))
        #centroide = calcula_centroide(uf["sigla"])
        #uf0["centroide"] = centroide 
        # não preciso mais disso, uso o método fitBounds
        reg = uf["regiao"]["nome"]
        uf0["regiao"] = reg
        REGIOES.append(uf0) 
    return REGIOES



if __name__ == "__main__":
    REGIOES = estados_por_regiao()
    with open(DATA_PATH / "meta" / "estados.json", "w") as fp:
        json.dump(REGIOES, fp, ensure_ascii=False, indent=2)
    
    SISAB = load_sisab()
    LISTA_DOENCAS = {"doenças": list(SISAB.columns[3:-2].values)}
    with open(DATA_PATH / "meta" / "lista_doencas.json", "w") as fp:
        json.dump(LISTA_DOENCAS, fp, ensure_ascii=False, indent=2)



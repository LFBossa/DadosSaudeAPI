from fastapi import FastAPI
from typing import Union
import json
import pandas as pd 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

def load_file(path: str) -> str: 
    with open(path) as fp:
        return fp.read() 

 
def load_json(path: str) -> dict:
    with open(path) as fp:
        jsondict = json.load(fp)
    return jsondict

def dump_json(object: dict, path: str, **kwargs):
    with open(path, "w") as fp:
        json.dump(object, fp, **kwargs)


app = FastAPI()

origins = [ 
    "http://localhost",
    "http://localhost:8886",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


saude = pd.read_pickle("dados/saude-series.pd.pkl")
indices = pd.read_pickle("dados/indices.pd.pkl")

@app.get("/", response_class=HTMLResponse)
async def main():
    pagina = load_file("pages/index.html")
    return HTMLResponse(content=pagina, status_code=200)

@app.get("/saude/lista-doencas")
async def listadoencas(): 
    return load_json("dados/doencas-short.json")


@app.get("/saude/lista-municipios")
async def listamunicipios(regiao: Union[str, None] = None ):
    muni = pd.read_pickle("dados/municipios.pd.pkl") 
    if regiao:
        lista_regioes = load_json("dados/regioes-short.json")
        nome_regiao = lista_regioes[regiao]
        return muni.query(f"regiao == '{nome_regiao}'").to_dict(orient="records")
    else: 
        return muni.to_dict(orient="records")

@app.get("/saude/lista-regioes")
async def listaregioes(): 
    return load_json("dados/regioes-short.json")


@app.get("/saude/serie/{doenca_short}/{ibge}")
async def seriedoenca(doenca_short: str, ibge: int, por_mil: bool = False ):
    lista_doencas = load_json("dados/doencas-short.json")
    doenca = lista_doencas[doenca_short]
    if por_mil:
        pesquisa = indices.query(f"Ibge == {ibge}")[["referencia",doenca]].rename(columns={doenca: "atendimentos"})
    else:
        pesquisa = saude.query(f"Ibge == {ibge}")[["referencia",doenca]].rename(columns={doenca: "atendimentos"})
    return pesquisa.to_dict(orient="list")
 
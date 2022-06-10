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


SAUDE = pd.read_pickle("dados/saude-series.pd.pkl")
INDICES = pd.read_pickle("dados/indices.pd.pkl")
POPULACAO = pd.read_csv("dados/populacao.csv")
MUNICIPIOS = pd.read_pickle("dados/municipios.pd.pkl")
LISTA_DOENCAS = load_json("dados/doencas-short.json")
LISTA_REGIOES = load_json("dados/regioes-short.json")

@app.get("/", response_class=HTMLResponse)
async def main():
    pagina = load_file("pages/index.html")
    return HTMLResponse(content=pagina, status_code=200)


@app.get("/mapa", response_class=HTMLResponse)
async def main():
    pagina = load_file("pages/mapa.html")
    return HTMLResponse(content=pagina, status_code=200)

@app.get("/saude/lista-doencas")
async def listadoencas(): 
    return LISTA_DOENCAS


@app.get("/saude/lista-municipios")
async def listamunicipios(regiao: Union[str, None] = None ): 
    if regiao: 
        nome_regiao = LISTA_REGIOES[regiao]
        return MUNICIPIOS.query(f"regiao == '{nome_regiao}'").to_dict(orient="records")
    else: 
        return MUNICIPIOS.to_dict(orient="records")

@app.get("/saude/lista-regioes")
async def listaregioes(): 
    return LISTA_REGIOES


@app.get("/saude/serie/{doenca_short}/{ibge}")
async def seriedoenca(doenca_short: str, ibge: int, por_mil: bool = False ): 
    doenca = LISTA_DOENCAS[doenca_short]
    if por_mil:
        pesquisa = INDICES.query(f"Ibge == {ibge}")[["referencia",doenca]].rename(columns={doenca: "atendimentos"})
    else:
        pesquisa = SAUDE.query(f"Ibge == {ibge}")[["referencia",doenca]].rename(columns={doenca: "atendimentos"})
    return pesquisa.to_dict(orient="list")



@app.get("/populacao/")
async def populacao(ibge: Union[int, None] = None , regiao: Union[str, None] = None ):
    if ibge:
        pesquisa = POPULACAO.query(f"IBGE == {ibge}")
        return pesquisa.to_dict(orient="records")[0]
    elif regiao:
        região = LISTA_REGIOES[regiao]
        lista_ibge = MUNICIPIOS.query(f"regiao == '{região}'").ibge.unique()
        return POPULACAO.query(f"IBGE in {list(lista_ibge)}").sum().to_dict()
    else:
        raise HTTPException(status_code=400, detail="A requisição precisa ter um parâmetro ibge ou regiao não nulos") 
 
@app.get("/saude/estado/{doenca_short}/")
async def saudeestado(doenca_short: str, ano: int):
    doenca = LISTA_DOENCAS[doenca_short]
    series = SAUDE.query(f"ano == {ano}").groupby("Ibge").sum()[doenca]/POPULACAO.set_index("IBGE")[str(ano)]*1000
    return series.to_dict()


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


import pandas as pd 
from pathlib import Path
import json

raw_data_folder = Path(__file__).parent.parent /  "raw_data"
data_folder = Path(__file__).parent.parent /  "data"

def load_sisab() -> pd.DataFrame:
    df = pd.read_csv(data_folder / "SISAB/SISAB-populacao.csv", sep=",")
    return df
  
 


if __name__ == "__main__":
    # carrega o sisab
    sisab = load_sisab()
    ESTADOS = sisab.Uf.unique()
    for uf in ESTADOS:
        print(f"Agregando {uf}")
        ESTADO_DICT = {}
        estado_df = sisab.query(f"Uf == '{uf}'")
        CIDADES = estado_df.Municipio.unique()
        for muni in CIDADES:
            cidade_df = estado_df.query(f"Municipio == \"{muni}\"").sort_values("referencia")
            ibge_cod, nome = cidade_df.iloc[0, [1,2]].values
            ibge_cod = str(ibge_cod)
            ESTADO_DICT[ibge_cod] = {"Município": nome}
            ESTADO_DICT[ibge_cod].update(
                cidade_df[cidade_df.columns[3:]].to_dict(orient="list")
            )
        with open(data_folder / f"SISAB/SISAB-{uf}.json", "w") as fp:
            json.dump(ESTADO_DICT, fp, ensure_ascii=False)


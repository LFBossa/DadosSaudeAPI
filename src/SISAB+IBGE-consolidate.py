import pandas as pd 
from pathlib import Path


raw_data_folder = Path(__file__).parent.parent /  "raw_data"
data_folder = Path(__file__).parent.parent /  "data"

def load_sisab() -> pd.DataFrame:
    df = pd.read_csv(data_folder / "SISAB/SISAB-consolidado.csv", sep=",")
    df.Municipio = df.Municipio.str.title()
    return df

def load_ibge() -> pd.DataFrame:
    return pd.read_csv(data_folder / "IBGE/populacao_consolidada.csv", sep=",")
 
def ibge_code_dict(ibge_df : pd.DataFrame)-> dict:
    """O SISAB não tem o DV do código IBGE. Essa função retorna um dicionário
    {\d{6}: \d{7}} que permite associar o DV à cada código
    """ 
    return {x//10: x for x in ibge["Cód."]}

def add_dv_ibge(mapa: dict, cod: int) -> int:
    return mapa[cod]

def match_populacao_referencia(sisab_row, ibge_df):
    codibge = sisab_row["Ibge"]
    ano = sisab_row["referencia"]//100
    populacao = None
    while populacao is None:
        try:
            populacao = ibge_df.loc[codibge, str(ano)]
        except KeyError:
            # tenta pegar do ano atual, se der ruim, reduz o ano em 1
            ano -= 1
    return populacao


if __name__ == "__main__":
    # carrega o sisab
    sisab = load_sisab()
    # carrega ibge
    ibge = load_ibge()
    # cria o mapeamento
    mapa_dv = ibge_code_dict(ibge)
    # coloca o ibge com indice como o código
    ibge.set_index("Cód.", inplace=True)
    # adiciona o DV no código 
    sisab.Ibge = sisab.Ibge.apply( lambda x: add_dv_ibge(mapa_dv, x))

    calcula_pop = lambda row: match_populacao_referencia(row, ibge)
    sisab["populacao"] = sisab.apply(calcula_pop, axis=1)

    sisab.to_csv(data_folder / 'SISAB/SISAB-populacao.csv', index=False)


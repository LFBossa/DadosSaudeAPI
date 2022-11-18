import requests
from time import sleep
import json


def get_SUSera(headers_raw, ano_dados,mes_dados):
    """Vamos importar dados do SUS na MARRA""" 
    headers = {key: val.strip() for (key, val) in [ x.split(":", maxsplit=1) for x in headers_raw.split("\n")]}
    url = headers["Referer"]
    payload_raw = """j_idt44=j_idt44
lsCid=
dtBasicExample_length=10
lsSigtap=
td-ls-sigtap_length=10
unidGeo=estado
estados=SC
selectLinha=MUN.CO_MUNICIPIO_IBGE
selectcoluna=PCA
idadeInicio=0
idadeFim=0
tpIdade=
tpProducao=4 
tabela_length=10
javax.faces.ViewState=-618364827450665268:-2729416449945736178
j_idt192=j_idt192"""
    payload = {key: val.strip() for (key, val) in [ x.split("=", maxsplit=1) for x in payload_raw.split("\n")]}
    payload["j_idt76"] =  ["{ano}{:02d}".format(mes_dados,ano=ano_dados)]
    payload["condicaoAvaliada"] = ["ABP{:03d}".format(x) for x in [9, 6, 10, 5, 7, 11, 12, 14, 18, 17, 23, 22]]
    payload["tipoAtendimento"] = [1,2,4,5,6]
    # O seu token está visível apenas pra você
    response = requests.post(url, headers=headers,data=payload)
    if response.status_code == 200:
        return response.text
    else:
        return response.status_code

if __name__ == "__main__":
    headers = """Host: sisab.saude.gov.br
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 713
Origin: https://sisab.saude.gov.br
Connection: keep-alive
Referer: https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/saude/RelSauProducao.xhtml;jsessionid=x+yOlKywigRisCru9HiAAsUl
Cookie: _ga=GA1.3.600333197.1649334263; JSESSIONID=x+yOlKywigRisCru9HiAAsUl; BIGipServersisab_prod=1946230188.22560.0000; TS0116db68=01f6470b2fafdf7d989cacc4e92a2f8e91cfb807dcec0c32d3b0ba111a5c7ea26c9a70f51e0704c42b93761623982bedfb3a84d6c021bf62f335dd9c8478af00a7ec38f4caa8cbbdb4ee03e2686f9d6af337532456; _gid=GA1.3.500987628.1649959631
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1"""
    referencia = input("Digite a referência: ")
    ano = int(referencia[:4])
    mes = int(referencia[4:6])

    print(ano, mes, sep="\t")

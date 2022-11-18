import requests
from time import sleep
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_SUSera(headers_raw, cookies, ano_dados,mes_dados):
    """Vamos importar dados do SUS na MARRA""" 
    line_headers = headers_raw.split("\n")
    headers = {key: val.strip() for (key, val) in [ x.split(":", maxsplit=1) for x in line_headers[1:]]}
    _, urlpath, _ = line_headers[0].split(" ")
    url = headers["Referer"]
    payload_raw = """j_idt44=j_idt44
lsCid=
dtBasicExample_length=10
lsSigtap=
td-ls-sigtap_length=10
unidGeo=brasil
j_idt76=202207
selectLinha=MUN.CO_MUNICIPIO_IBGE
selectcoluna=PCA
idadeInicio=0
idadeFim=0
tpIdade=
tpProducao=4 
tabela_length=10
javax.faces.ViewState=7902303290776419962%3A635397846698827681
j_idt192=j_idt192"""
    payload = {key: val.strip() for (key, val) in [ x.split("=", maxsplit=1) for x in payload_raw.split("\n")]}
    payload["j_idt76"] =  ["{ano}{:02d}".format(mes_dados,ano=ano_dados)]
    payload["condicaoAvaliada"] = ["ABP{:03d}".format(x) for x in [9, 6, 10, 5, 7, 11, 12, 14, 18, 17, 23, 22]] 
    # O seu token está visível apenas pra você
    print(url)
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    else:
        return response.status_code


def multiline_input(message):
    print(f"{message} {bcolors.UNDERLINE}[Ctrl-D or Ctrl-Z ( windows ) to save it.]{bcolors.ENDC}")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)

if __name__ == "__main__":
    #20headers = multiline_input("Insira o header: ")
    headers = """POST /paginas/acessoRestrito/relatorio/federal/saude/RelSauProducao.xhtml HTTP/1.1
Host: sisab.saude.gov.br
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 310
Origin: https://sisab.saude.gov.br
Connection: keep-alive
Referer: https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/saude/RelSauProducao.xhtml;jsessionid=C8BeSZyD48Kxw+-EfVIkn6AS
Cookie: JSESSIONID=uD9jz-lvJ2Neuo8zPojQwmHn; BIGipServerpool_sisab_jboss=!LjAP3jK4LYSgF3Oi4dOS8fa1J/wqqRxmdZBiRlRGAKLDcNuZsctBlJt1UJc/RRWUBNNmHGX+yI8Znak=
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1"""
    cookies = {
		"BIGipServerpool_sisab_jboss": "!LjAP3jK4LYSgF3Oi4dOS8fa1J/wqqRxmdZBiRlRGAKLDcNuZsctBlJt1UJc/RRWUBNNmHGX+yI8Znak=",
		"JSESSIONID": "uD9jz-lvJ2Neuo8zPojQwmHn"
	}
    #referencia = input("Digite a referência (YYYYMM): ")
    #ano = int(referencia[:4])
    #mes = int(referencia[4:6])
    print(get_SUSera(headers, None, 2022, 5))


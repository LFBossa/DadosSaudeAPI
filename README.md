# Dados de Saúde API
API estática de dados para o mapa da saúde brasileiro. 
Os scripts desse repositório fazem os seguintes trabalhos:

* Rodam um bot selenium que faz download dos dados do SISAB;
* Capturam os dados de fronteiras dos municípios utilizando a API do IBGE;
* Capturam os dados de população utilizando o SIDRA do IBGE;
* Consolidam todos esses dados em arquivos topojson e json;

# Instalação

* Tenha [`pipenv`](https://pipenv.pypa.io/en/latest/) instalado em sua máquina

```shell
git clone git@github.com:LFBossa/DadosSaudeAPI.git
cd DadosSaudeAPI
pipenv install
```

# Baixando os dados

Tendo o `make` instalado em sua máquina, basta rodar o comando 

```shell
make all
```

e os dados serão automaticamente baixados e processados.
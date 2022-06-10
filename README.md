# MapaSaudeSC-API
API de dados para o mapa da saúde SC

# Instalação

* Tenha [`pipenv`](https://pipenv.pypa.io/en/latest/) instalado em sua máquina

```shell
git clone git@github.com:LFBossa/DadosSaudeAPI.git
cd DadosSaudeAPI
pipenv install
```

# Rodando o servidor

```shell
pipenv shell
uvicorn main:app --reload --port=8886
```

pythoncommand := pipenv run python
delcommand := rm -f

directories:
	mkdir -p raw_data/IBGE
	mkdir -p raw_data/SISAB
	mkdir -p raw_data/temp
	mkdir -p data/geodata
	mkdir -p data/IBGE
	mkdir -p data/meta
	mkdir -p data/SISAB

all: directories
	$(pythoncommand) src/IBGE-populacao.py
	$(pythoncommand) src/IBGE-populacao-convert.py
	$(pythoncommand) src/IBGE-geodata.py
	$(pythoncommand) src/SISAB-bot.py
	$(pythoncommand) src/SISAB-convert.py
	$(pythoncommand) src/SISAB+IBGE-consolidate.py
	$(pythoncommand) src/atendimentos-por-estado.py
	$(pythoncommand) src/Metadados.py
 

clear: 
	$(delcommand) raw_data/IBGE/*
	$(delcommand) raw_data/SISAB/*
	$(delcommand) raw_data/temp/*
	$(delcommand) data/geodata/*
	$(delcommand) data/IBGE/*
	$(delcommand) data/meta/*
	$(delcommand) data/SISAB/*

.PHONY: clear populacao geodata sisab aggregate
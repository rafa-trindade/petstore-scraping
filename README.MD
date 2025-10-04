# 🐾 petstore-scraper

Projeto de **scraping** para coletar informações de lojas (franquias) do setor pet, estruturando os dados em formato padronizado para análise, consulta e integração.  

O projeto segue a arquitetura **Extract → Transform**, onde os dados brutos coletados (extract) são tratados e padronizados (transform) antes de serem salvos.  

Os dados coletados por este scraper são preparados para uso no projeto [**`petstore-bi`**](https://github.com/rafa-trindade/petstore-bi), servindo como fonte de carga (load) para dashboards e análises.

## 📌 Descrição
O `petstore-scraper` automatiza a coleta de dados de pet shops e franquias do segmento pet.  
Ele permite extrair informações como **endereço, telefone, horários de funcionamento, serviços e produtos oferecidos**, facilitando análises regionais e integração com sistemas externos.

O projeto segue a arquitetura **Extract → Transform**:  

- **Extract:** cada scraper coleta dados brutos das páginas das redes Petz, Petlove e Petland e salva em CSVs na pasta `data/raw/`.  
- **Transform:** os arquivos brutos são processados e padronizados em CSVs limpos na pasta `data/processed/`, prontos para análise e integração.

## 📊 Dados coletados
Os dados extraídos são estruturados no seguinte formato:

| empresa   | franquia | nome da loja | endereço | bairro | cidade | estado | CEP | telefone | horário de funcionamento | produtos para | serviços disponíveis |
|-----------|----------|--------------|----------|--------|--------|--------|-----|----------|--------------------------|---------------|-----------------------|

## 🚀 Possíveis usos
- Consultar todas as lojas de uma franquia específica.  
- Mapear presença de lojas por cidade/estado.  
- Identificar disponibilidade de serviços oferecidos em diferentes regiões.  
- Construir dashboards e análises.

## ⚙️ Tecnologias
- [selenium](https://pypi.org/project/selenium/) → automação de navegação e captura de páginas dinâmicas  
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) → parsing de HTML  
- [lxml](https://pypi.org/project/lxml/) → processamento rápido de HTML/XML  
- [pandas](https://pypi.org/project/pandas/) → manipulação e estruturação de dados  

## 📂 Saída
- **Raw:** CSVs brutos na pasta `data/raw/` (ex.: `petz_raw.csv`).  
- **Processed:** CSVs tratados e padronizados na pasta `data/processed/` (ex.: `petz_processed.csv`).  

## 📊 Redes suportadas
Atualmente, o projeto coleta dados das seguintes redes:

- **Petz** 🐶🐱  
- **Petlove** 💙  
- **Petland** 🌎  

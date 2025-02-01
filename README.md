# Testador de Velocidade de Internet
Um script simples em Python para medir a velocidade de download, upload e ping da sua conexão à internet. Os resultados são armazenados em um arquivo CSV para histórico e análise posterior.

## 📋 Funcionalidades
Mede a velocidade de download e upload (em Mbps).
Mede o ping (em ms).
Armazena os resultados com data e hora em um arquivo log_velocidade.csv.

## 🚀 Como usar
Certifique-se de ter o Python instalado (versão 3.7 ou superior).

Instale a biblioteca necessária:
pip install speedtest-cli

Baixe ou clone este repositório:
git clone https://github.com/GabrielFSantana/testador-de-velocidade.git

Navegue até o diretório do projeto:
cd testador-de-velocidade

Execute o script:
python testador.py

## 📊 Exemplo de Saída
Quando você executar o script, verá algo assim no terminal:

Teste de Velocidade de Internet
Download: 120.45 Mbps
Upload: 30.78 Mbps
Ping: 15.23 ms
Resultado salvo em log_velocidade.csv!

## 📂 Estrutura do Projeto
testador-de-velocidade/
testador.py         # Script principal
log_velocidade.csv  # Arquivo gerado com os logs (após a execução)
README.md           # Documentação do projeto

## 🛠️ Tecnologias Usadas
Python
Speedtest CLI

## 📖 Como funciona
O script utiliza a biblioteca speedtest-cli para medir a velocidade de internet.
Os resultados são exibidos no terminal e salvos no arquivo log_velocidade.csv.
Se o arquivo CSV não existir, ele será criado automaticamente.

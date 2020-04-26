#Projeto 'Desafio Nasa' para vaga de engenheiro de dados na Semantix
###Feito por Gustavo Pedroso em 25/04/2020
###Testado em OS: Windows 10 Professional

##Arquivos Importantes
* respostas.txt (arquivo com as respostas para as perguntas dissertativas)
* exec_log.txt (arquivo com os logs de execução do código main.py)
* Desafio_NASA.pdf (arquivo com a descrição original do desafio)

## Para executar o código cerfique-se de ter:
* python versão 3.7 ou compatível com spark 2.4.5 (3.8 não é compatível)
* spark 2.4.5
* java 8
* variáveis de ambiente configuradas (JAVA_HOME, SPARK_HOME)
* arquivos de dados (NASA logs) na pasta correta (data) seguindo nomenclatura como em main.py

## Quando os pontos acima estiverem verificados, execute a aplicação usando uma das formas abaixo:
* Na pasta raiz do projeto execute: python src/main.py
* Na pasta raiz do projeto execute: spark-submit src/main.py

Obs: usando o spark-submit a quantidade de logs do Spark dificulta a leitura. É possível reduzir a verbosidade através do arquivo de configuração log4j.properties


# Exercícios bootcamp semantix engenheiro de dados

## Spark

Iniciar docker em sua maquina:


1. Instalação do docker e docker-compose

2. Executar os seguintes comandos, para baixar as imagens do Cluster de Big Data:

git clone https://github.com/rodrigo-reboucas/docker-bigdata.git spark
cd spark
docker-compose –f docker-compose-parcial.yml pull
3. Iniciar o cluster Hadoop através do docker-compose

docker-compose –f docker-compose-parcial.yml up -d
4. Listas as imagens em execução

5. Verificar os logs dos containers do docker-compose em execução

6. Verificar os logs do container jupyter-spark

7. Acessar pelo browser o Jupyter, através do link:

http://localhost:8889


### Spark com Kafka

> docker exec -it kafka bash

> kafka-topics --bootstrap-server kafka:9092 --topic topicTeste --create --partitions 1 --replication-factor 1 

>kafka-console-consumer --boostrap-server kafka:9092 --topic topicTeste

>kafka-console-producer --broker-list kafka:9092 --topic topicTeste --property parse.key=true --property key.separator=,

#### iniciando no shell
>spark-shell --packages org.apache.spark:spark-streaming-kafka-0-10_2.11:2.4.1


# Exercícios bootcamp semantix engenheiro de dados

## Kafka

### Iniciando o docker
docker-compose up -d

### Entrando no Broker
docker exec -it broker bash

### Kafka topics
kafka-topics --version

#### listar
kafka-topics --bootstrap-server localhost:9092 --list

#### criar
kafka-topics --bootstrap-server localhost:9092 --topic <nometopico> --create --partitions 3 --replication-factor 1


kafka-topics --bootstrap-server localhost:9092 --create --topic msg-cli --partitions 2 --replication-factor 1


#### descrever tópico
kafka-topics --bootstrap-server localhost:9092 --topic <nometopico> --describe
kafka-topics --bootstrap-server localhost:9092 --topic msg-cli --describe

#### deletar tópico
kafka-topics --bootstrap-server localhost:9092 --topic <nometopico> --delete

### kafka produtores

#### enviar
kafka-console-producer --broker-list localhost:9092 --topic <nometopico>
kafka-console-producer --broker-list localhost:9092 --topic msg-cli

#### enviar para todos
kafka-console-producer --broker-list localhost:9092 --topic <nometopico> acks=all

### kafka consumidores

#### mensagens em tempo real
kafka-console-consumer --bootstrap-server localhost:9092 --topic <nometopico>
kafka-console-consumer --bootstrap-server localhost:9092 --topic msg-cli --group app-cli

#### mensagens desde a criação do tópico
kafka-console-consumer --bootstrap-server localhost:9092 --topic <nometopico> --from-beginning

#### criar grupo de consumidores
kafka-console-consumer --bootstrap-server localhost:9092 --topic <nometopico> --group <nomegrupo>

#### listar grupos de consumidores
kafka-consumer-groups --bootstrap-server localhost:9092 --list

#### descrever grupo
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group <nomegrupo>


#### redefinir o deslocamento do mais antigo
kafka-consumer-groups --bootstrap-server localhost:9092 --group <nomegrupo> --reset-offsets --to-earliest --execute --topic <nometopico>


#### anterar o deslocamento
kafka-consumer-groups --bootstrap-server localhost:9092 --group <nomegroup> --reset-offsets --shift-by -2 --execute --topic <nometopico>

kafka-consumer-groups --bootstrap-server localhost:9092 --reset-offset --shift-by -2 --execute --topic msg-cli --group app-cli
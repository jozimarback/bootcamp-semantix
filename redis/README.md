# Exercícios bootcamp semantix engenheiro de dados

## Redis

### Iniciando o docker
docker-compose up -d

#### redis iniciar
docker exec -it redis bash

redis-cli

#### redis inserir
SET usuario:nome Jozimar
SET usuario:sobrenome Back
SET views:qtd 100

#### redis obter
get usuario:nome
get views:qtd
strlen usuario:nome

#### redis veririfcar tipo
type usuario:sobrenome

#### redis incrementar valor
incrby views:qtd 10

#### redis deletar valor
del usuario:sobrenome

#### redis definir tempo de vida de uma chave em segundos
expire views:qtd 3600
##### verificar tempo de vida
ttl view:qtd
##### setar ao infinito
persist views:qtd
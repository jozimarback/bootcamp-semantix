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

#### redis listas
rpush views:ultimo_usuario Joao Ana
lpush views:ultimo_usuario Carlos
rpush views:ultimo_usuario Carol

##### recuperar itens da lista
lrange views:ultimo_usuario 0 -1

lrange views:ultimo_usuario 0 -2

##### tamanho da lista
llen views:ultimo_usuario

##### redefinir tamanho da lista removendo o primeiro
ltrim views:ultimo_usuario 1 -1

##### obter primeiro ou ultimo
lpop views:ultimo_usuario
rpop views:ultimo_usuario

##### obter primeiro ou ultimo com tempo de espera
blpop views:ultimo_usuario 5
brpop views:ultimo_usuario 5

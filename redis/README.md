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

#### redis sets
##### adicionar
sadd pesquisa:produto monitor mouse teclado
sadd pesquisa:desconto 'memoria ram' monitor teclado HD
##### contar quantidade
scard pesquisa:produto
##### listar
smembers pesquisa:produto
##### se existe valor
sismember pesquisa:produto monitor
##### remover
srem pesquisa:produto monitor
spop pesquisa:produto
##### interseção
sinter pesquisa:produto pesquisa:desconto
##### diferença
sdiff pesquisa:produto pesquisa:desconto
##### criar a partir de união
sunionstore pesquisa:produto_desconto pesquisa:produto pesquisa:desconto


#### redis sets ordenados
##### adicionar
zadd pesquisa:produto 100 monitor 200 HD 10 mouse 50 teclado
##### contar quantidade
zcard pesquisa:produto

##### listar menor para maior
zrange pesquisa:produto 0 -1
zrank pesquisa:produto 0 -1

##### listar maior para menor
zrevrank pesquisa:produto 0 -1
zrevrange pesquisa:produto 0 -1

##### remover um item
zrem pesquisa:produto HD
zpopmax pesquisa:produto


#### Hash
hmset usuario:100 nome Augusto estado SP views 10

hgetall

##### contar quantidade de campos
hlen usuario:100

##### ver multiplos campos
hmget usuario:100 nome views

##### contar caracteres valor de um campo
hstrlen usuario:100 nome

##### incrementar
hincrby usuario:100 views 2

##### vizualizar campos
hkeys usuario:100

##### visualizar valores
kvals usuario:100

##### deletar chave
hdel usuario:100

#### PubSub

##### criar assinante
subscribe noticias:sp
psubscribe noticias:*

##### criar publicador
publish noticias:sp 'Msg 1'
publish noticias:sp 'Msg 2'
publish noticias:sp 'Msg 3'
publish noticias:rj 'Msg 4'
publish noticias:rj 'Msg 5'
publish noticias:rj 'Msg 6'

#####  cancelar assinatura
ctrl+c


#### Ler configuração do servidor
config get *

config get appendonly
config set appendonly no

config get save
config set save '120 500'

config get maxmemory*
config set maxmemory-policy allkeys-lru
config set maxmemory 1mb

####links
[tyr.redis](http://try.redis.io)
[redis.io/commands](https://redis.io/commands)
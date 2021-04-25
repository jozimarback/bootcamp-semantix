# Exercícios bootcamp semantix engenheiro de dados

## Levantando ambiente de estudo

### Clone ambiente
git clone https://github.com/rodrigo-reboucas/docker-bigdata.git

### Entrando na pasta
cd docker-bigdata

### Baixando imagens do docker
docker-compose pull

### Levantando docker compose
docker-compose up -d

### Ver quais serviços estão rodando
docker-compose ps

### Analisar logs dos serviços
docker-compose logs

### Analisar log de um serviço especifico
docker-compose logs namenode

### Entrar na linha de comando de um container 
docker exec -it namenode bash

### Executar comando de listagem de pastas dentro de um container
docker exec -it namenode ls

### Encerrar uso de ambiente docker compose
docker-compose down


## HDFS

### clonar dados em sua maquina
git clone https://github.com/rodrigo-reboucas/exercises-data.git

### Criar pasta e subpastas recursivamente
hdfs dfs -mkdir -p /user/aluno/jozimar/data

### Enviar arquivos locais para hdfs
hdfs dfs -put  /input/exercises-data/entrada1.txt /user/aluno/jozimar/data

### Listar recursivamente
hdfs dfs -ls -R /user/aluno/jozimar/data

### Mover arquivos
hdfs dfs -mv  /user/aluno/jozimar/data/entrada1.txt /user/aluno/jozimar/recover

### Remover pasta recursivamente no hdfs
hdfs dfs -rm -R  /user/aluno/jozimar/recover

### Encontrar arquivos no hdfs
hdfs dfs -find /user -name alunos.csv

### Ver inicio do arquivo
hdfs dfs -cat /user/aluno/jozimar/data/escola/alunos.csv | head -n 2

### Checksum
hdfs dfs -checksum /user/aluno/jozimar/data/escola/alunos.csv

## Fator de replicação do arquivo no cluster
hdfs dfs -setrep 2 /user/aluno/jozimar/data/escola/alunos.csv

### Ajuda em algum comando
hdfs dfs -help stat


### Saber status/informações do arquivo
hdfs dfs -stat %o /user/aluno/jozimar/data/escola/alunos.csv

### Espaço livre no cluster
hdfs dfs -df -h /user/aluno/jozimar/data/

### Espaço usado no cluster
hdfs dfs -du -h /user/aluno/jozimar/data/

## HIVE


### adicionar arquivo ao hdfs
docker exec -it namenode bash
hdfs dfs -mkdir /user/aluno/jozimar/data/populacao/7
hdfs dfs -put /input/exercises-data/populacaoLA/populacaoLA.csv /user/aluno/jozimar/data/populacao/

### Utilizar container HIVE
docker exec -it hive-server bash

### Utilizar jdbc
beeline --help
beeline -u jdbc:hive2://localhost:10000

### mostrar tabelas hive
show databases;

### criar tabelas
create database jozimar;

### Criar tabela HIVE
use jozimar;
create table pop(
    zip_code int,
    total_population int,
    median_age float,
    total_males int,
    total_females int,
    total_households int,
    average_household_size float
) 
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties("skip.header.line.count"="1");

### descrever campos tabela
desc pop;
desc formatted pop;

### carregar dados para tabela
load data inpath '/user/aluno/jozimar/data/populacao/' overwrite into table pop

### seleção de dados
select * from pop limit 10;
select count(1) from pop;


### sair do hive
ctrl + d

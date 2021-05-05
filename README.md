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

### Tabela particionada
docker exec -it namenode hdfs dfs -mkdir /user/aluno/jozimar/data/nascimento
docker exec -it namenode hdfs dfs -ls /
docker exec -it hive-server bash
beeline -u jdbc:hive2://localhost:10000
use jozimar;
create external table nascimento(nome string, sexo string, frequencia int) partitioned by (ano int) row format delimited fields terminated by ',' lines terminated by '\n' stored as textfile location '/user/aluno/jozimar/data/nascimento';

alter table nascimento add partition(ano=2015)

hdfs dfs -ls /user/aluno/jozimar/data/nascimento
hdfs dfs -put /input/exercises-data/names/yob2015.txt /user/aluno/jozimar/data/nascimento/ano-2015

### Formato e compressão de arquivos
create table pop_parquet(zip_code int, total_population int, median_age float, total_males int, total_females int, total_households int, average_household_size float) stored as parquet;


insert into pop_parquet select * from pop;

create table pop_parquet_snappy(zip_code int, total_population int, median_age float, total_males int, total_females int, total_households int, average_household_size float) stored as parquet tblproperties('parquet.compress'='SNAPPY');


insert into pop_parquet_snappy select * from pop;

### sair do hive
ctrl + d

## Sqoop

### importação de dados mysql

### copiar dados para dentro do conteiner
docker cp input/exercises-data/db-sql/ database:/

docker exec -it database bash

ls /db-sql/
mysql -h localhost -u root -psecret

### criar base de dados sakila
cd /db-sql/sakila/
mysql -h localhost -u root -psecret < sakila-mv-schema.sql
mysql -h localhost -u root -psecret < sakila-mv-data.sql

### usando sqoop
docker exec -it namenode bash
sqoop list-databases --connect jdbc:mysql://database --username root --password secret
sqoop list-tables --connect jdbc:mysql://database/employees --username root --password secret
sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "select * from departments"
sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "insert into departments values('d010','BI')"
sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "create table benefits(cod int(2)  AUTO_INCREMENT PRIMARY KEY, name varchar(30))"
sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "insert into benefits values(null,'food vale')"

### importar tabelas
sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "select * from employees limit 10"

sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --warehouse-dir /user/hive/warehouse/db_test_a

hdfs dfs -ls -h /user/hive/warehouse/db_test_a/employees

sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --where "gender-'M'" --warehouse-dir /user/hive/warehouse/db_test_b

sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --columns "first_name,last_name" --fields-terminated-by '\t' --warehouse-dir /user/hive/warehouse/db_test_c

sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --columns "first_name,last_name" --lines-terminated-by ':' --warehouse-dir /user/hive/warehouse/db_test_c --delete-target-dir

### compressão de arquivo
sqoop import --table titles --connect jdbc:mysql://database/employees --username root --password secret -m 8 --as-parquetfile --warehouse-dir /user/hive/warehouse/db_test2_4

sqoop import --table titles --connect jdbc:mysql://database/employees --username root --password secret -m 5 --as-parquetfile --warehouse-dir /user/hive/warehouse/db_test2_5 --compress --compression-codec org.apache.hadoop.io.compress.SnappyCodec

sqoop import -Dorg.apache.sqoop.splitter.allow_text_splitter=true --table cp_titles_date --connect jdbc:mysql://database/employees --username root --password secret -m 4 --warehouse-dir /user/hive/warehouse/db_test2_title --split-by title

hdfs dfs -ls -h -R /user/hive/warehouse/db_test2_title

### pratica com carga incremental
docker exec -it database bash
mysql -psecret
use sakila;
show tables;
create table cp_rental_append select rental_id,rental_date from rental;
create table cp_rental_id select * from cp_rental_append;
create table cp_rental_date select * from cp_rental_append;

docker exec -it namenode bash

sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --table cp_rental_append

sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --table cp_rental_id

sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --table cp_rental_date

hdfs dfs -ls -R /user/hive/warehouse/db_test3

docker exec -it database bash
apt-get update
apt-get install apt-file
vi insert_rental.sql
mysql -psecret < insert_rental.sql

docker exec -it namenode bash
sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --append --table cp_rental_append
sqoop eval --connect jdbc:mysql://database/sakila --username root --password secret --query "select * from cp_rental_append order by rental_id desc limit 5"

sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --incremental append --table cp_rental_id --check-column rental_id --last-value 16049

sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --incremental lastmodified --merge-key rental_id --table cp_rental_date --check-column rental_date --last-value '2005-08-23 22:50:12.0'

sqoop import  --table titles --connect jdbc:mysql://database/employees --username root --password secret --warehouse-dir /user/aluno/jozimar/data -m 1


sqoop import  --table titles --connect jdbc:mysql://database/employees --username root --password secret -m 1 --hive-import --hive-table jozimar.titles

sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "truncate table titles"

sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "select * from titles limit 10"

sqoop export --table titles --connect jdbc:mysql://database/employees --username root --password secret --hive-table jozimar.titles --export-dir /user/aluno/jozimar/data/titles
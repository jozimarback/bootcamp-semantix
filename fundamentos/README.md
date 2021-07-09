# Exercícios bootcamp semantix engenheiro de dados

## Levantando ambiente de estudo

### Clone ambiente
>git clone https://github.com/rodrigo-reboucas/docker-bigdata.git

### Entrando na pasta
>cd docker-bigdata

### Baixando imagens do docker
>docker-compose pull

### Levantando docker compose
>docker-compose up -d

### Ver quais serviços estão rodando
>docker-compose ps

### Analisar logs dos serviços
>docker-compose logs

### Analisar log de um serviço especifico
>docker-compose logs namenode

### Entrar na linha de comando de um container 
>docker exec -it namenode bash

### Executar comando de listagem de pastas dentro de um container
>docker exec -it namenode ls

### Encerrar uso de ambiente docker compose
docker-compose down


## HDFS

### clonar dados em sua maquina
>git clone https://github.com/rodrigo-reboucas/exercises-data.git

### Criar pasta e subpastas recursivamente
>hdfs dfs -mkdir -p /user/aluno/jozimar/data

### Enviar arquivos locais para hdfs
>hdfs dfs -put  /input/exercises-data/entrada1.txt /user/aluno/jozimar/data

### Listar recursivamente
>hdfs dfs -ls -R /user/aluno/jozimar/data

### Mover arquivos
>hdfs dfs -mv  /user/aluno/jozimar/data/entrada1.txt /user/aluno/jozimar/recover

### Remover pasta recursivamente no hdfs
>hdfs dfs -rm -R  /user/aluno/jozimar/recover

### Encontrar arquivos no hdfs
>hdfs dfs -find /user -name alunos.csv

### Ver inicio do arquivo
>hdfs dfs -cat /user/aluno/jozimar/data/escola/alunos.csv | head -n 2

### Checksum
>hdfs dfs -checksum /user/aluno/jozimar/data/escola/alunos.csv

## Fator de replicação do arquivo no cluster
>hdfs dfs -setrep 2 /user/aluno/jozimar/data/escola/alunos.csv

### Ajuda em algum comando
>hdfs dfs -help stat


### Saber status/informações do arquivo
>hdfs dfs -stat %o /user/aluno/jozimar/data/escola/alunos.csv

### Espaço livre no cluster
>hdfs dfs -df -h /user/aluno/jozimar/data/

### Espaço usado no cluster
>hdfs dfs -du -h /user/aluno/jozimar/data/

## HIVE


### adicionar arquivo ao hdfs
>docker exec -it namenode bash

>hdfs dfs -mkdir /user/aluno/jozimar/data/populacao/7

>hdfs dfs -put /input/exercises-data/populacaoLA/populacaoLA.csv /user/aluno/jozimar/data/populacao/

### Utilizar container HIVE
>docker exec -it hive-server bash

### Utilizar jdbc
>beeline --help

>beeline -u jdbc:hive2://localhost:10000

### mostrar tabelas hive
>show databases;

### criar tabelas
>create database jozimar;

### Criar tabela HIVE
>use jozimar;

```
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
```
### descrever campos tabela
>desc pop;

>desc formatted pop;

### carregar dados para tabela
>load data inpath '/user/aluno/jozimar/data/populacao/' overwrite into table pop

### seleção de dados
>select * from pop limit 10;

>select count(1) from pop;

### Tabela particionada
>docker exec -it namenode hdfs dfs -mkdir /user/aluno/jozimar/data/nascimento

>docker exec -it namenode hdfs dfs -ls /

>docker exec -it hive-server bash

>beeline -u jdbc:hive2://localhost:10000

>use jozimar;

>create external table nascimento(nome string, sexo string, frequencia int) partitioned by (ano int) row format delimited fields terminated by ',' lines terminated by '\n' stored as textfile location '/user/aluno/jozimar/data/nascimento';

>alter table nascimento add partition(ano=2015)

>hdfs dfs -ls /user/aluno/jozimar/data/nascimento

>hdfs dfs -put /input/exercises-data/names/yob2015.txt /user/aluno/jozimar/data/nascimento/ano-2015

### Formato e compressão de arquivos
>create table pop_parquet(zip_code int, total_population int, median_age float, total_males int, total_females int, total_households int, average_household_size float) stored as parquet;


>insert into pop_parquet select * from pop;

>create table pop_parquet_snappy(zip_code int, total_population int, median_age float, total_males int, total_females int, total_households int, average_household_size float) stored as parquet tblproperties('parquet.compress'='SNAPPY');


>insert into pop_parquet_snappy select * from pop;

### sair do hive
ctrl + d

## Sqoop

### importação de dados mysql

### copiar dados para dentro do conteiner
>docker cp input/exercises-data/db-sql/ database:/

>docker exec -it database bash

>ls /db-sql/

>mysql -h localhost -u root -psecret

### criar base de dados sakila
>cd /db-sql/sakila/

>mysql -h localhost -u root -psecret < sakila-mv-schema.sql

>mysql -h localhost -u root -psecret < sakila-mv-data.sql

### usando sqoop
>docker exec -it namenode bash

>sqoop list-databases --connect jdbc:mysql://database --username root --password secret

>sqoop list-tables --connect jdbc:mysql://database/employees --username root --password secret

>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "select * from departments"

>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "insert into departments values('d010','BI')"

>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "create table benefits(cod int(2)  AUTO_INCREMENT PRIMARY KEY, name varchar(30))"

>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "insert into benefits values(null,'food vale')"

### importar tabelas
>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "select * from employees limit 10"

>sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --warehouse-dir /user/hive/warehouse/db_test_a

>hdfs dfs -ls -h /user/hive/warehouse/db_test_a/employees

>sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --where "gender-'M'" --warehouse-dir /user/hive/warehouse/db_test_b

>sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --columns "first_name,last_name" --fields-terminated-by '\t' --warehouse-dir /user/hive/warehouse/db_test_c

>sqoop import --table employees --connect jdbc:mysql://database/employees --username root --password secret --columns "first_name,last_name" --lines-terminated-by ':' --warehouse-dir /user/hive/warehouse/db_test_c --delete-target-dir

### compressão de arquivo
>sqoop import --table titles --connect jdbc:mysql://database/employees --username root --password secret -m 8 --as-parquetfile --warehouse-dir /user/hive/warehouse/db_test2_4

>sqoop import --table titles --connect jdbc:mysql://database/employees --username root --password secret -m 5 --as-parquetfile --warehouse-dir /user/hive/warehouse/db_test2_5 --compress --compression-codec org.apache.hadoop.io.compress.SnappyCodec

>sqoop import -Dorg.apache.sqoop.splitter.allow_text_splitter=true --table cp_titles_date --connect jdbc:mysql://database/employees --username root --password secret -m 4 --warehouse-dir /user/hive/warehouse/db_test2_title --split-by title

>hdfs dfs -ls -h -R /user/hive/warehouse/db_test2_title

### pratica com carga incremental
>docker exec -it database bash

>mysql -psecret

>use sakila;

>show tables;

>create table cp_rental_append select rental_id,rental_date from rental;

>create table cp_rental_id select * from cp_rental_append;

>create table cp_rental_date select * from cp_rental_append;

>docker exec -it namenode bash

>sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --table cp_rental_append

>sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --table cp_rental_id

>sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --table cp_rental_date

>hdfs dfs -ls -R /user/hive/warehouse/db_test3

>docker exec -it database bash

>apt-get update

>apt-get install apt-file

>vi insert_rental.sql

>mysql -psecret < insert_rental.sql

>docker exec -it namenode bash

>sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --append --table cp_rental_append

>sqoop eval --connect jdbc:mysql://database/sakila --username root --password secret --query "select * from cp_rental_append order by rental_id desc limit 5"

>sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --incremental append --table cp_rental_id --check-column rental_id --last-value 16049

>sqoop import --connect jdbc:mysql://database/sakila --username root --password secret --warehouse-dir /user/hive/warehouse/db_test3 -m 1 --incremental lastmodified --merge-key rental_id --table cp_rental_date --check-column rental_date --last-value '2005-08-23 22:50:12.0'

>sqoop import  --table titles --connect jdbc:mysql://database/employees --username root --password secret --warehouse-dir /user/aluno/jozimar/data -m 1

>sqoop import  --table titles --connect jdbc:mysql://database/employees --username root --password secret -m 1 --hive-import --hive-table jozimar.titles

>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "truncate table titles"

>sqoop eval --connect jdbc:mysql://database/employees --username root --password secret --query "select * from titles limit 10"

>sqoop export --table titles --connect jdbc:mysql://database/employees --username root --password secret --hive-table jozimar.titles --export-dir /user/aluno/jozimar/data/titles

## HBase

>docker exec -it hbase-master bash

>hbase version

>hbase shell

>create 'controle',{NAME=>'produto'},{NAME=>'fornecedor'}

>put 'controle','1','produto:nome','ram'

>put 'controle','2','produto:nome','hd'

>put 'controle','3','produto:nome','mouse'

>scan 'controle'

>put 'controle','1','produto:qtd','100'

>put 'controle','2','produto:qtd','50'

>put 'controle','3','produto:qtd','150'

>put 'controle','1','fornecedor:nome','TI Comp'

>put 'controle','2','fornecedor:nome','Peças PC'

>put 'controle','3','fornecedor:nome','Inf Rec'

>put 'controle','1','fornecedor:estado','SP'

>put 'controle','2','fornecedor:estado','MG'

>put 'controle','3','fornecedor:estado','SP'

>describe 'controle'

>count 'controle'

>alter 'controle',{NAME=>'produto',VERSIONS=>3}

>describe 'controle'

>put 'controle','2','produto:qtd','200'

>get 'controle','2', {COLUMNS=>['produto:qtd'], VERSION=>2}

>help "get"

>scan 'controle',{COLUMNS=>'fornecedor:estado', LIMIT => 2}

>scan 'controle',{COLUMNS=>'fornecedor:estado', LIMIT => 5,"ValueFilter(=, 'binary:SP')"}

>deleteall 'controle','1'

>deleteall 'controle','3'

>delete 'controle','2','fornecedor:estado'


## Spark Scala
>hdfs dfs -put /input/exercises-data/juros_selic/ /user/aluno/jozimar/data

>docker exec -it spark bash

>spark-shell

>val jurosDF = spark.read.json("/user/aluno/rodrigo/data/juros_selic/juros_selic.json")

>jurosDF.show(5,false)

>jurosDF.count()
### salvar no hive
>val jurosDF10 = jurosDF.where("valor > 10")

>jurosDF10.show()

>jurosDF10.write.saveAsTable("jozimar.tab_juros_selic")

### ler do hive
>val jurosHiveDF = spark.read.table("jozimar.tab_juros_selic")

>jurosHiveDF.printSchema

>jurosHiveDF.show(5)
### salvar no hdfs
>jurosHiveDF.write.parquet("/user/aluno/jozimar/data/save_juros")

>docker -it namenode bash

>hdfs dfs -ls /user/aluno/jozimar/data/save_juros

### ler do hdfs
>val jurosHDFS = spark.read.load("/user/aluno/jozimar/data/save_juros")
ou
>val jurosHDFS = spark.read.load("hdfs://namenode:8080/user/aluno/jozimar/data/save_juros")

>jurosHDFS.printSchema
>jurosHDFS.show(5)

### join
>val alunosDF = spark.read.option("header","true").option("inferSchema","true").csv("/user/aluno/jozimar/data/escola/alunos.csv")

>alunosDF.printSchema

>alunosDF.show(3)

>alunosDF.write.saveAsTable("jozimar.tab_alunos")#salvar no hive

>val cursosDF = spark.read.option("header","true").option("inferSchema","true").csv("/user/aluno/jozimar/data/escola/cursos.csv")

>val alunos_cursosDF = alunosDF.join(cursosDF, "id_curso")

>alunos_cursosDF.show(10)

### spark catalog
>spark.catalog.listDatabases.show(false)

>spark.catalog.setCurrentDatabase("jozimar")

>spark.catalog.listTables.show

>spark.catalog.listColumns("tab_alunos").show

>spark.read.table("tab_alunos").show(10)

>spark.sql("select * from tab_alunos limit 10")

### spark sql queries vs dataframe

>spark.sql("select id_discente, nome from tab_alunos limt 5").show

>spark.read.table("tab_alunos").select("id_discente", "nome").limit(5).show

>spark.sql("select id_discente, nome, ano_ingresso from tab_alunos where ano_ingresso >= 2018").show

>spark.read.table("tab_alunos").select("id_discente", "nome", "ano_ingresso").where("ano_ingresso>=2018").show


>spark.sql("select id_discente, nome, ano_ingresso from tab_alunos where ano_ingresso >= 2018 order by nome desc").show

>spark.read.table("tab_alunos").select("id_discente", "nome", "ano_ingresso").where("ano_ingresso>=2018").orderBy($"nome".desc).show
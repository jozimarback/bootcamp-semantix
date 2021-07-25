[link download imagem](https://hub.docker.com/r/academysemantix/docker-cdh-611)

> docker pull academysemantix/docker-cdh-611

>docker build . -t academysemantix/docker-cdh-611

>docker run -d -p 8050:8050 -p 8051:8051 -p 21000:21000 -p 21050:21050 -p 25000:25000 -p 25010:25010 -p 25020:25020 -p 50070:50070 -p 50075:50075 -p 8888:8888 -p 9999:9999 -p 50111:50111 -p 10002:10002 -v ~/input:/home/input -v ~/output:/home/output --name cdh6 academysemantix/docker-cdh-611

>docker ps

>docker exec -it cdh6 ls /

>docker cp ../data/ cdh6:/home/input

> docker exec -it cdh6 bash


### olhar hdfs

>hdf dfs -ls /

### entrar no hive e executar

>hive

>hive>show databases;


> ctrl+ d 
### executar impala

>impala-shell

#### quando em produção sempre entrar no worker e nunca no master

>impala-shell -i worker1

> ctrl+ d 

#### criar pasta hdfs
>hdfs dfs -mkdir /user/jozimar

>hdfs dfs -mkdir /user/jozimar/data




> docker stop cdh6

> docker start cdh6


### comandos

#### Exercicio hdsf
```
$> hdfs dfs -ls /user/jozimar/data
```

>  hdfs dfs -put /home/input/populacaoLA/populacaoLA.csv  /user/jozimar/data/

> hdfs dfs -put /home/input/populacaoLA/populacaoLA.csv  /user/jozimar/data/


#### Criar tabela hive
> create database jozimar;

> use jozimar;


```
hive> create table pop(
    zip_cod int,
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

```
hive> show create table pop;
```

```
hive> desc formatted pop;
hive> desc pop;
```

```
hive> load data inpath '/user/jozimar/data/populacaoLA.csv' overwrite into table pop;
```

ou caso queria mover manualmente do hdfs

```
$ hdfs dfs -mv /user/rodrigo/data/populacaoLA.csv /user/hive/warehouse/jozimar.db/pop
```

Criar tabela como resumo de outra
```
hive> create table pop_resumo as select zip_cod, total_population, median_age from pop;
```

```
$ hdfs dfs -tail /user/hive/warehouse/rodrigo.db/pop_resumo/000000_0
```

> create table pop_resumo as select zip_cod, total_population, median_age from pop

> insert overwrite directory '/user/jozimar/tab_pop_resumo' row format delimited fields terminated by '\b' select * from pop_resumo;

criar tabela externa
```
hive> create external table nascimento(
    nome string,
    sexo string
    frequencia int
)
partitioned by (ano int)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
location '/user/jozimar/data/nascimento';

hive> alter table nascimento add partition(ano=2015);
```

### partition e buckets
Para perfoamnce em campos classificadores utilizar particionamento.
Para perfomance em campos numericos utilizar buckets

para criar buckets automaticamente

>hive> SET hive.enforce.bucketing=true

patição dinamica

>hive> insert overwrite table user_cidade partition(cidade) select * from user;

mostrar partições

>hive> show partitions user;

alterar nome da partição

>hive> alter table user partition city rename to partition state;

excluir partição

>hive> alter table user drop partition (city='SP');

reparar tabela sincronizando tabela com metastore quando não encontrar partição

>msck repair table <nome_tabela>

### exercicio

> hdfs dfs -mkdir /user/jozimar/data/nascimento

```
>hive> create external table nascimento(
    nome string,
    sexo string,
    frequencia int
)
partitioned by (ano int)
row format delimited
fields terminated by ','
line terminated by '\n'
stored as textfile
locations '/user/jozimar/data/nascimento'
```

>hive> alter table nascimento add partition(ano=2015);

>hdfs dfs -put /home/input/data/names/yob2015.txt /user/jozimar/data/nascimento/ano=2015

>hive> alter table nascimento add partition(ano=2016);

>hive> alter table nascimento add partition(ano=2017);

>hdfs dfs -put /home/input/data/names/yob2016.txt /user/jozimar/data/nascimento/ano=2016

>hdfs dfs -put /home/input/data/names/yob2017.txt /user/jozimar/data/nascimento/ano=2017

### formato de arquivos

```
>hive> create table pop_parquet stored as parquet as select * from pop;
```

```
>hive> create table pop_parquet_snappy stored as parquet tblproperties('parquet.compress'='snappy') as select * from pop;
```

> hdfs dfs -ls -h -R /user/hive/warehouse/jozimar.db


```
>hive> create table pop_avro_separado stored as avro tblproperties('avro.schema.literal'='{"name":"pop","type":"record","fields":[{"name":"zip_cod","type":"int"},{"name":"total_population","type":"int"}]}') as select * from pop_parquet;
```

### criar tabela com map ou struct

Exemplo de dados
>a,Alice,home:555-1111|work:555-2222

```
hive> create table customer_phones(
    cust_id string,
    name string,
    phones MAP<string,string>
)
row format delimited
fields terminated by ','
collection items terminated by '|'
map keys terminatd by ':'

hive> select name, phones['home'] as home FROM customers_phones;
```


Exemplo de dados
>a,Alice,742 Evergreen Terrace|Springfield|OR|97477

```
hive> create table customers_addr(
    cust_id string,
    name string,
    address STRUCT<street:string
        ,city:string
        ,state:string
        ,zipcode:string
    >
)
row format delimited
fields terminated by ','
collection items terminated by '|';

hive> select name, address.street as home FROM customers_addr;
```

SerDe LazySimple

```
hive> create table people(fname string, lname string)
row format SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
with serdeproperties('field.delim'='\t');
```

SerDe Regex

>10309296107596201608290122150akland              CA94618

```
hive> create table fixed(cust_id int, order_dt string, order_tm string, city string, state, string, n string)
row format serde 'org.apache.hadoop.hive.serde2.RegexSerDe'
with serdeproperties("input.regex"="(\\d{7})(\\d{7})(\\d{8})(\\d{6})(.{20})(\\w{2})(\\d{5})");
```

SerDe OpenCSV

>3,"Bitmoney, Inc.", "bmi@example.com"

```
create table vendors(id int, name string, email string)
row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde';
```


### analise de frases

```
hive> SELECT txt FROM phrases WHERE id=12345
```

>I bought this compiter and I love it. It's super fast.


```
hive> SELECT setences(txt) FROM phrases WHERE id=12345
```

>[["I" ,"bought" ,"this" ,"compiter" ,"and", "I", "love", "it"], ["It's", "super", "fast"]]

```
hive> SELECT explode(ngrams(setences(txt)),2,4) FROM phrases WHERE id=12345
```

>{"ngram":["i","love"],"estfrequency":3.0}
{"ngram":["it","it's"],"estfrequency":2.0}

### plano de executação
>hive explain select * from user;

>impala> select * from user;
>impala> profile;

Explain no impala


| Valor  | Nome      | Descrição                                                  |
| ------ | --------- | ---------------------------------------------------------- |
| 0      | MINIMAL   | Util para validacao de sequencia de join em queries longas |
| 1      | STANDARD  | Mostra o caminho logico  de trabalho (defaul)              |
| 2      | EXTENDED  | Detalha como é o plano usando estatistica                  |
| 3      | VERBOSE   | Primariamente usado por desenvolvedores impala             |

impala> SET EXPLAIN_LEVEL=0;
impala> EXPLAIN SELECT COUNT(o.order_id) FROM orders o JOIN order_details d ON (o.order_id = d.order_id) WHERE YEAR(o.order_date) = 2008;

hive spark

>hive>SET hive.execution.engine=mr;

>hive>SET hive.execution.engine=spark;
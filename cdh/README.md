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




> docker stop cdh6

> docker start cdh6


### comandos

#### olhar hdsf
```
$> hdfs dfs -ls /user/jozimar/data
```

#### Criar tabela hive
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
lines terminated by '\'
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
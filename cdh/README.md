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
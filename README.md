# Execicios bootcamp semantix engenheiro de dados

## Comandos HDFS
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

## Ver inicio do arquivo
hdfs dfs -cat /user/aluno/jozimar/data/escola/alunos.csv | head -n 2

## Checksum
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
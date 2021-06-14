# Exercícios bootcamp semantix engenheiro de dados

## Elastic

### Iniciando o docker
>docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.2

>docker pull docker.elastic.co/kibana/kibana:7.9.2

>docker pull docker.elastic.co/logstash/logstash:7.9.2

>docker-compose up -d

#### comando exercicio 1 pelo dev_tool do http://localhost:5601/

```
GET produto/_count
```

```
DELETE produto/_doc/4
```

```
GET produto/_doc/1
```

```
POST produto/_update/3
{
  "doc":{
    "qtd":30
  }
}
```

verificar se existe
```
HEAD produto/_doc/3
```

```
POST produto/_doc/4
{
    "nome": "cpu", "qtd": 15, "descricao": "i5, 2.5Ghz"
}
```

```
POST produto/_doc/3
{
    "nome": "memória ram", "qtd": 10, "descricao": "8GB, DDR4"
}
```

```
POST produto/_doc/2
{
   "nome": "hd", "qtd": 20, "descricao": "Interface USB 2.0, 500GB, Sistema: Windows 10, Windows 8, Windows 7 "
}
```

```
POST produto/_doc/1
{
  "nome": "mouse", "qtd": 50, "descricao": "com fio USB, compatível com Windows, Mac e Linux"
}
```

buscar

```
GET populacao/_search
```
buscar com filtro

```
GET cliente/_search?q=hadoop
```

```
GET cliente/_search?q=nome:João&q=idade:20
```

buscar paginado

```
GET cliente/_search
{
  "from":0,
  "size":10,
  "query":{
    ...
  }
}
```


fechar e abrir indice
```
GET cliente/_close
```

```
GET cliente/_open
```

ver propriedades/campos de um indice

```
GET produto/_mapping
```
reindex
```
PUT produto2/_mapping
{
  "properties":{
    ...propriedades de mapeamento do indice produto anterando os tipos de campos que vc quiser
  }
}
```

```
POST _reindex 
{
  "source":{
    "index": "produto"
  },
  "dest": {
    "index": "produto2"
  }
}
```

assim produto2 recebe os dados com a nova tipagem e o antigo indice pode ser fechado

```
POST produto/_close
```

query & filtros

[Term](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)

```
GET produto/_search
{
  "query": {
    "term": {
      "nome": {
        "value": "mouse"
      }
    }
  }
}
```

```
GET produto/_search
{
  "query": {
    "terms": {
      "nome": ["mouse","teclado"]      
    }
  }
}
```

```
GET produto/_search
{
  "query": {
    "constant_score":{
      "filter":{
        "term": {
          "nome": "mouse"
        }
      }
    }
  }
}
```

```
GET produto/_search
{
  "query": {
    "match":{
      "descricao": "USB"
    }
  }
}
```


```
GET produto/_search
{
  "query": {
    "bool":{
      "must":[{
        "match":{"descricao": "USB"}
      }],
      "must_not": [{
        "match":{"descricao":"linux"}
      }]
    }
  }
}
```

```
GET produto/_search
{
  "query": {
    "bool":{
      "should":[{
        "match":{"nome":"memória"}
      },{
        "match":{"descricao": "USB"}
      }],
      "must_not": [{
        "match":{"descricao":"linux"}
      }]
    }
  }
}
```

Ordem busca com operadores

```
GET produto/_search
{
  "query":{
    "match":{
      "descricao":{
        "query": "windows linux",
        "operator:"and"
      }
    }
  }
}
```
O padrão de busca é operator OR, então quando buscar por algo que deve conter um ou outro não é necesário  informar o operator

```
GET produto/_search
{
  "query":{
    "match":{
      "descricao":  "windows linux usb"
    }
  }
}
```


```
GET produto/_search
{
  "query":{
    "match":{
      "descricao":{
        "query": "windows linux usb",
        "minimum_should_match":2
      }
    }
  }
}
```


```
GET produto/_search
{
  "query":{
    "match":{
      "descricao":{
        "query": "windows linux usb",
        "minimum_should_match":"50%"
      }
    }
  }
}
```

Range
```
GET populacao/_search
{
  "query": {
    "range": {
      "Total Population":{
        "lt":100
      } 
    }
  }
}
```

```
GET populacao/_search
{
  "query": {
    "range": {
      "Median Age":{
        "gt":70
      } 
    }
  }
}
```

```
GET populacao/_search
{
  "size":20,
  "query": {
    "range": {
      "Zip COde":{
        "get": 90056,
        "lte": 90067
      } 
    }
  }
}
```


```
GET bolsa/_search
{
  "query":{
    "range":{
      "timestamp":{
        "gte": "2019-01-01",
        "lte": "2019-03-01",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```


```
GET bolsa/_search
{
  "query":{
    "range":{
      "timestamp":{
        "gte": "2019-04-01",
        "lte": "now",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

Elastic Analyzer

- [referencia](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)
- [exemplo](https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html)


```
POST _analyze
{
  "analyzer": "simple",
  "text": "O elasticsearch surgiu em 2010"
}
```

```
POST _analyze
{
  "analyzer": "brazilian",
  "text": "O elasticsearch surgiu em 2010"
}
```

```
PUT produto
{
  "mappings": {
    "properties": {
      "descricao":{
        "type": "text",
        "analyzer": "brazilian"
      }
    }
  }
}
```

```
PUT produto1{
  "settings":{
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings":{
    "properties":{
      "descricao":{
        "type": "text",
        "analyzer": "brazilian"
      }
    }
  }
}
```

```
POST _reindex
{
  "source": {
    "index": "produto"
  },
  "dest": {
    "index": "produto1"
  }
}
```

```
DELETE produto
```

```
POST _reindex
{
  "source": {
    "index": "produto1"
  },
  "dest": {
    "index": "produto"
  }
}
```

Agregações

```
GET bolsa/_search
{
  "size":0,
  "aggs":{
    "media":{
      "avg": {
        "field": "volume"
      }
    }
  }
}
```


```
GET bolsa/_search
{
  "size":0,
  "aggs":{
    "estatistica":{
      "stats": {
        "field": "close"
      }
    }
  }
}
```

```
GET bolsa/_search
{
  "query":{
    "range":{
      "@timestamp":{
        "gte":"2019-04-01",
        "lte":"now"
      }
    }
  },
  "aggs":{
    "estatistica":{
      "stats": {
        "field": "open"
      }
    }
  }
}
```


```
GET bolsa/_search
{
  "size":0,
  "aggs":{
    "mediana":{
      "percentiles": {
        "field": "open",
        "percents":[
          1,5,25,50,75,95,99
        ]
      }
    }
  }
}
```
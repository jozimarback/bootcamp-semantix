# Exercícios bootcamp semantix engenheiro de dados

## MongoDB


### Iniciando o docker
docker-compose up -d

### Listando bases
docker exec -it mongo bash
mongo
show dbs

### Utilizando uma base de dados
use jozimar
db.createCollection('produto')
db.nomeColecao.renameColection('cliente')

db.produto.insertMany([
    {_id: 1, "nome": "cpu i5", "qtd": 15},
    {_id: 2, nome: "memória ram", qtd: 10, descricao: {armazenamento: "8GB", tipo:"DDR4"}},
    {_id: 3, nome: "mouse", qtd: 50, descricao: {conexao: "USB", so: ["Windows", "Mac", "Linux"]}},
    {_id: 4, nome: "hd externo", "qtd": 20, descricao: {conexao: "USB", armazenamento: "500GB", so: ["Windows 10", "Windows 8", "Windows 7"]}}
])

db.produto.find()

### consultas
db.produto.find({nome: "mouse"})

db.produto.find({quantidade: 20},{nome:1,_id:0})

db.produto.find({quantidade:{$lte: 20}},{nome:1, qtd:1,_id:0})

db.produto.find({quantidade:{$gte:10,$lte: 20}},{nome:1, qtd:1,_id:0})

db.produto.find({"descricao.conexao":"USB"},{nome:1, qtd:0,_id:0})

db.produto.find({"descricao.so":{$in:["Windows","Windows10"]}})

db.produto.find().sort({nome:1}).pretty()

db.produto.findOne({"descricao.conexao":"USB"})
db.produto.find({"descricao.conexao":"USB", qtd:{$lt: 25}})

db.produto.find({$or:[{"descricao.conexao":"USB"}, {qtd:{$lt: 25}}]})
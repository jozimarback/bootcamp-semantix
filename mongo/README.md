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
    {_id: 1, "nome": "cpu i5", "qtd": "15"},
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

### Update

db.produto.updateOne({ _id:1 }, { $set:{nome:'cpu i7'}})
db.produto.updateOne({ _id:1 }, { $set:{qtd:15}})

db.produto.updateMany({ qtd:{$gte:30} }, { $set:{qtd:30}})
db.produto.updateMany({}, { $rename:{ "descricao.so": "descricao.sistema" }})

db.produto.updateMany({"descricao.conexao":"USB"}, { $set:{ "descricao.conexao": "USB 2.0" }})

#### adicionando data de alteração
db.produto.updateMany(
    {"descricao.conexao":"USB 2.0"}, 
    { 
        $set: { "descricao.conexao": "USB 3.0" },
        $currentDate: { data_modificacao: { $type:"date" } }
    }
)

#### update em array
##### alterar
db.produto.updateOne({_id:3, "descricao.sistema": "Windows"},{$set:{"descricao.sistema.$": "Windows 10"}})
##### adicionar
db.produto.updateOne({_id:4 },{$push:{"descricao.sistema": "Linux"}})
##### remover
db.produto.updateOne({_id:3 },{$pull:{"descricao.sistema": "Mac"}, $currentDate:{ts_modificado:{$type:"timestamp"}}})

### Remover

db.createCollection('tes/te')
db.teste.insertOne({usuario:''Semantix,data_acesso: new Date()})

db.teste.find(data_acesso: {$gte: Date('2020')}})
db.teste.find(data_acesso: {$gte: ISODate('2020-01-01')}})

db.teste.updateOne({usuario:"Semantix"},{$currentDate:{data_acesso: {type:"timestamp"}}})

db.teste.deleteOne({_id:ObjectId(...)})
db.teste.drop()


### Indices

db.produto.CreateIndex({nome:1},{name:"query_produto"})

db.produto.getIndexes()

db.produto.find.explain()

db.produto.find().hint("nome":1)

db.produto.find().hint("nome":1).explain()

db.produto.dropIndex({nome:1})
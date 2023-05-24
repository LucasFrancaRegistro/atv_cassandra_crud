import pymongo
client = pymongo.MongoClient("mongodb+srv://programa:o5ma5JcTMMNPbydk@cluster0.ephuxat.mongodb.net/?retryWrites=true&w=majority")
database = client.test
import redis
conR = redis.Redis(host='redis-10721.c261.us-east-1-4.ec2.cloud.redislabs.com',
                  port=10721,
                  password='123senha')
import pickle

global db
db = client.mercadolivre

def insertVendedor():
    from usuario_crud import createEndereco
    global db
    col = db.vendedor
    nome = input('nome do vendedor: ')
    email = input('email do vendedor: ')
    cpf = input('cpf do vendedor: ')
    enderecos = []
    while True:
        enderecos.append(createEndereco())
        resposta = input('quer adicionar outro endereço? (y/n) ')
        if resposta == 'n':
            break
    doc = {"nome": nome,
        "email": email,
        "cpf": cpf,
        'endereço': enderecos,
        'produtos': []
        }
    x = col.insert_one(doc)
    print(x.inserted_id)

def sortVendedor():
    global db
    col = db.vendedor
    docs = col.find().sort('nome')
    objetos = []
    for obj in docs:
        objetos.append(obj)
    return objetos

def updateVendedor():
    from usuario_crud import updateEndereco
    from compras_crud import search
    global db
    col = db.vendedor
    vendedores = search(sortVendedor())
    vendedor = vendedores[int(input("Escolha o vendedor que deseja editar: "))]
    print('''O que deseja editar? 
    Nome
    Email
    Cpf
    Endereço
    Produtos''')
    escolha = input("Escreva a sua opção: ").lower()
    if escolha == "endereço":
        updateEndereco(vendedor)
    elif escolha == "produtos":
        updateVendedorProdutos(vendedor)
    else:
        valor = input("valor novo ")
        toUpdate = { "$set": { escolha: valor} }
        query = { "_id": vendedor["_id"]}
        col.update_one(query, toUpdate)

def updateVendedorProdutos(vendedor):
    from compras_crud import search
    from produto_crud import sortProduto
    global db
    col = db.vendedor
    vendaProdutos = vendedor["produtos"]
    print('''O que deseja fazer?
    1:  Adicinar aos produtos vendidos
    2:  Remover dos produtos vendidos''')
    escolha = input('Escolha uma opção: ')
    if escolha == '1':
        produtos = search(sortProduto())
        produto = produtos[int(input("escolha o produto que quer adicionar: "))]
        del produto["vendedor"]
        vendaProdutos.append(produto)
    elif escolha == '2':
        for index in range(len(vendaProdutos)):
            print(str(index) + ':' + str(vendaProdutos[index]))
        vendaProdutos.pop(int(input("Escolha o produto para remover: ")))
    query = { "_id": vendedor["_id"]}
    toUpdate = {"$set":{ "produtos": vendaProdutos}}
    col.update_one(query, toUpdate)

def deleteVendedor():
    from compras_crud import search
    global db
    col = db.vendedor
    vendedores = search(sortVendedor())
    escolha = int(input("Vendedor a deletar: "))[vendedores[escolha]["_id"]]
    query = { "_id": vendedor['_id'] }
    col.delete_one(query)

def syncRedisVendEnd():
    from compras_crud import search
    vendedores = search(sortVendedor())
    vendedor = vendedores[int(input("Escolha o vendedor: "))]
    enderecos = vendedor["endereço"]
    if conR.exists(vendedor["email"]+"-endereco") > 0:
        conR.delete(vendedor["email"]+"-endereco")
    for endereco in enderecos:
        conR.lpush(vendedor["email"]+"-endereco", pickle.dumps(endereco))

def syncMongoVendEnd():
    from compras_crud import search
    global db
    col = db.vendedor
    vendedores = search(sortVendedor())
    vendedor = vendedores[int(input("Escolha o vendedor: "))]
    enderecosMongo = []
    enderecosRedis = conR.lrange(vendedor["email"]+"-enderecos", 0, -1)
    for endereco in enderecosRedis:
        enderecosMongo.append(pickle.loads(endereco))
    query = { "_id": vendedor["_id"]}
    toUpdate = {"$set":{ "endereço": enderecosMongo}}
    col.update_one(query, toUpdate)

#deleteVendedor()
#insertVendedor()
#updateVendedor()
import pymongo
client = pymongo.MongoClient("mongodb+srv://programa:o5ma5JcTMMNPbydk@cluster0.ephuxat.mongodb.net/?retryWrites=true&w=majority")
database = client.test
#print(db)

global db
db = client.mercadolivre

def insertProduto():
    from compras_crud import search
    from vendedor_crud import sortVendedor
    global db
    col = db.produtos
    nome = input('nome do produto: ')
    quantidade = int(input('quantidade de produtos: '))
    preco = int(input('preço do produto: '))
    foto = input('link da foto do produto: ')
    vendedores = search(sortVendedor())
    escolha = int(input("Escolha o vendedor: "))
    vendedor = vendedores[escolha]
    del vendedor["produtos"]
    doc = {"nome": nome,
        "quantidade": quantidade,
        "preço": preco,
        "vendedor": vendedor,
        "foto": foto}
    col.insert_one(doc)

def updateProduto():
    from compras_crud import search
    from vendedor_crud import sortVendedor
    global db
    col = db.produtos
    produtos = search(sortProduto())
    escolha = int(input("produto a editar: "))
    produto = produtos[escolha]
    campo = input("campo para editar: ")
    if campo == "vendedor":
        vendedores = search(sortVendedor())
        escolha = int(input("Escolha o vendedor: "))
        vendedor = vendedores[escolha]
        del vendedor["produtos"]
        valor = vendedor
    else:   valor = input("valor novo ")
    toUpdate = { "$set": { campo: valor} }
    col.update_one(produto, toUpdate)

def sortProduto():
    global db
    col = db.produtos
    docs = col.find().sort('nome')
    objetos = []
    for obj in docs:
        objetos.append(obj)
    return objetos

def deleteProduto():
    from compras_crud import search
    global db
    col = db.produtos
    produto = search(sortProduto())[int(input("Escolha o produto a deletar: "))]
    query = { "_id": produto["_id"]}
    col.delete_one(query)

# deleteProduto()
# insertProduto()
#updateProduto()

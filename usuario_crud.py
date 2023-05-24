import pymongo
import pickle
client = pymongo.MongoClient("mongodb+srv://programa:o5ma5JcTMMNPbydk@cluster0.ephuxat.mongodb.net/?retryWrites=true&w=majority")
database = client.test
import redis
conR = redis.Redis(host='redis-10721.c261.us-east-1-4.ec2.cloud.redislabs.com',
                  port=10721,
                  password='123senha')


#print(db)

global db
db = client.mercadolivre

def createEndereco():
    rua =  input('Nome da rua: ')
    bairro = input('Nome do bairro: ')
    numero = input('Numero da residencia: ')
    complemento = input('Complemento (opcional): ')
    endereco = {
        "rua": rua,
        "bairro": bairro,
        "numero": numero,
        "complemento": complemento
    }
    return endereco

def updateEndereco(usuario):
    col = db.usuario
    enderecos = usuario["endereço"]
    print('''O que deseja fazer?
    1:  Atualizar endereço
    2:  Adicionar endereço
    3:  Deletar endereço''')
    escolha = input("Escolha uma opção: ")
    if escolha == '1':
        for index in range(len(enderecos)):
            print(str(index) + ':' + str(enderecos[index]))
        enderecoVelho = int(input('Escolha o endereço a atualizar: '))
        enderecoNovo = createEndereco()
        enderecos[enderecoVelho] = enderecoNovo
    elif escolha == '2':
        enderecoNovo = createEndereco()
        enderecos.append(enderecoNovo)
    elif escolha == '3':
        for index in range(len(enderecos)):
            print(str(index) + ':' + str(enderecos[index]))
        enderecos.pop(int(input('Escolha o endereço a deletar: ')))
    query = { "_id": usuario["_id"]}
    toUpdate = {"$set": { "endereço": enderecos}}
    col.update_one(query, toUpdate)



def insertUsuario():
    global db
    col = db.usuario
    nome = input('Nome do usuario: ')
    email = input('Email do usuario: ')
    cpf = input('Cpf do usuario: ')
    enderecos = []
    while True:
        enderecos.append(createEndereco())
        resposta = input('Quer adicionar outro endereço? (y/n) ')
        if resposta == 'n':
            break
    doc = {"nome": nome,
        "email": email,
        "cpf": cpf,
        'endereço': enderecos,
        'favoritos': []
        }
    x = col.insert_one(doc)
    print(x.inserted_id)

def sortUsuario():
    global db
    col = db.usuario
    docs = col.find().sort('nome')
    objetos = []
    for obj in docs:
        objetos.append(obj)
    return objetos

def updateUsuario():
    from compras_crud import search
    global db
    col = db.usuario
    usuarios = search(sortUsuario())
    usuario = usuarios[int(input("Escolha o usuario que deseja editar: "))]
    print('''O que deseja editar? 
    Nome
    Email
    Cpf
    Endereço
    Favoritos''')
    escolha = input("Escreva a sua opção: ").lower()
    if escolha.lower() == "endereço":
        updateEndereco(usuario)
    elif escolha.lower() == "favoritos":
        updateFavorito(usuario)
    else:
        valor = input("valor novo ")
        toUpdate = { "$set": { escolha: valor} }
        query = { "_id": usuario["_id"]}
        col.update_one(query, toUpdate)
    

def deleteUsuario():
    from compras_crud import search
    global db
    col = db.usuario
    usuarios = search(sortUsuario())
    escolha = int(input("usuario a deletar: "))
    usuario = usuarios[escolha]
    conR.set(usuario["email"], pickle.dumps(usuario))
    conR.expire(usuario["email"], 7200)
    query = { "_id": usuario["_id"] }
    col.delete_one(query)

def restaurarUsuario():
    global db
    col = db.usuario
    usuario_res = input("Email do usuario a restaurar: ")
    if conR.exists(usuario_res) > 0:
        usuario = conR.get(usuario_res)
        col.insert_one(pickle.loads(usuario))
    else:
        print("Usuario não existe")


def updateFavorito(usuario):
    from compras_crud import search
    from produto_crud import sortProduto
    global db
    col = db.usuario
    favoritos = usuario["favoritos"]
    print('''O que deseja fazer?
    1:  Adicionar aos favoritos
    2:  Adicionar aos favoritos redis
    3:  Remover dos favoritos''')
    escolha = input('Escolha uma opção: ')
    if escolha == '1':
        produtos = search(sortProduto())
        favoritos.append(produtos[int(input("escolha o produto que quer adicionar: "))])
    elif escolha == '2':
        if conR.exists(usuario["email"]+"-endereco") < 1:
            conR.delete(usuario["email"]+"-endereco")
        produto = search(sortProduto())[int(input("Escolha o produto para adicionar aso favoritos: "))]
        conR.lpush(usuario["email"]+"-endereco", pickle.dumps(produto))
    elif escolha == '3':
        for index in range(len(favoritos)):
            print(str(index) + ':' + str(favoritos[index]))
        favoritos.pop(int(input("Escolha o produto para remover: ")))
    query = { "_id": usuario["_id"]}
    toUpdate = {"$set":{ "favoritos": favoritos}}
    col.update_one(query, toUpdate)

def syincRedisFav():
    from compras_crud import search
    usuarios = search(sortUsuario())
    usuario = usuarios[int(input("Escolha o usuario: "))]
    favoritos = usuario["favoritos"]
    if conR.exists(usuario["email"]+"-favoritos") > 0:
        conR.delete(usuario["email"]+"-favoritos")
    for favorito in favoritos:
        conR.lpush(usuario["email"]+"-favoritos", pickle.dumps(favorito))

def syincMongoFav():
    from compras_crud import search
    global db
    col = db.usuario
    usuarios = search(sortUsuario())
    usuario = usuarios[int(input("Escolha o usuario: "))]
    favoritosMongo = []
    favoritosRedis = conR.lrange(usuario["email"]+"-favoritos", 0, -1)
    for favaorito in favoritosRedis:
        favoritosMongo.append(pickle.loads(favaorito))
    query = { "_id": usuario["_id"]}
    toUpdate = {"$set":{ "favoritos": favoritosMongo}}
    col.update_one(query, toUpdate)


def syncRedisUsuaEnd():
    from compras_crud import search
    usuarios = search(sortUsuario())
    usuario = usuarios[int(input("Escolha o usuario: "))]
    enderecos = usuario["endereço"]
    if conR.exists(usuario["email"]+"-endereco") > 0:
        conR.delete(usuario["email"]+"-endereco")
    for endereco in enderecos:
        conR.lpush(usuario["email"]+"-endereco", pickle.dumps(endereco))

def syncMongoUsuaEnd():
    from compras_crud import search
    global db
    col = db.usuario
    usuarios = search(sortUsuario())
    usuario = usuarios[int(input("Escolha o usuario: "))]
    if conR.exists(usuario["email"]+"-endereco") < 1:
        print("Este usuario não possui favoritos no Redis: ")
    else:
        enderecosMongo = []
        enderecosRedis = conR.lrange(usuario["email"]+"-enderecos", 0, -1)
        for endereco in enderecosRedis:
            enderecosMongo.append(pickle.loads(endereco))
        query = { "_id": usuario["_id"]}
        toUpdate = {"$set":{ "endereço": enderecosMongo}}
        col.update_one(query, toUpdate)

#insertUsuario()
#deleteUsuario()
#restaurarUsuario()
#updateUsuario()
# syincRedisFav()
# for i in conR.lrange("pamonha123@gmail.com-favoritos", 0, -1):
#     print(pickle.loads(i))
#print(conR.exists("pamonha123@gmail.com-favoritos"))
#syincMongoFav()

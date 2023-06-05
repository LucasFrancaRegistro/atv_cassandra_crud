
import pickle
from cassandra_connect import cluster

session = cluster.connect()


def createEndereco(email):
    rua =  input('Nome da rua: ')
    bairro = input('Nome do bairro: ')
    numero = input('Numero da residencia: ')
    complemento = input('Complemento (opcional): ')
    session.execute("INSERT INTO endereco (id, email_residente, rua, bairro, numero, complemento) VALUES (%s, %s, %s, %s, %s, %s)", (uuid.uuid1(), email, rua, bairro, numero, complemento))

def updateEndereco(usuario):

    enderecos = session.execute(" SELECT * FROM endereco WHERE email_residente=%s", (usuario.email))
    print('''O que deseja fazer?
    1:  Atualizar endereço
    2:  Adicionar endereço
    3:  Deletar endereço''')
    escolha = input("Escolha uma opção: ")
    if escolha == '1':
        for index in range(len(enderecos)):
            print(str(index) + ':' + str(enderecos[index]))
        enderecoVelho = int(input('Escolha o endereço a atualizar: '))
        enderecoNovo = createEndereco(usuario.email)
        enderecos[enderecoVelho] = enderecoNovo
    elif escolha == '2':
        createEndereco(usuario.email)   
    elif escolha == '3':
        for index in range(len(enderecos)):
            print(str(index) + ':' + str(enderecos[index]))
        session.execute(" DELETE FROM endereco WHERE id=", (enderecos[index].id))
    




def insertUsuario():
    nome = input('Nome do usuario: ')
    email = input('Email do usuario: ')
    cpf = input('Cpf do usuario: ')
    while True:
        createEndereco(email)
        resposta = input('Quer adicionar outro endereço? (y/n) ')
        if resposta == 'n':
            break
    session.execute(" INSERT INTO usuario (cpf, nome, email) VALUES (%s, %s, %s)", (cpf, nome, email))

def sortUsuario():
    docs = session.execute(" SELECT * FROM usuario")
    usuarios = []
    for obj in docs:
        enderecos, favoritos = [], []
        for endereco in session.execute(" SELECT * FROM endereco WHERE email_residente=%s", (obj.email)):
            enderecos.append(endereco)
        for favorito in session.execute(" SELECT * FROM favoritos WHERE email_usuario=%s", (obj.email)):
            favoritos.append(session.execute(" SELECT * FROM produtos WHERE id_produto=%s", (favorito.id_produto)))
        usuario = {
            usuario: obj
            enderecos: enderecos
            favoritos: favoritos
        }
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
    usuarios = sortUsuario()
    for index in usuarios:
        print(str(index) + ":  " + str(usuarios[index]))
    usuario = usuarios[int(input("Escolha o usuario a deletar: "))]
    session.execute("DELETE FROM usuario WHERE email=s%", (usuario.email))
    session.execute("DELETE FROM endereco WHERE email_residente=s%", (usuario.email))
    session.execute("DELETE FROM favoritos WHERE email_usuario=s%", (usuario.email))



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
        favorito = favoritos[(int(input("Escolha o produto para remover: ")))]
        session.execute("DELETE FROM favoritos WHERE id=s%", (favorito.id))
    query = { "_id": usuario["_id"]}
    toUpdate = {"$set":{ "favoritos": favoritos}}
    col.update_one(query, toUpdate)


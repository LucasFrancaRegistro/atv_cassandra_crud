
import pickle
import uuid
from tabelas import cluster

session = cluster.connect()


def insert_usuario(session, sobrenome, email, nome, endereco):
    id = uuid.uuid4()
    session.execute("INSERT INTO usuarios (id, sobrenome, email, nome, endereco) VALUES (%s,%s,%s,%s,%s)", [id, sobrenome, email, nome, endereco])

def insert_favoritos(session,email,produto):
  id = uuid.uuid4()
  session.execute("INSERT INTO favoritos (id, email, produto) VALUES (%s,%s,%s)", [id, email,produto])

def find_usuarios():
  result = session.execute("SELECT * FROM usuarios")
  return result

def find_favoritos():
  result = session.execute("SELECT * FROM favoritos;")
  return result

def delete_usuario(session, email):
    id_result = session.execute("SELECT id FROM usuarios WHERE email = %s", [email])
    id = id_result.one().id if id_result else None
    if id:
        prepared = session.prepare("DELETE FROM usuarios WHERE id = ?")
        session.execute(prepared, [id])
    else:
        print("Usuário não encontrado.")

def deletar_favorito(session, email):
    nome_result = session.execute("SELECT nome FROM usuarios WHERE email = %s", [email])
    nome = nome_result.one().nome if nome_result else None
    if nome:
        print(f"Cliente: {nome}")
        favoritos = session.execute("SELECT * FROM favoritos WHERE email = %s", [email])
        posicao = 1
        for favorito in favoritos:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [favorito.produto]).one().preco
            nome = favorito.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1
        chave = True
        while chave:
            produtoNome = input("Produto a excluir: ")
            chave = (input("Deseja excluir outro produto? (s/n): ") == 's')
            id_result = session.execute("SELECT id FROM favoritos WHERE email = %s AND produto = %s", [email, produtoNome])
            id = id_result.one().id if id_result else None
            if id:
                prepared = session.prepare("DELETE FROM favoritos WHERE id = ?")
                session.execute(prepared, [id])
            else:
                print("Favorito não encontrada.")
    else:
        print("Usuário não encontrado.")

def adastro_usuario():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    print("Endereços")
    enderecos = []
    adicao = True
    while adicao:
        cep = input("CEP: ")
        numero = input("Número: ")
        enderecos.append({"cep": cep,"numero": numero})
        adicao = (input("Deseja adicionar outro endereço? (s/n): ") == 's')
    insert_usuario(session, sobrenome, email, nome, enderecos)

def pega_usuarios():
    usuarios = find_usuarios()
    for usuario in usuarios:
        print("Nome: " + usuario.nome)
        print("Sobrenome: " + usuario.sobrenome)
        print("Email: " + usuario.email)
        posicao = 1
        if usuario.endereco is not None:
            print("Endereços: ")
            for endereco in usuario.endereco:
                cep = endereco["cep"]
                numero = endereco["numero"]
                print(f"0{posicao} - CEP: {cep}, Número: {numero}")
                posicao += 1
        print("Favoritos: ")
        pega_favoritos(usuario.email)

def pega_favoritos(email):
        posicao = 1
        favoritos = session.execute("SELECT * FROM favoritos WHERE email = %s", [email])
        for favorito in favoritos:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [favorito.produto]).one().preco
            nome = favorito.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1

def atualizar_usuario():
    email = input("Email do usuário a atualizar: ")
    row = session.execute("SELECT id FROM usuarios WHERE email = %s", [email]).one()
    if not row:
        print("Usuário não encontrado.")
        return 
    user_id = row.id
    print("Quais campos deseja atualizar?")
    print("01 - Nome")
    print("02 - Sobrenome")
    print("03 - Email")
    campos = input("Quais campos? (exemplo: 01,02,03): ")
    campos = campos.split(",")
    for campo in campos:
        campo = int(campo)
        if campo == 1:
            nome = input("Novo nome: ")
            session.execute("UPDATE usuarios SET nome = %s WHERE id = %s", [nome, user_id])
        elif campo == 2:
            sobrenome = input("Novo sobrenome: ")
            session.execute("UPDATE usuarios SET sobrenome = %s WHERE id = %s", [sobrenome, user_id])
        elif campo == 3:
            novo_email = input("Novo email: ")
            session.execute("UPDATE usuarios SET email = %s WHERE id = %s", [novo_email, user_id])

def cadastrar_favoritos():
    from compras_crud import cadastrar_itens
    cadastrar_itens("favoritos", "Nome do produto favoritado: ", "Deseja adicionar outro favorito? (s/n): ")

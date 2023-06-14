import uuid
from cassandra_connect import cluster

session = cluster.connect()


def insert_vendedor(session, nome,sobrenome,email):
  id = uuid.uuid4()
  session.execute("INSERT INTO vendedores (id, sobrenome, email, nome) VALUES (%s,%s,%s,%s)", [id, sobrenome, email, nome])

def insert_relacao(session,email,produto):
  id = uuid.uuid4()
  session.execute("INSERT INTO produtos_vendedor (id, email, produto) VALUES (%s,%s,%s)", [id, email,produto])

def find_vendedores():
  result = session.execute("SELECT * FROM vendedores")
  return result

def delete_vendedor(session,email):
    id_result = session.execute("SELECT id FROM vendedores WHERE email = %s", [email])
    id = id_result.one().id if id_result else None
    if id:
        prepared = session.prepare("DELETE FROM vendedores WHERE id = ?")
        session.execute(prepared, [id])
    else:
        print("Vendedor não encontrado.")

def remover_relacao(session, email):
    nome_result = session.execute("SELECT nome FROM vendedores WHERE email = %s", [email])
    nome = nome_result.one().nome if nome_result else None
    if nome:
        print(f"Vendedor: {nome}")
        favoritos = session.execute("SELECT * FROM produtos_vendedor WHERE email = %s", [email])
        posicao = 1
        for favorito in favoritos:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [favorito.produto]).one().preco
            nome = favorito.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1
        chave = True
        while chave:
            produtoNome = input("Produto a remover: ")
            chave = (input("Deseja remover outro produto? (s/n): ") == 's')
            id_result = session.execute("SELECT id FROM produtos_vendedor WHERE email = %s AND produto = %s", [email, produtoNome])
            id = id_result.one().id if id_result else None
            if id:
                prepared = session.prepare("DELETE FROM produtos_vendedor WHERE id = ?")
                session.execute(prepared, [id])
            else:
                print("Relação não encontrada.")
    else:
        print("Vendedor não encontrado.")

def cadastro_vendedor():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    email = input("Email: ")
    insert_vendedor(session, nome, sobrenome, email)

def pega_vendedores():
    vendedores = find_vendedores()
    for vendedor in vendedores:
        print("Nome: " + str(vendedor.nome))
        print("Sobrenome: " + str(vendedor.sobrenome))
        print("Email: " + str(vendedor.email))
        posicao = 1
        produtos = vendedor.produtos
        if produtos is not None:
            print("Vende esses produtos: ")
            for produto in produtos:
                nome = produto.get("nome", "")
                print(f"0{posicao} - Nome do produto: {nome}")
                posicao += 1
        print("Relação com produtos: ")
        pega_relacao(vendedor.email)

def pega_relacao(email):
        posicao = 1
        favoritos = session.execute("SELECT * FROM produtos_vendedor WHERE email = %s", [email])
        for favorito in favoritos:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [favorito.produto]).one().preco
            nome = favorito.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1

def atualizar_vendedor():
    email = input("Email do vendedor a atualizar: ")
    row = session.execute("SELECT id FROM vendedores WHERE email = %s", [email]).one()
    if not row:
        print("Vendedor não encontrado.")
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
            session.execute("UPDATE vendedores SET nome = %s WHERE id = %s", [nome, user_id])
        elif campo == 2:
            sobrenome = input("Novo sobrenome: ")
            session.execute("UPDATE vendedores SET sobrenome = %s WHERE id = %s", [sobrenome, user_id])
        elif campo == 3:
            novo_email = input("Novo email: ")
            session.execute("UPDATE vendedores SET email = %s WHERE id = %s", [novo_email, user_id])


def adicionar_relacao():
    from compras_crud import cadastrar_itens
    cadastrar_itens("relacao", "Nome do produto: ", "Deseja adicionar outro produto? (s/n): ")



import uuid
from cassandra_connect import cluster

session = cluster.connect()


def insert_compras(session,email,produto):
  id = uuid.uuid4()
  session.execute("INSERT INTO compras (id, email, produto) VALUES (%s,%s,%s)", [id, email,produto])

def find_compras():
  result = session.execute("SELECT * FROM compras;")
  return result

def delete_compra(session, email):
    nome_result = session.execute("SELECT nome FROM usuarios WHERE email = %s", [email])
    nome = nome_result.one().nome if nome_result else None
    if nome:
        print(f"Cliente: {nome}")
        compras = session.execute("SELECT * FROM compras WHERE email = %s", [email])
        posicao = 1
        for compra in compras:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [compra.produto]).one().preco
            nome = compra.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            posicao += 1
        chave = True
        while chave:
            produtoNome = input("Produto a excluir: ")
            chave = (input("Deseja excluir outro produto? (s/n): ") == 's')
            id_result = session.execute("SELECT id FROM compras WHERE email = %s AND produto = %s", [email, produtoNome])
            id = id_result.one().id if id_result else None
            if id:
                prepared = session.prepare("DELETE FROM compras WHERE id = ?")
                session.execute(prepared, [id])
                return
            else:
                print("Compra não encontrada.")
    else:
        print("Usuário não encontrado.")

def pega_compras():
    clientes = find_clientes()
    for cliente in clientes:
        print(f'Cliente: {cliente.nome}')
        posicao = 1
        total = 0  
        compras = session.execute("SELECT * FROM compras WHERE email = %s", [cliente.email])
        for compra in compras:
            preco = session.execute("SELECT preco FROM produtos WHERE nome = %s", [compra.produto]).one().preco
            nome = compra.produto
            print(f"0{posicao} - Produto: {nome}, Preço: R${str(preco).replace('.', ',')}")
            total += float(preco.replace(",", "."))
            posicao += 1
    print(f"Total: R${str(total).replace('.', ',')}")

def showCompras(objetos):
    for i in range(len(objetos)):
        print(str(i)+ ': '+
            str({ "data": objetos[i]["data"],
            "usuario": objetos[i]["usuario"]["nome"],
            "vendedor": objetos[i]["vendedor"]["nome"],
            "produto": objetos[i]["produto"]["nome"]}))

def cadastrar_itens(tipo, mensagem, opcao):
    from produto_crud import pega_produtos, find_produtos
    from usuario_crud import insert_favoritos
    from vendedor_crud import insert_relacao
    email = input("Email do usuário: ")
    print('')
    print("Produtos disponíveis:")
    pega_produtos()
    itensNome = []
    chave = True
    while chave:
        itemNome = input(mensagem)
        itensNome.append(itemNome)
        chave = (input(opcao) == 's')
    produtos = find_produtos()
    for produto in produtos:
        for itemNome in itensNome:
            if produto.nome == itemNome:
                if tipo == "compras":
                    insert_compras(session, email, produto.nome)
                elif tipo == "favoritos":
                    insert_favoritos(session, email, produto.nome)
                elif tipo == "relacao":
                    insert_relacao(session, email, produto.nome)

def cadastrar_compras():
    cadastrar_itens("compras", "Nome do produto comprado: ", "Deseja adicionar outra compra? (s/n): ")

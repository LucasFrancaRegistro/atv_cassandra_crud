import uuid
from cassandra_connect import cluster

session = cluster.connect()

def insert_produtos(session,nome,quantia,preco):
  id = uuid.uuid4()
  session.execute("INSERT INTO produtos (id, preco, quantia, nome) VALUES (%s,%s,%s,%s)", [id, preco, quantia, nome])


def find_produtos():
  result = session.execute("SELECT * FROM produtos")
  return result

def delete_produto(session,nome):
    id_result = session.execute("SELECT id FROM produtos WHERE nome = %s", [nome])
    id = id_result.one().id if id_result else None
    if id:
        prepared = session.prepare("DELETE FROM produtos WHERE id = ?")
        session.execute(prepared, [id])
    else:
        print("Produto não encontrado.")

def cadastro_produto():
    nome = input("Nome: ")
    valor  = input("Valor: ")
    quantia = input("Quantia em estoque: ")

def pega_produtos():
    produtos = find_produtos()
    for produto in produtos:
        print("Nome: " + produto.nome)
        print("Preço: " + produto.preco)
        print("Quantia disponível: " + produto.quantia)
        print("")

def atualizar_produto():
    nome = input("Nome do produto a atualizar: ")
    row = session.execute("SELECT id FROM produtos WHERE nome = %s", [nome]).one()
    if not row:
        print("Produto não encontrado.")
        return
    id_prod = row.id
    print("Quais campos deseja atualizar?")
    print("01 - Nome")
    print("02 - Valor")
    print("03 - Quantia")
    campos = input("Quais campos? (exemplo: 01,02,03): ")
    campos = campos.split(",")
    for campo in campos:
        campo = int(campo)
        if campo == 1:
            nome = input("Novo nome: ")
            session.execute("UPDATE produtos SET nome = %s WHERE id = %s", [nome, id_prod])
        elif campo == 2:
            preco = input("Novo valor: ")
            session.execute("UPDATE produtos SET preco = %s WHERE id = %s", [preco, id_prod])
        elif campo == 3:
            quantia = input("Nova quantia: ")
            session.execute("UPDATE produtos SET quantia = %s WHERE id = %s", [quantia, id_prod])

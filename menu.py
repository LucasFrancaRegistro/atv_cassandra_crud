import pymongo
client = pymongo.MongoClient("mongodb+srv://programa:o5ma5JcTMMNPbydk@cluster0.ephuxat.mongodb.net/?retryWrites=true&w=majority")
database = client.test

def main():
    while True:
        print('''Bem vindo ao central de banco de dados do Mercado Livre
        use os numeros para escolher suas opções

        no que deseja interagir?

        1:  Usuarios
        2:  Vendedores
        3:  Produtos
        4:  Compras
        0:  Sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            usuarioCRUD()
        elif escolha == '2':
            vendedorCRUD()
        elif escolha == '3':
            produtoCRUD()
        elif escolha == '4':
            comprasCRUD()
        else:
            break

        
def usuarioCRUD():
    while True:
        print('''O que deseja fazer?
        
        1:  Inserir usuario
        2:  Listar usuarios
        3:  Atualizar usuario
        4:  Deletar usuario
        5:  Restaurar usuario
        6:  Sincronizar favoritos no Redis
        7:  Sincronizar favoritos no Mongo
        8:  Sincronizar endereços no Redis
        9:  Sincronizar endereços no Mongo
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from usuario_crud import insertUsuario
            insertUsuario()
        elif escolha == '2':
            from usuario_crud import sortUsuario
            usuarios = sortUsuario()
            for usuario in usuarios:
                print(str(usuario) + '''
                ''')
        elif escolha == '3':
            from usuario_crud import updateUsuario
            updateUsuario()
        elif escolha == '4':
            from usuario_crud import deleteUsuario
            deleteUsuario()
        elif escolha == "5":
            from usuario_crud import restaurarUsuario
            restaurarUsuario()
        elif escolha == "6":
            from usuario_crud import syincRedisFav
            syincRedisFav()
        elif escolha == "7":
            from usuario_crud import syincMongoFav
            syincMongoFav()
        elif escolha == "8":
            from usuario_crud import syncRedisUsuaEnd
            syncRedisUsuaEnd()
        elif escolha == "8":
            from usuario_crud import syncMongoUsuaEnd
            syncMongoUsuaEnd()
        else:
            break

def vendedorCRUD():
    while True:
        print('''O que deseja fazer?
        
        1:  Inserir vendedor
        2:  Listar vendedores
        3:  Atualizar vendedor
        4:  Deletar vendedor
        5:  Sincronizar endereços no Redis
        6:  Sincronizar endereços no Mongo
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from vendedor_crud import insertVendedor
            insertVendedor()
        elif escolha == '2':
            from vendedor_crud import sortVendedor
            vendedores = sortVendedor()
            for vendedor in vendedores:
                print(str(vendedor) + '''
                ''')
        elif escolha == '3':
            from vendedor_crud import updateVendedor
            updateVendedor()
        elif escolha == '4':
            from vendedor_crud import deleteVendedor
            deleteVendedor()
        elif escolha == '5':
            from vendedor_crud import syncRedisVendEnd
            syncRedisVendEnd()
        elif escolha == '6':
            from vendedor_crud import syncMongoVendEnd
            syncMongoVendEnd()
        else:
            break

def produtoCRUD():
    while True:
        print('''O que deseja fazer?
        
        1:  Inserir produto
        2:  Listar produtos
        3:  Atualizar produto
        4:  Deletar produto
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from produto_crud import insertProduto
            insertProduto()
        elif escolha == '2':
            from produto_crud import sortProduto
            produtos = sortProduto()
            for produto in produtos:
                print(str(produto) + '''
                ''')
        elif escolha == '3':
            from produto_crud import updateProduto
            updateProduto()
        elif escolha == '4':
            from produto_crud import deleteProduto
            deleteProduto()
        else:
            break

def comprasCRUD():
    while True:
        print('''O que deseja fazer?
        
        1:  Inserir compra
        2:  Listar compras
        3:  Atualizar compra
        4:  Deletar compra
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from compras_crud import insertCompra
            insertCompra()
        elif escolha == '2':
            from compras_crud import sortCompras
            compras = sortCompras()
            for compra in compras:
                print(str(compra) + '''
                ''')
        elif escolha == '3':
            from compras_crud import updateCompra
            updateCompra()
        elif escolha == '4':
            from compras_crud import deleteCompra
            deleteCompra()
        else:
            break


main()
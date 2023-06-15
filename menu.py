
from tabelas import cluster

session = cluster.connect()
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
        5:  Adicionar Favoritos
        6:  Remover Favoritos
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from usuario_crud import cadastro_usuario
            cadastro_usuario()
        elif escolha == '2':
            from usuario_crud import pega_usuarios
            pega_usuarios()
        elif escolha == '3':
            from usuario_crud import atualizar_usuario
            atualizar_usuario()
        elif escolha == '4':
            from usuario_crud import delete_usuario
            delete_usuario()
        elif escolha == '5':
            from usuario_crud import cadastrar_favoritos
            cadastrar_favoritos()
        elif escolha == '6':
            from usuario_crud import deletar_favorito
            email = input("Email do usuário relacionado ao favorito: ")
            deletar_favorito(session,email) 
        else:
            break

def vendedorCRUD():
    while True:
        print('''O que deseja fazer?
        
        1:  Inserir vendedor
        2:  Listar vendedores
        3:  Atualizar vendedor
        4:  Deletar vendedor
        5:  Adicionar relação com produto
        6:  Remover relação com produto
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from vendedor_crud import cadastro_vendedor
            cadastro_vendedor()
        elif escolha == '2':
            from vendedor_crud import pega_vendedores
            pega_vendedores()
        elif escolha == '3':
            from vendedor_crud import atualizar_vendedor
            atualizar_vendedor()
        elif escolha == '4':
            from vendedor_crud import delete_vendedor
            email = input("Email do vendedor: ")
            delete_vendedor(session,email)
        elif escolha == '5':
            from vendedor_crud import adicionar_relacao
            adicionar_relacao()
        elif escolha == '6':
            from vendedor_crud import remover_relacao
            email = input("Email do vendedor relacionado ao produto: ")
            remover_relacao(session,email)
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
            from produto_crud import cadastro_produto
            cadastro_produto()
        elif escolha == '2':
            from produto_crud import pega_produtos
            pega_produtos()
        elif escolha == '3':
            from produto_crud import atualizar_produto
            atualizar_produto()
        elif escolha == '4':
            from produto_crud import delete_produto
            nome = input("Nome do produto: ")
            delete_produto(session,nome)
        else:
            break

def comprasCRUD():
    while True:
        print('''O que deseja fazer?
        
        1:  Inserir compra
        2:  Listar compras
        3:  Deletar compra
        0:  sair''')

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            from compras_crud import cadastrar_compras
            cadastrar_compras()
        elif escolha == '2':
            from compras_crud import pega_compras
            pega_compras()
        elif escolha == '3':
            from compras_crud import delete_compra
            email = input("Email do usuário relacionado à compra: ")
            delete_compra(session,email)
        else:
            break


main()
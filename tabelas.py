from cassandra_connect import cluster

def criarTableas():
    session = cluster.connect()
    session.execute("""
            CREATE TABLE IF NOT EXISTS mercado_livre.usuarios (
                id UUID PRIMARY KEY,
                nome text,
                sobrenome text,
                email text,
                endereco list<frozen<map<text, text>>>
            )
        """)

    session.execute("""
            CREATE TABLE IF NOT EXISTS mercado_livre.vendedores (
                id UUID PRIMARY KEY,
                nome text,
                sobrenome text,
                email text,
                produtos list<text>
            )
        """)

    session.execute("""
            CREATE TABLE IF NOT EXISTS mercado_livre.produtos (
                id UUID PRIMARY KEY,
                nome text,
                quantia text,
                preco text
            )
        """)

    session.execute("""
            CREATE TABLE IF NOT EXISTS mercado_livre.compras (
                id UUID PRIMARY KEY,
                email text,
                produto text
            )
        """)

    session.execute("""
            CREATE TABLE IF NOT EXISTS mercado_livre.favoritos (
                id UUID PRIMARY KEY,
                email text,
                produto text
            )
        """)

    session.execute("""
            CREATE TABLE IF NOT EXISTS mercado_livre.produtos_vendedor (
                id UUID PRIMARY KEY,
                email text,
                produto text
            )
        """)

    session.execute("CREATE INDEX IF NOT EXISTS email_usuario ON usuarios (email);")
    session.execute("CREATE INDEX IF NOT EXISTS email_vendedor ON vendedores (email);")
    session.execute("CREATE INDEX IF NOT EXISTS nome_produto ON produtos (nome);")
    session.execute("CREATE INDEX IF NOT EXISTS email_compra ON compras (email);")
    session.execute("CREATE INDEX IF NOT EXISTS produto_compra ON compras (produto);")
    session.execute("CREATE INDEX IF NOT EXISTS email_favorito ON favoritos (email);")
    session.execute("CREATE INDEX IF NOT EXISTS produto_favorito ON favoritos (produto);")
    session.execute("CREATE INDEX IF NOT EXISTS email_prod_vend ON produtos_vendedor (email);")
    session.execute("CREATE INDEX IF NOT EXISTS produto_prod_vend ON produtos_vendedor (produto);")

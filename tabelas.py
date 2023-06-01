from cassandra_connect import cluster

session = cluster.connect()
session.execute(''' 
CREATE TABLE IF NOT EXISTS mercadolivre.usuario (
nome text,
cpf text,
email text,
)
 ''')

session.execute(''' 
CREATE TABLE IF NOT EXISTS mercadolivre.favoritos (
id uuid,
email_usuario text,
id_produto uuid
)
 ''')

session.execute(''' 
CREATE TABLE IF NOT EXISTS mercadolivre.endereco (
rua text,
bairro text,
numero text,
complemento text,
email_residente text
)
 ''')

session.execute(''' 
CREATE TABLE IF NOT EXISTS mercadolivre.vendedor (
nome text,
cpf text,
email text
)
 ''')

session.execute(''' 
CREATE TABLE IF NOT EXISTS mercadolivre.produtos (
id uuid,
nome text,
quantidade int,
preco int,
email_vendedor text,
foto text
)
 ''')

session.execute(''' 
CREATE TABLE IF NOT EXISTS mercadolivre.compras (
id uuid,
data text,
email_usuario,
email_vendedor,
id_produto uuid
)
 ''')
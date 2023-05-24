from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

cloud_config= {
  'secure_connect_bundle': os.getcwd() + '/secure-connect-fatec.zip'
}
auth_provider = PlainTextAuthProvider('GFjvZcBUJAGwiEYkudQteHmr', '60FZlJDcW7_dngTZ9LMJj60mH7x_,QuFRUy1A7jlAF3lTR785xszuyx,o8vzZnBcPTdZIQpeCZYLq-5B18W-i4CbJRRTtUAS-8vYZA_TbzQRfrQQrzHvM6G_XIBU8N_A')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")
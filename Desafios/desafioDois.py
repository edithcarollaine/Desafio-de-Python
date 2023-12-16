import pprint
import pymongo as pyM

# Conexão com mongo atlas
#client = pyM.MongoClient(iNSERIR LINK DO ATLAS AQUI)

# Criando a collecion
db = client.desafio
collection = db.desafio.collection

# Definindo informações para o doc
post = [{
    'Nome': 'Manuel Neves',
    'Cpf': '01234567891',
    'Endereço': 'Jacinto Ramos, bairro colinas',
    'Tipo': 'Pessoa física',
    'Agencia': '0124',
    'Numero': '102013',
    'Saldo': 100.0,
},
    {
    'Nome': 'Marcela Mendes',
    'Cpf': '19876543210',
    'Endereco': 'Passagem São Jorge, bairro matinha',
    'Tipo': 'Pessoa física',
    'Agencia': '0124',
    'Numero': '106113',
    'Saldo': 200.0,
},
    {
    'Nome': 'Ingrid Natalia',
    'Cpf': '11213141516',
    'Endereco': 'Passagem água doce, bairro colinas',
    'Tipo': 'Pessoa física',
    'Agencia': '0124',
    'Numero': '101413',
    'Saldo': 400.0,
}]

# Submetendo as informações
posts = db.posts
result = posts.insert_many(post)
print(result.inserted_ids)

# Mostrando os docs
#for post in posts.find():
#    pprint.pprint(post)

print('\nColeções armazenadas no mongoDB')
collections = (db.list_collection_names())
for collection in collections:
    print(collection)

'''print('\nRemovendo uma collection armazenada no mongoDB e mostrando')
db['posts'].drop()
collections = (db.list_collection_names())  # Removendo a collecions
collections_mostre = (db.list_collection_names())  # Mostrando que a collections foi removida

for collection in collections:
    print(collection)
for collection in collections_mostre:
    print(collection)'''

print('\nMostrando as informações da collection usando find()')
for post in posts.find():
    pprint.pprint(post)

print('\nRecuperação a partir da chave valor')
pprint.pprint(db.posts.find_one({'Nome': 'Manuel Neves'}))

# Contagem de documentos
print('\nQuantidade de documentos')
print(posts.count_documents({}))

# Para deletar todos os documentos
#print(posts.delete_many({}))

client.drop_database('desafio')

print(db.list_collection_names())

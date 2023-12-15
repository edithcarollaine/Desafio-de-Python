from sqlalchemy import Column, func
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship


Base = declarative_base()  # Mapear qual tabela no BD será relacionada com cada classe.


class Cliente(Base):
    __tablename__ = 'client_account'  # first table

    # atributos

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(11), nullable=False)
    endereco = Column(String(50), nullable=False)

    conta = relationship(
        'Conta', back_populates='cliente', cascade='all, delete-orphan',
    )

    def __repr__(self):
        return (f'Cliente(Id = {self.id},'
                f' Nome = {self.nome}, CPF = {self.cpf}, Endereço = {self.endereco})')


class Conta(Base):
    __tablename__ = 'conta'  # second table

    # atributos

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    numero = Column(Integer)
    id_cliente = Column(Integer, ForeignKey('client_account.id'), nullable=False)
    saldo = Column(Float)

    cliente = relationship('Cliente', back_populates='conta')

    def __repr__(self):
        return (f'Conta(Id = {self.id}, Tipo = {self.tipo}, Agẽncia = {self.agencia}, '
                f' Numero = {self.numero}, Saldo = {self.saldo})')


engine = create_engine('sqlite://')
Base.metadata.create_all(engine)  # Criando as classes como tabela no banco de dados  # Iniciando a conexão com o Banco de dados

inspetor_engine = inspect(engine)
print('Verificando se as tabelas foram criadas')
print(inspetor_engine.get_table_names())


'''
Inserção de informações dentro das tabelas já criadas 
'''

with Session(engine) as session:
    cliente_um = Cliente(
        nome='Manuel Neves',
        cpf='01234567891',
        endereco='Jacinto Ramos, bairro colinas',
        conta=[Conta(tipo='Pessoa física', agencia='0124', numero='102013', saldo=500.0)]
    )
    cliente_dois = Cliente(
        nome='Marcela Mendes',
        cpf='19876543210',
        endereco='Passagem São Jorge, bairro colinas',
        conta=[Conta(tipo='Pessoa física', agencia='0124', numero='106113', saldo=200.0)]
    )
    cliente_tres = Cliente(
        nome='Ingrid Natalia',
        cpf='11213141516',
        endereco='Passagem água doce, bairro colinas',
        conta=[Conta(tipo='Pessoa física', agencia='0124', numero='101413', saldo=100.0)],
    )

    session.add_all([cliente_um, cliente_dois, cliente_tres])
    session.commit()

'''
Recuperação de informações do banco de dados com técnicas diferentes
'''

print('\nRecuperando usuários a partir de condição com select')
recuperar = select(Cliente).where(Cliente.nome.in_(['Ingrid Natalia', 'Marcela Mendes']))
for cliente in session.scalars(recuperar):
    print(cliente)

print('\nRecuperando informação a partir do id com select')
recuperar_endereco = select(Conta).where(Conta.id_cliente.in_([2]))
for result in session.scalars(recuperar_endereco):
    print(result)


print('\nRecuperando todas as informações do Cliente com select')
recuperar_order = (select(Cliente).order_by(Cliente.id.desc()))
for result in session.scalars(recuperar_order):
    print(result)

print('\nRecuperando todas as informações da Conta com o query')
recuperar = session.query(Conta).all()
for result in recuperar:
    print(result)

print('\nRecuperando todas as informações do Cliente com o query')
recuperar = session.query(Cliente).all()
for result in recuperar:
    print(result)

'''
Outra opção para conexão da engine
'''
print('\nMostrando resultados de cliente e conta com engine.connect')
conectar = engine.connect()
recuperar_join = select(Cliente.nome, Cliente.endereco, Conta.tipo, Conta.saldo).join_from(Conta, Cliente)
result = conectar.execute(recuperar_join).fetchall()

for result_last in result:
    print(result_last)

print('\nResultado de instâncias em Cliente e conta')
recuperar_count = select(func.count('*')).select_from(Cliente)
recuperar_count_two = select(func.count('*')).select_from(Conta)

for result in session.scalars(recuperar_count):
    print(result)
for result in session.scalars(recuperar_count_two):
    print(result)

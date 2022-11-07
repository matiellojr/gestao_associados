from flask import Flask
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy

class AssociadosModel(db.Model):

    __tablename__ = 'associados'
    id = sa.Column(sa.Integer, primary_key = True)
    data_cadastro = sa.Column(sa.Date)
    data_atualizada = sa.Column(sa.Date)
    cpf = sa.Column(sa.String(15))
    nome_completo = sa.Column(sa.String(200))
    endereco = sa.Column(sa.String(200))
    cidade = sa.Column(sa.String(200))
    uf = sa.Column(sa.String(2))
    email = sa.Column(sa.String(200))
    data_nascimento = sa.Column(sa.Date)
    telefone = sa.Column(sa.String(30))
    estado_civil = sa.Column(sa.String(50))
    como_identifica = sa.Column(sa.String())
    situacao_trabalho = sa.Column(sa.String(50))
    tipo_sanguineo = sa.Column(sa.String(3))
    quantidades_filhos = sa.Column(sa.Integer)
    status_associado = sa.Column(sa.Boolean)

    def __init__(self, id, cpf, nome_completo, endereco, data_cadastro, cidade, uf,  email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, situacao_trabalho, como_identifica, quantidades_filhos, status_associado):
        self.id = id
        self.data_cadastro = data_cadastro
        self.data_atualizada = data_atualizada
        self.cpf = cpf
        self.nome_completo = nome_completo
        self.endereco = endereco
        self.cidade = cidade
        self.uf = uf
        self.email = email
        self.tipo_sanguineo = tipo_sanguineo
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.estado_civil = estado_civil
        self.situacao_trabalho = situacao_trabalho
        self.como_identifica = como_identifica
        self.quantidades_filhos = quantidades_filhos
        self.status_associado = status_associado


class tipos_sanguineo(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    tipos = sa.Column(sa.String(3))

    def __init__(self, tipos):
        self.tipos = tipos

class identificacao(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    tipo = sa.Column(sa.String(30))

    def __init__(self, tipo):
        self.tipo = tipo

class estado_civil(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    tipo = sa.Column(sa.String(30))

    def __init__(self, tipo):
        self.tipo = tipo

class status_mensalidade(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    situacao = sa.Column(sa.String(50))

    def __init__(self, situacao):
        self.situacao = situacao
    

def execute_insert():
    # busca uma linha > tem_tipos_sanguineos.fetchone()
    # busca todas as linhas > tem_tipos_sanguineos.fetchall() 
    # busca todas as linhas, cada linha tem um dicionário com os nomes dos campos > tem_tipos_sanguineos.dictfetchall() 
    tem_tipos_sanguineos = db.engine.execute('SELECT 1 FROM tipos_sanguineo;')
    tem_identificacao = db.engine.execute('SELECT 1 FROM identificacao;')
    tem_estado_civil = db.engine.execute('SELECT 1 FROM ESTADO_CIVIL;')
    # tem_status_mensalidade = db.engine.execute('SELECT 1 FROM STATUS_MENSALIDADE;')
    
    if not(tem_tipos_sanguineos.fetchone()):
        db.engine.execute('''
            INSERT INTO tipos_sanguineo VALUES (1, 'A+');
            INSERT INTO tipos_sanguineo VALUES (2, 'B+');
            INSERT INTO tipos_sanguineo VALUES (3, 'AB+');
            INSERT INTO tipos_sanguineo VALUES (4, 'O+');
            INSERT INTO tipos_sanguineo VALUES (5, 'A-');
            INSERT INTO tipos_sanguineo VALUES (6, 'B-');
            INSERT INTO tipos_sanguineo VALUES (7, 'AB-');
            INSERT INTO tipos_sanguineo VALUES (8, 'O-');
        ''')
    else:
        print('Os dados da tabela do Tipo de Sanguíneos já está inserido!')

    if not(tem_identificacao.fetchone()):
        db.engine.execute('''
            INSERT INTO IDENTIFICACAO VALUES (1, 'Surdo');
            INSERT INTO IDENTIFICACAO VALUES (2, 'Surdocego');
            INSERT INTO IDENTIFICACAO VALUES (3, 'Deficiência Auditiva (DA)');
            INSERT INTO IDENTIFICACAO VALUES (4, 'Ouvinte');
        ''')
    else:
        print('Os dados da tabela do Identificação já está inserido!')

    if not(tem_estado_civil.fetchone()):
        db.engine.execute('''
            INSERT INTO ESTADO_CIVIL VALUES (1, 'Solteiro');
            INSERT INTO ESTADO_CIVIL VALUES (2, 'Casado');
            INSERT INTO ESTADO_CIVIL VALUES (3, 'Separado');
            INSERT INTO ESTADO_CIVIL VALUES (4, 'Divorciado');
            INSERT INTO ESTADO_CIVIL VALUES (5, 'Viúvo');
        ''')
    else:
        print('Os dados da tabela do Estado Civil já está inserido!')

    # if not(tem_status_mensalidade.fetchone()):
    #     db.engine.execute('''
    #         INSERT INTO status_mensalidade VALUES (1, 'Aguardando pagamento!');
    #         INSERT INTO status_mensalidade VALUES (2, 'Aguardando a aprovação!');
    #         INSERT INTO status_mensalidade VALUES (3, 'Pago!');
    #         INSERT INTO status_mensalidade VALUES (4, 'Atrasado!');
    #         INSERT INTO status_mensalidade VALUES (5, 'Não está apto para votar, 6 meses sem pagamento.');
    #     ''')
    # else:
    #     print('Os dados da tabela do Status de Mensalidade já está inserido!')

from ctypes.wintypes import PINT
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import sqlalchemy as sa
import enum
from datetime import date
from functions import validacao_cpf
import psycopg2


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviestest.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:admin@localhost/aulapython"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class associados(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    data_cadastro = sa.Column(sa.Date)
    data_atualizada = sa.Column(sa.Date)
    cpf = sa.Column(sa.String(15))
    nome_completo = sa.Column(sa.String(200))
    endereco = sa.Column(sa.String(200))
    cidade = sa.Column(sa.String(200))
    uf = sa.Column(sa.String(2))
    email = sa.Column(sa.String(100))
    data_nascimento = sa.Column(sa.Date)
    telefone = sa.Column(sa.String(15))
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


@app.route('/')
def page_principal():
    return render_template("index.html")




@app.route('/associado_lista')
def page_associado_lista():
    query_lista = db.engine.execute("SELECT * FROM associados ORDER BY ID;")
    return render_template("associado/associado_lista.html", lista_associados = query_lista)



@app.route('/associado_form' , methods=["GET", "POST"])
def page_associado_form():
    query_tipos_sanguineos = db.engine.execute("SELECT TIPOS FROM TIPOS_SANGUINEO;")
    query_identificacao = db.engine.execute('SELECT TIPO FROM IDENTIFICACAO;')
    query_estado_civil = db.engine.execute('SELECT TIPO FROM ESTADO_CIVIL;')
    query_quantidade_associados = db.engine.execute(f"SELECT COUNT(*) FROM ASSOCIADOS;")

    data_atualizada = request.form.get('data_atualizada')
    data_cadastro = request.form.get('data_cadastro')
    cpf = request.form.get('cpf')
    nome_completo = request.form.get('nome_completo')
    endereco = request.form.get('endereco')
    email = request.form.get('email')
    cidade = request.form.get('cidade')
    uf = request.form.get('uf')
    tipo_sanguineo = request.form.get('tipo_sanguineo')
    data_nascimento = request.form.get('data_nascimento')
    telefone = request.form.get('telefone')
    estado_civil = request.form.get('estado_civil')
    situacao_trabalho = request.form.get('situacao_trabalho')
    como_identifica = request.form.get('como_identifica')
    quantidades_filhos = request.form.get('quantidades_filhos')

    if (request.method == 'POST'):
        if not(validacao_cpf.Cpf.validate(request.form.get('cpf'))):
            cpf_error = request.form.get('cpf')
            flash(f"Favor prencher no campo CPF, que está incorreto: {cpf_error}!", "error")
        else:
            get_id = query_quantidade_associados.fetchone()
            get_last_id = get_id[0] + 1
            associado = associados(get_last_id, cpf, nome_completo, endereco, data_cadastro, cidade, uf, email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, situacao_trabalho, como_identifica, quantidades_filhos, False)
            table_login = login(get_last_id, '', '')
            db.session.add(associado)
            db.session.add(table_login)
            db.session.commit()
            return redirect(url_for('page_associado_lista'))

    return render_template("associado/associado_form.html", tipos = query_tipos_sanguineos,  identificacao = query_identificacao, estado_civil = query_estado_civil, data_hoje=date.today())



@app.route('/<int:id>/associado_atualiza' , methods=["GET", "POST"])
def page_associado_atualiza(id):
    query_associados = db.engine.execute(f"SELECT * FROM ASSOCIADOS WHERE ID = {id} ORDER BY ID;")

    if (request.method == 'POST'):
        if not(validacao_cpf.Cpf.validate(request.form['cpf'])):
            cpf_error = request.form['cpf']
            flash(f"O CPF está incorreto: {cpf_error}!", "error")
        else:
            data_atualizada = date.today()
            data_cadastro = request.form['data_cadastro']
            cpf = request.form['cpf']
            nome_completo = request.form['nome_completo']
            endereco = request.form['endereco']
            email = request.form['email']
            cidade = request.form['cidade']
            uf = request.form['uf']
            tipo_sanguineo = request.form['tipo_sanguineo']
            data_nascimento = request.form['data_nascimento']
            telefone = request.form['telefone']
            estado_civil = request.form['estado_civil']
            situacao_trabalho = request.form['situacao_trabalho']
            como_identifica = request.form['como_identifica']
            quantidades_filhos = request.form['quantidades_filhos']
            # tem_filhos = request.form['switch_filhos']
            # https://www.youtube.com/watch?v=_sgVt16Q4O4

            if (request.form.get('status_associado')):
                status_associado = True
            else:
                status_associado = False

            db.engine.execute(
                f"""
                    UPDATE ASSOCIADOS SET DATA_CADASTRO='{data_cadastro}', DATA_ATUALIZADA='{data_atualizada}', CPF='{cpf}', NOME_COMPLETO='{nome_completo}', ENDERECO='{endereco}', CIDADE='{cidade}', UF='{uf}', EMAIL='{email}', DATA_NASCIMENTO='{data_nascimento}', TELEFONE='{telefone}', ESTADO_CIVIL='{estado_civil}', como_identifica='{como_identifica}', SITUACAO_TRABALHO='{situacao_trabalho}', TIPO_SANGUINEO='{tipo_sanguineo}', QUANTIDADES_FILHOS={quantidades_filhos}, STATUS_ASSOCIADO={status_associado} WHERE ID={id};
                """)
            db.session.commit()
            return redirect(url_for('page_associado_lista'))

    return render_template("associado/associado_atualiza.html", _query_associados = query_associados)


# --------------------------------------------
# Financeiro
# --------------------------------------------
# https://lala-rustamli.medium.com/casting-populated-table-column-to-enum-in-flask-with-sqlalchemy-f44fe404d9ae
# class TipoMensalidade(enum.Enum):
#     MENSAL = 'Mensal'
#     ANUAL  = 'Anual'

# class StatusMensalidade(enum.Enum):
#     status1 = 'Ainda falta pagar!'
#     status2 = 'Pago!'
#     status3 = 'Atrasado!'

# class mensalidade(db.Model):
#     id = sa.Column(sa.Integer, primary_key = True)
#     tipo_mensalidade = sa.Column(sa.Enum(TipoMensalidade))
#     data_pagamento = sa.Column(sa.Date)
#     data_vencimento = sa.Column(sa.Date)
#     valor_mensalidade = sa.Column(sa.Float)
#     pagamento_confirmado = sa.Column(sa.Boolean)
#     status_mensalidade = sa.Column(sa.Enum(StatusMensalidade))
#     id_pagamento = relationship("pagamento", back_populates="mensalidade")

#     def __init__(self, tipo_mensalidade, data_pagamento, data_vencimento,valor_mensalidade, pagamento_confirmado, status_mensalidade, id_pagamento):
#         self.tipo_mensalidade = tipo_mensalidade
#         self.data_pagamento = data_pagamento
#         self.data_vencimento = data_vencimento
#         self.valor_mensalidade = valor_mensalidade
#         self.pagamento_confirmado = pagamento_confirmado
#         self.status_mensalidade = status_mensalidade
#         self.id_pagamento = id_pagamento


# class pagamento(db.Model):
#     id = sa.Column(sa.Integer, primary_key = True)
#     data_pagamento = sa.Column(sa.Date)
#     valor_pagamento = sa.Column(sa.Float)
#     comprovante_pagamento = sa.Column(sa.String)
#     mensalidade_id = sa.Column(sa.Integer, sa.ForeignKey("mensalidade.id"))

#     def __init__(self, data_pagamento, valor_pagamento, comprovante_pagamento, mensalidade_id):
#         self.data_pagamento = data_pagamento
#         self.valor_pagamento = valor_pagamento
#         self.comprovante_pagamento = comprovante_pagamento
#         self.mensalidade_id = mensalidade_id


@app.route('/financeiro_form' , methods=["GET", "POST"])
def page_financeiro_form():
    return render_template("financeiro/financeiro_form.html")


# --------------------------------------------------------------
#  Login
# --------------------------------------------------------------
class login(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    cpf_login = sa.Column(sa.String(15))
    password_login = sa.Column(sa.String(10))

    def __init__(self, id, cpf_login, password_login):
        self.id = id
        self.cpf_login = cpf_login
        self.password_login = password_login
        

@app.route('/login')
def page_login_access():
    
    # query_login = db.engine.execute(f"SELECT COUNT(*) FROM LOGIN;")
    return render_template("login/login_access.html")

@app.route('/login_form', methods=["GET", "POST"])
def page_login_form():
    query_tipos_sanguineos = db.engine.execute("SELECT TIPOS FROM TIPOS_SANGUINEO;")
    query_identificacao = db.engine.execute('SELECT TIPO FROM IDENTIFICACAO;')
    query_estado_civil = db.engine.execute('SELECT TIPO FROM ESTADO_CIVIL;')
    query_quantidade_associados = db.engine.execute(f"SELECT COUNT(*) FROM ASSOCIADOS;")

    cpf_login = request.form.get('cpf')
    password_login = request.form.get('password_login')

    cpf = request.form.get('cpf')
    data_atualizada = request.form.get('data_atualizada')
    data_cadastro = request.form.get('data_cadastro')
    nome_completo = request.form.get('nome_completo')
    endereco = request.form.get('endereco')
    email = request.form.get('email')
    cidade = request.form.get('cidade')
    uf = request.form.get('uf')
    tipo_sanguineo = request.form.get('tipo_sanguineo')
    data_nascimento = request.form.get('data_nascimento')
    telefone = request.form.get('telefone')
    estado_civil = request.form.get('estado_civil')
    situacao_trabalho = request.form.get('situacao_trabalho')
    como_identifica = request.form.get('como_identifica')
    quantidades_filhos = request.form.get('quantidades_filhos')
    

    if (request.method == 'POST'):
        if not(validacao_cpf.Cpf.validate(request.form.get('cpf'))):
            cpf_error = request.form.get('cpf')
            flash(f"Favor prencher no campo CPF, que está incorreto: {cpf_error}, deixar assim, 36377907931!", "error")
        elif (len(password_login) <= 0) and (len(password_login) <= 6) and (len(password_login) > 10):
            flash(f"Favor prencher a Senha de 5 a 10 caracteres!", "error")
        else:
            get_id = query_quantidade_associados.fetchone()
            get_last_id = get_id[0] + 1
            associado = associados(get_last_id, cpf, nome_completo, endereco, data_cadastro, cidade, uf, email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, situacao_trabalho, como_identifica, quantidades_filhos, False)
            table_login = login(get_last_id, cpf_login, password_login)
            db.session.add(associado)
            db.session.add(table_login)
            db.session.commit()
            return redirect(url_for('page_login_access'))

    return render_template("login/login_form.html", tipos = query_tipos_sanguineos,  identificacao = query_identificacao, estado_civil = query_estado_civil, data_hoje=date.today())


@app.route('/login_forgot_password', methods=["GET", "POST"])
def page_login_forgot_password():

    if (request.method == 'POST'):
        query = db.engine.execute(f"SELECT A.CPF, L.PASSWORD_LOGIN FROM ASSOCIADOS A INNER JOIN LOGIN L ON (L.ID = A.ID) WHERE A.CPF = '{request.form['cpf_login']}';")
        if not(query.fetchone()):
            print("não foi encontrado registro na tabela!")
        get_CPF = query.fetchone()
        print(get_CPF[0])
        if not(validacao_cpf.Cpf.validate(request.form['cpf_login'])):
            cpf_error = request.form['cpf_login']
            flash(f"O CPF está incorreto: {cpf_error}!", "error")

        # else:
        #     db.engine.execute(
        #         f"""
        #             UPDATE LOGIN SET PASSWORD_LOGIN = {}
        #         """)


        # if not(validacao_cpf.Cpf.validate(request.form.get('cpf_login'))):
        #     cpf_error = request.form.get('cpf_login')
        #     flash(f"Favor prencher no campo CPF, que está incorreto: {cpf_error}, deixar assim, 36377907931!", "error")
        
        # get_CPF = query_CPF.fetchone()
        # flash(f"Favor prencher a Senha de 5 a 10 caracteres!", "error")


    return render_template("login/login_forgot_password.html")
    
    
    
# --------------------------------------------------------------

if __name__ == "__main__":
    app.secret_key = "\x10)\xd8\x1a]J\x93z,\x1f)\x0b(w\\\xa7G\xbeQ\xa9\x10\xf7\x94T"

    with app.app_context():
        db.create_all()
        execute_insert()
        print(" [*** BANCO DE DADOS ATIVADO! ***]")
    app.run(debug=True)
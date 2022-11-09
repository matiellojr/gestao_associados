from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
# https://github.com/Sidon/py-ufbr
from pyUFbr.baseuf import ufbr
import sqlalchemy as sa
from datetime import date
from functions import validacao_cpf
import psycopg2


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviestest.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:admin@localhost/gestao_associados_asblu"
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

class status_pagamento(db.Model):
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
    tem_status_pagamento = db.engine.execute('SELECT 1 FROM STATUS_PAGAMENTO;')
    
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

    if not(tem_status_pagamento.fetchone()):
        db.engine.execute('''
            INSERT INTO status_pagamento VALUES (1, 'Aguardando pagamento!');
            INSERT INTO status_pagamento VALUES (2, 'Aguardando a aprovação!');
            INSERT INTO status_pagamento VALUES (3, 'Pago!');
            INSERT INTO status_pagamento VALUES (4, 'Atrasado!');
            INSERT INTO status_pagamento VALUES (5, 'Não está apto para votar, 6 meses sem pagamento.');
        ''')
    else:
        print('Os dados da tabela do Status de Pagamento já está inserido!')


@app.route('/')
def page_principal():
    return render_template("index.html")




@app.route('/associado_lista')
def page_associado_lista():
    query_lista = db.engine.execute("SELECT * FROM associados ORDER BY ID;")
    return render_template("associado/associado_lista.html", lista_associados = query_lista)



# @app.route('/associado_form' , methods=["GET", "POST"])
# def page_associado_form():
#     query_tipos_sanguineos = db.engine.execute("SELECT TIPOS FROM TIPOS_SANGUINEO;")
#     query_identificacao = db.engine.execute('SELECT TIPO FROM IDENTIFICACAO;')
#     query_estado_civil = db.engine.execute('SELECT TIPO FROM ESTADO_CIVIL;')
#     query_quantidade_associados = db.engine.execute(f"SELECT COUNT(*) FROM ASSOCIADOS;")

#     data_atualizada = request.form.get('data_atualizada')
#     data_cadastro = request.form.get('data_cadastro')
#     cpf = request.form.get('cpf')
#     nome_completo = request.form.get('nome_completo')
#     endereco = request.form.get('endereco')
#     email = request.form.get('email')
#     cidade = request.form.get('cidade')
#     uf = request.form.get('uf')
#     tipo_sanguineo = request.form.get('tipo_sanguineo')
#     data_nascimento = request.form.get('data_nascimento')
#     telefone = request.form.get('telefone')
#     estado_civil = request.form.get('estado_civil')
#     situacao_trabalho = request.form.get('situacao_trabalho')
#     como_identifica = request.form.get('como_identifica')
#     quantidades_filhos = request.form.get('quantidades_filhos')

#     if (request.method == 'POST'):
#         # if not(validacao_cpf.Cpf.validate(request.form.get('cpf'))):
#         #     cpf_error = request.form.get('cpf')
#         #     flash(f"Favor prencher no campo CPF, que está incorreto: {cpf_error}!", "error")
#         # else:
#             get_id = query_quantidade_associados.fetchone()
#             get_last_id = get_id[0] + 1
#             associado = associados(get_last_id, cpf, nome_completo, endereco, data_cadastro, cidade, uf, email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, situacao_trabalho, como_identifica, quantidades_filhos, False)
#             table_login = login(get_last_id, '', '')
#             db.session.add(associado)
#             db.session.add(table_login)
#             db.session.commit()
#             return redirect(url_for('page_associado_lista'))

#     return render_template("associado/associado_form.html", tipos = query_tipos_sanguineos,  identificacao = query_identificacao, estado_civil = query_estado_civil)



@app.route('/<int:id>/associado_atualiza' , methods=["GET", "POST"])
def page_associado_atualiza(id):
    query_tipos_sanguineos = db.engine.execute("SELECT TIPOS FROM TIPOS_SANGUINEO;")
    query_estado_civil = db.engine.execute('SELECT TIPO FROM ESTADO_CIVIL;')
    query_associados = db.engine.execute(f"SELECT * FROM ASSOCIADOS WHERE ID = {id} ORDER BY ID;")
    query_identificacao = db.engine.execute('SELECT TIPO FROM IDENTIFICACAO;')


    # se clicar no botão Atualizar, no form associado_atualiza
    if (request.method == 'POST'):
        cpf_without_mask = validacao_cpf.Cpf.retirapontoshifen(request.form['cpf'])
        if not(validacao_cpf.Cpf.validate(cpf_without_mask)):
            cpf_error = request.form['cpf']
            flash(f"O CPF está incorreto: {cpf_error}!", "error")
        else:
            data_atualizada = date.today()
            data_cadastro = request.form['data_cadastro']
            cpf = cpf_without_mask
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

    return render_template("associado/associado_atualiza.html", _query_associados = query_associados, identificacao = query_identificacao, tipos_sanguineos = query_tipos_sanguineos, estado_civil = query_estado_civil, unidade_federativa = ufbr.list_uf, cidades_sc = ufbr.list_cidades(sigla='SC'), cidades_pr = ufbr.list_cidades(sigla='PR'), cidades_rs = ufbr.list_cidades(sigla='RS'))


# --------------------------------------------
# Financeiro
# --------------------------------------------
# https://lala-rustamli.medium.com/casting-populated-table-column-to-enum-in-flask-with-sqlalchemy-f44fe404d9ae

class mensalidade(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    ehMensal = sa.Column(sa.Boolean)
    data_pagamento = sa.Column(sa.Date)
    data_vencimento = sa.Column(sa.Date)
    valor_mensalidade = sa.Column(sa.Float)
    # id_pagamento = relationship("pagamento", back_populates="mensalidade", lazy = True)

    def __init__(self, id, ehMensal, data_pagamento, data_vencimento, valor_mensalidade):
        self.id = id
        self.ehMensal = ehMensal
        self.data_pagamento = data_pagamento
        self.data_vencimento = data_vencimento
        self.valor_mensalidade = valor_mensalidade


class pagamento(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    data_pagamento = sa.Column(sa.Date)
    valor_pagamento = sa.Column(sa.Float)
    comprovante_pagamento = sa.Column(sa.String)
    status_pagamento = sa.Column(sa.String)
    pagamento_confirmado = sa.Column(sa.Boolean)
    # mensalidade_id = sa.Column(sa.Integer, sa.ForeignKey("mensalidade.id"))

    def __init__(self, data_pagamento, valor_pagamento, status_pagamento, pagamento_confirmado, comprovante_pagamento):
        self.data_pagamento = data_pagamento
        self.valor_pagamento = valor_pagamento
        self.status_pagamento = status_pagamento
        self.pagamento_confirmado = pagamento_confirmado
        self.comprovante_pagamento = comprovante_pagamento
        # self.mensalidade_id = mensalidade_id


@app.route('/mensalidade_form' , methods=["GET", "POST"])
def page_mensalidade_form():
    query_mensalidade = db.engine.execute("SELECT * FROM MENSALIDADE;")
    query_count_mensalidade = db.engine.execute("SELECT COUNT(*) FROM MENSALIDADE;")

    isMensal = bool(True)
    data_pagamento = request.form.get('data_pagamento')
    data_vencimento = request.form.get('data_vencimento')
    valor_mensalidade = request.form.get('valor_mensalidade')
    mensalidade_mensal = request.form.get('tipo_mensalidade')

    if (request.method == 'POST'):
        get_id = query_count_mensalidade.fetchone()
        get_last_id = get_id[0] + 1
        # print(f'>>> POST MENSAL >> {mensal}')
        print(f'>>> POST TIPO   >> {mensalidade_mensal}')
        
        if (mensalidade_mensal == True):
            ehMensal = True
        else:
            ehMensal = False

        get_mensalidade = mensalidade(get_last_id, ehMensal, data_pagamento, data_vencimento, valor_mensalidade)
        db.session.add(get_mensalidade)
        db.session.commit()
        flash(f"Mensalidade cadastrada!", "success")
        return redirect(url_for('page_mensalidade_form'))

    return render_template("financeiro/mensalidade/mensalidade_form.html", mensalidade = query_mensalidade, ehMensal = isMensal)


# --------------------------------------------------------------
#  Login
# --------------------------------------------------------------
class login(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    cpf_login = sa.Column(sa.String(30))
    password_login = sa.Column(sa.String())

    def __init__(self, id, cpf_login, password_login):
        self.id = id
        self.cpf_login = cpf_login
        self.password_login = password_login
        

@app.route('/login_access')
def page_login_access():
    # query_login = db.engine.execute(f"SELECT COUNT(*) FROM LOGIN;")
    return render_template("login/login_access.html")

@app.route('/login_form', methods=["GET", "POST"])
def page_login_form():
    query_tipos_sanguineos = db.engine.execute("SELECT TIPOS FROM TIPOS_SANGUINEO;")
    query_identificacao = db.engine.execute('SELECT TIPO FROM IDENTIFICACAO;')
    query_estado_civil = db.engine.execute('SELECT TIPO FROM ESTADO_CIVIL;')
    query_quantidade_associados = db.engine.execute("SELECT COUNT(*) FROM ASSOCIADOS;")

    cpf_login = request.form.get('cpf')
    password_login = request.form.get('password_login')

    cpf = request.form.get('cpf')
    data_atualizada = request.form.get('data_atualizada')
    data_cadastro = request.form.get('data_cadastro')
    nome_completo = request.form.get('nome_completo')
    endereco = request.form.get('endereco')
    email = request.form.get('email')
    uf = request.form.get('uf')
    cidade = request.form.get('cidade')
    tipo_sanguineo = request.form.get('tipo_sanguineo')
    data_nascimento = request.form.get('data_nascimento')
    telefone = request.form.get('telefone')
    estado_civil = request.form.get('estado_civil')
    situacao_trabalho = request.form.get('situacao_trabalho')
    como_identifica = request.form.get('como_identifica')
    quantidades_filhos = request.form.get('quantidades_filhos')
    
    # quando clicar no botão "Atualizar", no assosciado_atualiza
    if (request.method == 'POST'):
        cpf_without_mask = validacao_cpf.Cpf.retirapontoshifen(cpf)
        print(cpf_without_mask)
        query_cpf = db.engine.execute(f"SELECT CPF FROM ASSOCIADOS WHERE CPF = '{cpf_without_mask}';")
        # get_status = query_cpf.fetchone()
        # print(get_status[0])

        if (query_cpf.fetchone()):
            query_status = db.engine.execute(f"SELECT STATUS_ASSOCIADO FROM ASSOCIADOS WHERE CPF = '{cpf_without_mask}';")
            get_status = query_status.fetchone()

            encontrou_cpf = f"Foi encontrado o CPF {request.form.get('cpf')} no sistema"

            if not(get_status[0]):
                flash(f'{encontrou_cpf}, mas a conta está desativada. Se deseja ativar, falar com a diretoria.')
            else:
                flash(f'{encontrou_cpf}.')
        elif not(validacao_cpf.Cpf.validate(cpf_without_mask)):
            flash(f"Favor prencher o campo CPF, está incorreto: {cpf_login}!", "error")
        else:
            get_id = query_quantidade_associados.fetchone()
            get_last_id = get_id[0] + 1
            associado = associados(get_last_id, cpf_without_mask, nome_completo, endereco, data_cadastro, cidade, uf, email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, situacao_trabalho, como_identifica, quantidades_filhos, False)
            table_login = login(get_last_id, cpf_without_mask, password_login)
            db.session.add(associado)
            db.session.add(table_login)
            db.session.commit()
            return redirect(url_for('page_login_access'))

    return render_template("login/login_form.html", tipos = query_tipos_sanguineos, identificacao = query_identificacao, estado_civil = query_estado_civil, data_hoje=date.today(), unidade_federativa = ufbr.list_uf, cidades_sc = ufbr.list_cidades(sigla='SC'), cidades_pr = ufbr.list_cidades(sigla='PR'), cidades_rs = ufbr.list_cidades(sigla='RS'))
    # http://jsfiddle.net/XH42p/


@app.route('/login_auth_forgot_password', methods=["GET", "POST"])
def page_login_auth_forgot_password():
    # depois para encriptar a senha
    # https://www.geeksforgeeks.org/hiding-and-encrypting-passwords-in-python/


    if (request.method == 'POST'):
        cpf_login_mask = request.form.get('cpf_login')
        new_password_login = request.form.get('new_password_login')
        cpf_login_without_mask = validacao_cpf.Cpf.retirapontoshifen(request.form.get('cpf_login'))

        query_cpf = db.engine.execute(f"SELECT * FROM LOGIN WHERE CPF_LOGIN = '{cpf_login_without_mask}';")

        if not(validacao_cpf.Cpf.validate(cpf_login_without_mask)):
            flash(f"Favor prencher o campo CPF, está incorreto: {cpf_login_mask}!", "error")
        elif not(query_cpf.fetchone()):
            flash(f"Não foi encontrado o CPF {cpf_login_mask} no sistema!", "error")
        else:
            #precisou ser dois diferentes, pois a query_cpf já executou...
            query_login = db.engine.execute(f"SELECT CPF_LOGIN, PASSWORD_LOGIN FROM LOGIN WHERE CPF_LOGIN = '{cpf_login_without_mask}';")
            get_query = query_login.fetchone()

            if (get_query[1] != new_password_login):
                db.engine.execute(
                    f"""
                        UPDATE LOGIN SET PASSWORD_LOGIN = '{new_password_login}' WHERE CPF_LOGIN={cpf_login_without_mask};
                    """)
                db.session.commit()
                flash(f"Senha alterada!", "error")
            else:
                flash(f"As senhas são as mesmas!", "error")
                
            
            
        return redirect(url_for('page_login_access'))

    return render_template("login/login_auth_forgot_password.html")
    
    
# --------------------------------------------------------------

if __name__ == "__main__":
    app.secret_key = "\x10)\xd8\x1a]J\x93z,\x1f)\x0b(w\\\xa7G\xbeQ\xa9\x10\xf7\x94T"

    with app.app_context():
        db.create_all()
        execute_insert()
        print(" [*** BANCO DE DADOS ATIVADO! ***]")
    app.run(debug=True)
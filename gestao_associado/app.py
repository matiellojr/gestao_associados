from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import sqlalchemy.orm as orm
# https://github.com/Sidon/py-ufbr
from pyUFbr.baseuf import ufbr
import sqlalchemy as sa
from datetime import date
from functions import validacao_cpf
import psycopg2


login_logado = True

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviestest.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:admin@localhost/gestao_associados_asblu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class associado(db.Model):
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
    id_estado_civil = sa.Column(sa.Integer, sa.ForeignKey('estado_civil.id')) 
    id_identificacao = sa.Column(sa.Integer, sa.ForeignKey('identificacao.id')) 
    situacao_trabalho = sa.Column(sa.String(50))
    id_tipo_sanguineo = sa.Column(sa.Integer, sa.ForeignKey('tipos_sanguineo.id')) 
    quantidades_filhos = sa.Column(sa.Integer)
    id_status_associado = sa.Column(sa.Integer, sa.ForeignKey('status_associado.id'))


    def __init__(self, id, cpf, nome_completo, endereco, data_cadastro, cidade, uf,  email, id_tipo_sanguineo, data_nascimento, data_atualizada, telefone, id_estado_civil, id_identificacao, situacao_trabalho, quantidades_filhos, id_status_associado):
        self.id = id
        self.data_cadastro = data_cadastro
        self.data_atualizada = data_atualizada
        self.cpf = cpf
        self.nome_completo = nome_completo
        self.endereco = endereco
        self.cidade = cidade
        self.uf = uf
        self.email = email
        self.id_tipo_sanguineo = id_tipo_sanguineo
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.id_estado_civil = id_estado_civil
        self.id_identificacao = id_identificacao
        self.situacao_trabalho = situacao_trabalho
        self.quantidades_filhos = quantidades_filhos
        self.id_status_associado = id_status_associado


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
    status = sa.Column(sa.String(50))

    def __init__(self, status):
        self.status = status
    

class status_associado(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    status = sa.Column(sa.String(50))

    def __init__(self, status):
        self.status = status


class status_mensalidade(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    status = sa.Column(sa.String(50))

    def __init__(self, status):
        self.status = status

class tipo_login(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    tipo = sa.Column(sa.String(50))

    def __init__(self, tipo):
        self.tipo = tipo




# --------------------------------------------
# Financeiro
# --------------------------------------------
class mensalidade(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    ehMensal = sa.Column(sa.Boolean)
    data_mensalidade = sa.Column(sa.Date)
    data_vencimento = sa.Column(sa.Date)
    valor_mensalidade = sa.Column(sa.Float)
    id_associado = sa.Column(sa.Integer, sa.ForeignKey('associado.id')) 
    id_status_mensalidade = sa.Column(sa.Integer, sa.ForeignKey('status_mensalidade.id'))

    def __init__(self, id, ehMensal, data_mensalidade,  data_vencimento, valor_mensalidade, id_associado, id_status_mensalidade):
        self.id = id
        self.ehMensal = ehMensal
        self.data_mensalidade = data_mensalidade
        self.data_vencimento = data_vencimento
        self.valor_mensalidade = valor_mensalidade
        self.id_associado = id_associado
        self.id_status_mensalidade = id_status_mensalidade


class pagamento(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    data_pagamento = sa.Column(sa.Date)
    valor_pagamento = sa.Column(sa.Float)
    pagamento_confirmado = sa.Column(sa.Boolean)
    id_status_pagamento = sa.Column(sa.Integer, sa.ForeignKey('status_pagamento.id'))
    id_mensalidade = sa.Column(sa.Integer, sa.ForeignKey('mensalidade.id')) 

    def __init__(self, id, data_pagamento, valor_pagamento,id_status_pagamento, id_mensalidade):
        self.id = id
        self.data_pagamento = data_pagamento
        self.valor_pagamento = valor_pagamento
        self.id_status_pagamento = id_status_pagamento
        self.id_mensalidade = id_mensalidade

# --------------------------------------------------------------
#  Login
# --------------------------------------------------------------
class login(db.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    cpf_login = sa.Column(sa.String(30))
    password_login = sa.Column(sa.String())
    id_tipo_login = sa.Column(sa.Integer, sa.ForeignKey('tipo_login.id')) 
    id_associado = sa.Column(sa.Integer, sa.ForeignKey('associado.id')) 

    def __init__(self, id, cpf_login, password_login, id_tipo_login, id_associado):
        self.id = id
        self.cpf_login = cpf_login
        self.password_login = password_login
        self.id_tipo_login = id_tipo_login
        self.id_associado = id_associado
        


def execute_insert():
    # busca uma linha > tem_tipos_sanguineos.fetchone()
    # busca todas as linhas > tem_tipos_sanguineos.fetchall() 
    # busca todas as linhas, cada linha tem um dicionário com os nomes dos campos > tem_tipos_sanguineos.dictfetchall() 
    tem_tipos_sanguineos = db.engine.execute('SELECT 1 FROM tipos_sanguineo;')
    tem_identificacao = db.engine.execute('SELECT 1 FROM identificacao;')
    tem_estado_civil = db.engine.execute('SELECT 1 FROM ESTADO_CIVIL;')
    tem_status_pagamento = db.engine.execute('SELECT 1 FROM STATUS_PAGAMENTO;')
    tem_status_associado = db.engine.execute('SELECT 1 FROM STATUS_ASSOCIADO;')
    tem_status_mensalidade = db.engine.execute('SELECT 1 FROM STATUS_MENSALIDADE;')
    tem_tipo_login = db.engine.execute('SELECT 1 FROM TIPO_LOGIN;')

    
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

    if not(tem_identificacao.fetchone()):
        db.engine.execute('''
            INSERT INTO IDENTIFICACAO VALUES (1, 'Surdo (a)');
            INSERT INTO IDENTIFICACAO VALUES (2, 'Surdocego');
            INSERT INTO IDENTIFICACAO VALUES (3, 'Deficiência Auditiva (DA)');
            INSERT INTO IDENTIFICACAO VALUES (4, 'Ouvinte');
        ''')

    if not(tem_estado_civil.fetchone()):
        db.engine.execute('''
            INSERT INTO ESTADO_CIVIL VALUES (1, 'Solteiro (a)');
            INSERT INTO ESTADO_CIVIL VALUES (2, 'Casado (a)');
            INSERT INTO ESTADO_CIVIL VALUES (3, 'Separado (a)');
            INSERT INTO ESTADO_CIVIL VALUES (4, 'Divorciado (a)');
            INSERT INTO ESTADO_CIVIL VALUES (5, 'Viúvo (a)');
        ''')

    if not(tem_status_associado.fetchone()):
        db.engine.execute('''
            INSERT INTO status_associado VALUES (1, 'Habilitado');
            INSERT INTO status_associado VALUES (2, 'Desabilitado');
            INSERT INTO status_associado VALUES (3, 'Não está apto para votar, 6 meses sem pagamento!');
        ''')

    if not(tem_status_mensalidade.fetchone()):
        db.engine.execute('''
            INSERT INTO status_mensalidade VALUES (1, 'Ainda falta pagar!');
            INSERT INTO status_mensalidade VALUES (2, 'Pago');
            INSERT INTO status_mensalidade VALUES (3, 'Não pago');
        ''')

    if not(tem_status_pagamento.fetchone()):
        db.engine.execute('''
            INSERT INTO status_pagamento VALUES (1, 'Pago');
            INSERT INTO status_pagamento VALUES (2, 'Não Pago');
        ''')

    if not(tem_tipo_login.fetchone()):
        db.engine.execute('''
            INSERT INTO tipo_login VALUES (0, 'Administrador');
            INSERT INTO tipo_login VALUES (1, 'Associado');
        ''')


@app.route('/<int:id>/inicio')
def page_principal_associado(id):
    if not(session.get("login")):
        return redirect("/associado")

    query_login_associado = db.engine.execute(f'''
        SELECT A.*, L.*, I.TIPO FROM ASSOCIADO A 
        INNER JOIN LOGIN L ON (A.ID = L.ID_ASSOCIADO)
        INNER JOIN IDENTIFICACAO I ON (A.ID_IDENTIFICACAO = I.ID)
        WHERE L.ID_ASSOCIADO = {id};
    ''')
    get = query_login_associado.fetchone()
    print(get[0])

    return render_template("index.html", id_associado = get[0], get = get)

@app.route('/index_admin')
def page_principal_admin():
    if not(session.get("login")):
        return redirect("/admin")
    return render_template("index_admin.html")


@app.route('/associado_lista/')
def page_associado_lista():
    if not(session.get("login")):
        return redirect("/admin")

    return render_template("associado/associado_lista.html", lista_associados = db.engine.execute("SELECT * FROM ASSOCIADO ORDER BY ID;"))


@app.route('/<int:id>/associado_atualiza_admin', methods=["GET", "POST"])
def page_associado_atualiza_admin(id):
    if not(session.get("login")):
        return redirect("/admin")

    _query_login = db.engine.execute(f"SELECT ID_TIPO_LOGIN FROM LOGIN WHERE ID_ASSOCIADO = {id};")
    query_tipos_sanguineos = db.engine.execute("SELECT * FROM TIPOS_SANGUINEO;")
    query_estado_civil = db.engine.execute('SELECT * FROM ESTADO_CIVIL;')
    query_associados = db.engine.execute(f"SELECT * FROM ASSOCIADO WHERE ID = {id} ORDER BY ID;")
    query_identificacao = db.engine.execute('SELECT * FROM IDENTIFICACAO;')
    query_status_associado = db.engine.execute('SELECT * FROM status_associado;')
    

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
            status__associado = request.form['status_associado']

            db.engine.execute(
                f"""
                    UPDATE ASSOCIADO SET DATA_CADASTRO='{data_cadastro}', DATA_ATUALIZADA='{data_atualizada}', CPF='{cpf}', NOME_COMPLETO='{nome_completo}', ENDERECO='{endereco}', CIDADE='{cidade}', UF='{uf}', EMAIL='{email}', DATA_NASCIMENTO='{data_nascimento}', TELEFONE='{telefone}', ID_ESTADO_CIVIL={estado_civil}, ID_IDENTIFICACAO={como_identifica}, SITUACAO_TRABALHO='{situacao_trabalho}', ID_TIPO_SANGUINEO={tipo_sanguineo}, QUANTIDADES_FILHOS={quantidades_filhos}, ID_STATUS_ASSOCIADO={status__associado} WHERE ID={id};
                """)
            db.session.commit()
            return redirect(url_for('page_associado_lista'))

    return render_template("associado/associado_atualiza_admin.html", _query_associados = query_associados, identificacao = query_identificacao, tipos_sanguineos = query_tipos_sanguineos, estado_civil = query_estado_civil, _status_associado = query_status_associado, login = _query_login,
    unidade_federativa = ufbr.list_uf,
    cidades_ac = ufbr.list_cidades(sigla='AC'),
    cidades_al = ufbr.list_cidades(sigla='AL'),
    cidades_ap = ufbr.list_cidades(sigla='AP'),
    cidades_am = ufbr.list_cidades(sigla='AM'),
    cidades_ba = ufbr.list_cidades(sigla='BA'),
    cidades_ce = ufbr.list_cidades(sigla='CE'),
    cidades_df = ufbr.list_cidades(sigla='DF'),
    cidades_es = ufbr.list_cidades(sigla='ES'),
    cidades_go = ufbr.list_cidades(sigla='GO'),
    cidades_ma = ufbr.list_cidades(sigla='MA'),
    cidades_mt = ufbr.list_cidades(sigla='MT'),
    cidades_ms = ufbr.list_cidades(sigla='MS'),
    cidades_mg = ufbr.list_cidades(sigla='MG'),
    cidades_pa = ufbr.list_cidades(sigla='PA'),
    cidades_pb = ufbr.list_cidades(sigla='PB'),
    cidades_pr = ufbr.list_cidades(sigla='PR'),
    cidades_pe = ufbr.list_cidades(sigla='PE'),
    cidades_pi = ufbr.list_cidades(sigla='PI'),
    cidades_rj = ufbr.list_cidades(sigla='RJ'),
    cidades_rn = ufbr.list_cidades(sigla='RN'),
    cidades_rs = ufbr.list_cidades(sigla='RS'),
    cidades_ro = ufbr.list_cidades(sigla='RO'),
    cidades_rr = ufbr.list_cidades(sigla='RR'),
    cidades_sc = ufbr.list_cidades(sigla='SC'),
    cidades_sp = ufbr.list_cidades(sigla='SP'),
    cidades_se = ufbr.list_cidades(sigla='SE'),
    cidades_to = ufbr.list_cidades(sigla='TO'))


@app.route('/<int:id>/associado_atualiza_associado', methods=["GET", "POST"])
def page_atualiza_associado(id):
    if not(session.get("login")):
        return redirect("/associado")

    _query_login = db.engine.execute(f"SELECT ID_TIPO_LOGIN FROM LOGIN WHERE ID_ASSOCIADO = {id};")
    query_tipos_sanguineos = db.engine.execute("SELECT * FROM TIPOS_SANGUINEO;")
    query_estado_civil = db.engine.execute('SELECT * FROM ESTADO_CIVIL;')
    query_associados = db.engine.execute(f"SELECT * FROM ASSOCIADO WHERE ID = {id} ORDER BY ID;")
    lista_associados = db.engine.execute(f"SELECT * FROM ASSOCIADO WHERE ID = {id} ORDER BY ID;")
    query_identificacao = db.engine.execute('SELECT * FROM IDENTIFICACAO;')
    query_status_associado = db.engine.execute('SELECT * FROM status_associado;')
    
    get_id_associado = query_associados.fetchone()

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

            db.engine.execute(
                f"""
                    UPDATE ASSOCIADO SET DATA_CADASTRO='{data_cadastro}', DATA_ATUALIZADA='{data_atualizada}', CPF='{cpf}', NOME_COMPLETO='{nome_completo}', ENDERECO='{endereco}', CIDADE='{cidade}', UF='{uf}', EMAIL='{email}', DATA_NASCIMENTO='{data_nascimento}', TELEFONE='{telefone}', ID_ESTADO_CIVIL={estado_civil}, ID_IDENTIFICACAO={como_identifica}, SITUACAO_TRABALHO='{situacao_trabalho}', ID_TIPO_SANGUINEO={tipo_sanguineo}, QUANTIDADES_FILHOS={quantidades_filhos} WHERE ID={id};
                """)
            db.session.commit()
            flash(f"Cadastro atualizado!", "success")
            return render_template("associado/associado_atualiza_associado.html", id_associado = get_id_associado[0])

    return render_template("associado/associado_atualiza_associado.html", _query_associados = lista_associados, identificacao = query_identificacao, tipos_sanguineos = query_tipos_sanguineos, estado_civil = query_estado_civil, _status_associado = query_status_associado, login = _query_login, id_associado = get_id_associado[0], unidade_federativa = ufbr.list_uf,
    cidades_ac = ufbr.list_cidades(sigla='AC'),
    cidades_al = ufbr.list_cidades(sigla='AL'),
    cidades_ap = ufbr.list_cidades(sigla='AP'),
    cidades_am = ufbr.list_cidades(sigla='AM'),
    cidades_ba = ufbr.list_cidades(sigla='BA'),
    cidades_ce = ufbr.list_cidades(sigla='CE'),
    cidades_df = ufbr.list_cidades(sigla='DF'),
    cidades_es = ufbr.list_cidades(sigla='ES'),
    cidades_go = ufbr.list_cidades(sigla='GO'),
    cidades_ma = ufbr.list_cidades(sigla='MA'),
    cidades_mt = ufbr.list_cidades(sigla='MT'),
    cidades_ms = ufbr.list_cidades(sigla='MS'),
    cidades_mg = ufbr.list_cidades(sigla='MG'),
    cidades_pa = ufbr.list_cidades(sigla='PA'),
    cidades_pb = ufbr.list_cidades(sigla='PB'),
    cidades_pr = ufbr.list_cidades(sigla='PR'),
    cidades_pe = ufbr.list_cidades(sigla='PE'),
    cidades_pi = ufbr.list_cidades(sigla='PI'),
    cidades_rj = ufbr.list_cidades(sigla='RJ'),
    cidades_rn = ufbr.list_cidades(sigla='RN'),
    cidades_rs = ufbr.list_cidades(sigla='RS'),
    cidades_ro = ufbr.list_cidades(sigla='RO'),
    cidades_rr = ufbr.list_cidades(sigla='RR'),
    cidades_sc = ufbr.list_cidades(sigla='SC'),
    cidades_sp = ufbr.list_cidades(sigla='SP'),
    cidades_se = ufbr.list_cidades(sigla='SE'),
    cidades_to = ufbr.list_cidades(sigla='TO'))


# --------------------------------------------------
#     Mensalidade
# --------------------------------------------------
@app.route('/mensalidade_lista_admin')
def page_mensalidade_lista():
    if not(session.get("login")):
        return redirect("/admin")

    query_status_pagamento = db.engine.execute("SELECT * FROM STATUS_PAGAMENTO;")
    query_lista = db.engine.execute('''
        SELECT A.ID, A.NOME_COMPLETO, M.*, P.*, ST.* FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        LEFT JOIN STATUS_PAGAMENTO ST ON (ST.ID = P.ID_STATUS_PAGAMENTO)
        ORDER BY 1;
    ''')


    count_mensalidade = db.engine.execute('''
        SELECT COUNT(*) FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        LEFT JOIN STATUS_PAGAMENTO ST ON (ST.ID = P.ID_STATUS_PAGAMENTO);
    ''')
    get_count = count_mensalidade.fetchone()

    return render_template("financeiro/mensalidade/mensalidade_lista_admin.html", lista_mensalidades_associado = query_lista, query_status_pagamento = query_status_pagamento, _get_count = get_count[0])


@app.route('/<int:id>/mensalidade_lista_asssociado')
def page_mensalidade_lista_associado(id):
    if not(session.get("login")):
        return redirect("/associado")

    query_status_pagamento = db.engine.execute("SELECT * FROM STATUS_PAGAMENTO;")
    query_lista_mensalidade = db.engine.execute(f'''
        SELECT A.ID, A.NOME_COMPLETO, M.*, P.*, ST.*  FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        LEFT JOIN STATUS_PAGAMENTO ST ON (ST.ID = P.ID_STATUS_PAGAMENTO)
        WHERE A.ID = {id}
        ORDER BY M.DATA_VENCIMENTO ASC;
    ''')

    query_associado_nome = db.engine.execute(f'''
        SELECT ID, NOME_COMPLETO FROM ASSOCIADO WHERE ID = {id};
    ''')
    get = query_associado_nome.fetchone()
    
    count_mensalidade = db.engine.execute(f'''
        SELECT COUNT(*) FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        LEFT JOIN STATUS_PAGAMENTO ST ON (ST.ID = P.ID_STATUS_PAGAMENTO)
        WHERE A.ID = {id};
    ''')
    get_count = count_mensalidade.fetchone() 
    
    status_mensalidade_id = db.engine.execute(f'''
        SELECT SM.ID, SM.STATUS FROM MENSALIDADE M
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        LEFT JOIN STATUS_MENSALIDADE SM ON (SM.ID = M.ID_STATUS_MENSALIDADE)
        WHERE A.ID = {id};
    ''')
    get_status_mensalidade = status_mensalidade_id.fetchone() 
    # get_id_status = get_status_mensalidade[0]
       

    return render_template("financeiro/mensalidade/mensalidade_lista_associado.html", lista_mensalidades_associado = query_lista_mensalidade, id_associado = get[0], nome_completo = get[1], status_mensalidade = query_status_pagamento, get_count = get_count[0])
    # get_status_mensalidade = get_id_status)



@app.route('/mensalidade_form', methods=["GET","POST"])
def page_mensalidade_form():
    if not(session.get("login")):
        return redirect("/admin")
    
    error = None
    query_mensalidade = db.engine.execute("SELECT * FROM MENSALIDADE;")
    query_status_mensalidade = db.engine.execute("SELECT * FROM STATUS_MENSALIDADE;")
    query_count_mensalidade = db.engine.execute("SELECT MAX(ID) FROM MENSALIDADE;")
    query_associados_habilitados = db.engine.execute('''
        SELECT A.ID, A.NOME_COMPLETO FROM ASSOCIADO A 
        INNER JOIN LOGIN L ON (A.ID = L.ID_ASSOCIADO)
        WHERE A.id_status_associado = 1
        ORDER BY 2;
    ''')

    data_mensalidade = request.form.get('data_mensalidade')
    data_vencimento = request.form.get('data_vencimento')
    valor_mensalidade = request.form.get('valor_mensalidade')
    mensalidade_mensal = request.form.get('tipo_mensalidade')
    id_associado = request.form.get('id_nome_associado')
    id_status_mensalidade = request.form.get('id_status_mensalidade')


    if (request.method == 'POST'):
        query_nome_associado = db.engine.execute(f"SELECT NOME_COMPLETO FROM ASSOCIADO WHERE ID = {id_associado};")
        get_nome_associado = query_nome_associado.fetchone()
        nome_associado = get_nome_associado[0]
        
        # se o tipo for mensal, recebe True
        if bool(mensalidade_mensal):
            Mensal = mensalidade_mensal
            if (data_vencimento < data_mensalidade):
                error = "Data de vencimento não pode ser antes que a Data de Início."
        else:
            # senão (se for anual) recebe false
            Mensal = mensalidade_mensal

        query_mensalidade_associado = db.engine.execute(f'''
            SELECT CAST(EXTRACT(MONTH FROM DATA_MENSALIDADE) AS INTEGER) AS MES, CAST(EXTRACT(YEAR FROM DATA_MENSALIDADE) AS INTEGER) AS ANO FROM MENSALIDADE WHERE ID_ASSOCIADO = {id_associado};
        ''')
        tem_mensalidade = query_mensalidade_associado.fetchall()

        lista_mensalidade = tem_mensalidade
        for lista_mensalidade in lista_mensalidade:
            month_mensalidade = lista_mensalidade[0]
            year_mensalidade = lista_mensalidade[1]
            if (int(month_mensalidade) == int(data_mensalidade[5:-3]) and int(year_mensalidade) == int(data_mensalidade[0:4])):
                if (error == None):
                    error = f"Mensalidade já está cadastrada para o(a) associado(a) {nome_associado} do {month_mensalidade}/{year_mensalidade}!"
                else:    
                    error = error + f" e a mensalidade já está cadastrada para o(a) associado(a) {nome_associado} do {month_mensalidade}/{year_mensalidade}!"

        if error == None:
            get_id = query_count_mensalidade.fetchone()
            if (get_id[0] == None):
                get_last_id = 1
            else:
                get_last_id = get_id[0] + 1

            db.engine.execute(
                f"""
                    INSERT INTO MENSALIDADE (ID, "ehMensal", DATA_MENSALIDADE, DATA_VENCIMENTO, VALOR_MENSALIDADE, ID_ASSOCIADO, ID_STATUS_MENSALIDADE) 
                    VALUES({get_last_id}, {Mensal}, '{data_mensalidade}', '{data_vencimento}', {valor_mensalidade}, {id_associado}, {id_status_mensalidade});
                """)
            db.session.commit()

            flash(f"Mensalidade cadastrada para {nome_associado}!", "success")
            return redirect(url_for('page_mensalidade_form'))
    return render_template("financeiro/mensalidade/mensalidade_form.html", error = error, mensalidade = query_mensalidade, eh_Mensal = bool(True), lista_associados = query_associados_habilitados, lista_status_mensalidade = query_status_mensalidade)

# @app.route('/<int:id>/mensalidade_consulta_associado' , methods=["GET", "POST"])
# def page_mensalidade_consulta_associado(id):
#     isMensal = bool(True)
#     query_associados_mensalidade = db.engine.execute(f"SELECT A.NOME_COMPLETO, M.* FROM MENSALIDADE M INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) WHERE M.ID = {id};")

#     return render_template("financeiro/mensalidade/mensalidade_consulta.html", eh_Mensal = isMensal, lista_associado_mensalidade = query_associados_mensalidade)


@app.route('/<int:id>/mensalidade_consulta_admin' , methods=["GET", "POST"])
def page_mensalidade_consulta_admin(id):
    if not(session.get("login")):
        return redirect("/admin")

    isMensal = bool(True)
    query_associados_mensalidade = db.engine.execute(f"SELECT A.NOME_COMPLETO, M.* FROM MENSALIDADE M INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) WHERE M.ID = {id} ORDER BY A.ID;")

    if (request.method == 'POST'):
        pass

    return render_template("financeiro/mensalidade/mensalidade_consulta_admin.html", eh_Mensal = isMensal, lista_associado_mensalidade = query_associados_mensalidade,
    lista_status_mensalidade = db.engine.execute("SELECT * FROM STATUS_MENSALIDADE;"))


@app.route('/<int:id>/delete_mensalidade')
def delete_mensalidade(id):
    db.engine.execute(f"DELETE FROM PAGAMENTO WHERE ID_MENSALIDADE = {id};")
    db.engine.execute(f"DELETE FROM MENSALIDADE WHERE ID = {id};")
    db.session.commit()
    return redirect(url_for('page_mensalidade_lista'))




# --------------------------------------------------
#     Pagamento
# --------------------------------------------------
@app.route('/<int:id>/pagamento_form' , methods=["GET", "POST"])
def page_pagamento_form(id):
    if not(session.get("login")):
        return redirect("/associado")

    query_count_pagamento = db.engine.execute("SELECT MAX(ID) FROM PAGAMENTO;")

    query_Men_Ass_Pag = db.engine.execute(f'''
        SELECT A.ID, A.NOME_COMPLETO, M.*, P.*  FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        WHERE M.ID = {id};
    ''')
    lista_get_id_pagamento = db.engine.execute(f'''
        SELECT A.ID, A.NOME_COMPLETO, M.* FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        WHERE M.ID = {id};
    ''')
    get = lista_get_id_pagamento.fetchone()
    
  

    data_pagamento = request.form.get('data_pagamento')
    valor_pagamento = request.form.get('valor_pagamento')
    id_status_pagamento = request.form.get('status_pagamento')
   

    if (request.method == 'POST'):
        get_id = query_count_pagamento.fetchone()
        if (get_id[0] == None):
            get_last_id = 1
        else:
            get_last_id = get_id[0] + 1

        db.engine.execute(f'''
            INSERT INTO PAGAMENTO (ID, DATA_PAGAMENTO, VALOR_PAGAMENTO, PAGAMENTO_CONFIRMADO, ID_STATUS_PAGAMENTO, ID_MENSALIDADE) 
            VALUES ({get_last_id}, '{data_pagamento}', {valor_pagamento}, TRUE, {id_status_pagamento}, {id});
        ''')
        db.engine.execute(f'''
            UPDATE MENSALIDADE SET ID_STATUS_MENSALIDADE = 2 WHERE ID = {id};
        ''')
        return redirect(url_for('page_mensalidade_lista_associado', id = get[0]))

    return render_template("financeiro/pagamento/pagamento_form.html", 
    query_Men_Ass_Pag = query_Men_Ass_Pag, 
    query_status_pagamento = db.engine.execute("SELECT * FROM STATUS_PAGAMENTO ORDER BY ID DESC;"),  
    date_today = date.today(), 
    id_associado = get[0])


@app.route('/<int:id>/pagamento_form_admin' , methods=["GET", "POST"])
def page_pagamento_form_admin(id):
    if not(session.get("login")):
        return redirect("/admin")

    query_count_pagamento = db.engine.execute("SELECT MAX(ID) FROM PAGAMENTO;")
    query_Men_Ass_Pag = db.engine.execute(f'''
        SELECT A.ID, A.NOME_COMPLETO, M.*, P.*  FROM MENSALIDADE M 
        INNER JOIN ASSOCIADO A ON (A.ID = M.ID_ASSOCIADO) 
        LEFT JOIN PAGAMENTO P ON (P.ID_MENSALIDADE = M.ID)
        WHERE M.ID = {id};
    ''')
    
    data_pagamento = request.form.get('data_pagamento')
    valor_pagamento = request.form.get('valor_pagamento')
    id_status_pagamento = request.form.get('status_pagamento')

    if (request.method == 'POST'):
        get_id = query_count_pagamento.fetchone()
        if (get_id[0] == None):
            get_last_id = 1
        else:
            get_last_id = get_id[0] + 1

        db.engine.execute(f'''
            INSERT INTO PAGAMENTO (ID, DATA_PAGAMENTO, VALOR_PAGAMENTO, PAGAMENTO_CONFIRMADO, ID_STATUS_PAGAMENTO, ID_MENSALIDADE) 
            VALUES ({get_last_id}, '{data_pagamento}', {valor_pagamento}, TRUE, {id_status_pagamento}, {id});
        ''')
        return redirect(url_for('page_mensalidade_lista'))

    return render_template("financeiro/pagamento/pagamento_form_admin.html", query_Men_Ass_Pag = query_Men_Ass_Pag, query_status_pagamento = db.engine.execute("SELECT * FROM STATUS_PAGAMENTO ORDER BY ID ASC;"), date_today = date.today())


# @app.route('/pagamento_lista' , methods=["GET", "POST"])
# def page_pagamento_lista():
#     return render_template("financeiro/pagamento/pagamento_lista.html")



# -------------------------------------------------------------
#         Login
# -------------------------------------------------------------
@app.route('/logout_admin')
def logout_administrador():
    session.pop('login', None)
    session.pop('password_login', None)
    flash(f"Deslogado com sucesso!", "success")
    return redirect(url_for('page_login_admin'))


@app.route('/admin', methods=["GET", "POST"])
def page_login_admin():
    if (request.method == 'POST'):
        tem_login = db.engine.execute(f"SELECT ID_TIPO_LOGIN FROM LOGIN WHERE CPF_LOGIN = '{request.form['login']}' AND PASSWORD_LOGIN = '{request.form['password_login']}';")

        if (tem_login.fetchone()):
            session['login'] = request.form['login']
            session['password_login'] = request.form['password_login']

            query_login_admin = db.engine.execute(f"SELECT ID_TIPO_LOGIN, ID_ASSOCIADO FROM LOGIN WHERE CPF_LOGIN = '{session['login']}' AND PASSWORD_LOGIN = '{session['password_login']}';")
            get = query_login_admin.fetchone()

            if (get[0] == 0):
                return redirect(url_for('page_principal_admin'))
        else:
            flash(f"Somente o Administrador pode entrar!", "error")

    return render_template("login/admin/login_admin.html")

@app.route('/')
def logout_associado():
    session.pop('login', None)
    session.pop('password_login', None)
    flash(f"Deslogado com sucesso!", "success")
    return redirect(url_for('page_login_associado'))


@app.route('/associado', methods=["GET", "POST"])
def page_login_associado():
    if (request.method == 'POST'):
        cpf_login = request.form.get('cpf_login')
        password_login = request.form.get('password_login')

        cpf_without_mask = validacao_cpf.Cpf.retirapontoshifen(cpf_login)

        session['login'] = request.form['cpf_login']
        session['password_login'] = request.form['password_login']
        
        tem_login = db.engine.execute(f'''
            SELECT A.*, L.* FROM ASSOCIADO A 
            INNER JOIN LOGIN L ON (A.ID = L.ID_ASSOCIADO)
            WHERE L.CPF_LOGIN = '{cpf_without_mask}' AND L.PASSWORD_LOGIN = '{password_login}' AND NOT(ID_TIPO_LOGIN = 0) AND A.ID_STATUS_ASSOCIADO = 1;
        ''')

        if (tem_login.fetchone()):
            query_login_associado = db.engine.execute(f"SELECT ID_TIPO_LOGIN, ID_ASSOCIADO FROM LOGIN WHERE CPF_LOGIN = '{cpf_without_mask}' AND PASSWORD_LOGIN = '{password_login}';")
            get = query_login_associado.fetchone()

            if (get[0] == 1):
                return redirect(url_for('page_principal_associado', id = get[1]))
        else:
            flash(f'''
            O Login ou a Senha está errada, ou está bloqueada! 
            \n Se deseja reativar a conta, falar com o administrador!''', "error")

    return render_template("login/associado/login_associado.html")


@app.route('/login_form', methods=["GET", "POST"])
def page_login_form():
    query_tipos_sanguineos = db.engine.execute("SELECT ID, TIPOS FROM TIPOS_SANGUINEO;")
    query_identificacao = db.engine.execute('SELECT ID, TIPO FROM IDENTIFICACAO;')
    query_estado_civil = db.engine.execute('SELECT ID, TIPO FROM ESTADO_CIVIL;')
    query_quantidade_associados = db.engine.execute("SELECT COUNT(*) FROM ASSOCIADO;")

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
    
    # quando clicar no botão "Cadastrar", no login_form
    if (request.method == 'POST'):
        cpf_without_mask = validacao_cpf.Cpf.retirapontoshifen(cpf)
        query_cpf = db.engine.execute(f"SELECT CPF FROM ASSOCIADO WHERE CPF = '{cpf_without_mask}';")
 
        if (query_cpf.fetchone()):
            query_status = db.engine.execute(f"SELECT ID_STATUS_ASSOCIADO FROM ASSOCIADO WHERE CPF = '{cpf_without_mask}';")
            get_status = query_status.fetchone()

            encontrou_cpf = f"Foi encontrado o CPF {request.form.get('cpf')} no sistema"

            if (get_status[0] == 3):
                flash(f'{encontrou_cpf}, mas a conta está desativada. Se deseja ativar, falar com a diretoria.')
            else:
                flash(f'{encontrou_cpf}.')
        elif not(validacao_cpf.Cpf.validate(cpf_without_mask)):
            flash(f"Favor prencher o campo CPF, está incorreto: {cpf_login}!", "error")
        else:
            get_id = query_quantidade_associados.fetchone()
            get_last_id = get_id[0] + 1
            table_associado = associado(get_last_id, cpf_without_mask, nome_completo, endereco, data_cadastro, cidade, uf, email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, como_identifica, situacao_trabalho, quantidades_filhos, 1)
            table_login = login(get_last_id, cpf_without_mask, password_login, 1, get_last_id)
            db.session.add(table_associado)
            db.session.add(table_login)
            db.session.commit()
            return redirect(url_for('page_login_associado'))

    return render_template("login/login_form.html", tipos = query_tipos_sanguineos, identificacao = query_identificacao, estado_civil = query_estado_civil, data_hoje=date.today(), unidade_federativa = ufbr.list_uf, 
    cidades_ac = ufbr.list_cidades(sigla='AC'),
    cidades_al = ufbr.list_cidades(sigla='AL'),
    cidades_ap = ufbr.list_cidades(sigla='AP'),
    cidades_am = ufbr.list_cidades(sigla='AM'),
    cidades_ba = ufbr.list_cidades(sigla='BA'),
    cidades_ce = ufbr.list_cidades(sigla='CE'),
    cidades_df = ufbr.list_cidades(sigla='DF'),
    cidades_es = ufbr.list_cidades(sigla='ES'),
    cidades_go = ufbr.list_cidades(sigla='GO'),
    cidades_ma = ufbr.list_cidades(sigla='MA'),
    cidades_mt = ufbr.list_cidades(sigla='MT'),
    cidades_ms = ufbr.list_cidades(sigla='MS'),
    cidades_mg = ufbr.list_cidades(sigla='MG'),
    cidades_pa = ufbr.list_cidades(sigla='PA'),
    cidades_pb = ufbr.list_cidades(sigla='PB'),
    cidades_pr = ufbr.list_cidades(sigla='PR'),
    cidades_pe = ufbr.list_cidades(sigla='PE'),
    cidades_pi = ufbr.list_cidades(sigla='PI'),
    cidades_rj = ufbr.list_cidades(sigla='RJ'),
    cidades_rn = ufbr.list_cidades(sigla='RN'),
    cidades_rs = ufbr.list_cidades(sigla='RS'),
    cidades_ro = ufbr.list_cidades(sigla='RO'),
    cidades_rr = ufbr.list_cidades(sigla='RR'),
    cidades_sc = ufbr.list_cidades(sigla='SC'),
    cidades_sp = ufbr.list_cidades(sigla='SP'),
    cidades_se = ufbr.list_cidades(sigla='SE'),
    cidades_to = ufbr.list_cidades(sigla='TO'))
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
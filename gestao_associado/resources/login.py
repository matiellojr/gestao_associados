from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import date
from functions import validacao_cpf
from flask_sqlalchemy import SQLAlchemy
from models.login import LoginModel
from models.associados import AssociadosModel

app = Flask(__name__)
db = SQLAlchemy(app)

class Login():
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
            cpf_without_mask = validacao_cpf.Cpf.retirapontoshifen(cpf)
            query_cpf = db.engine.execute(f"SELECT CPF, STATUS_ASSOCIADO FROM ASSOCIADOS WHERE CPF = '{cpf_without_mask}';")
            get_status = query_cpf.fetchone()

            if (get_status[0]):
                encontrou_cpf = f"Foi encontrado o CPF {request.form.get('cpf')} no sistema"

                if not(get_status[1]):
                    flash(f'{encontrou_cpf}, mas a conta está desativada. Se deseja ativar, falar com a diretoria.')
                else:
                    flash(f'{encontrou_cpf}.')
            elif not(validacao_cpf.Cpf.validate(cpf_without_mask)):
                flash(f"Favor prencher o campo CPF, está incorreto: {cpf_login}!", "error")
            else:
                get_id = query_quantidade_associados.fetchone()
                get_last_id = get_id[0] + 1
                associado = AssociadosModel(get_last_id, cpf_without_mask, nome_completo, endereco, data_cadastro, cidade, uf, email, tipo_sanguineo, data_nascimento, data_atualizada, telefone, estado_civil, situacao_trabalho, como_identifica, quantidades_filhos, False)
                table_login = LoginModel(get_last_id, cpf_without_mask, password_login)
                db.session.add(associado)
                db.session.add(table_login)
                db.session.commit()
                return redirect(url_for('page_login_access'))

        return render_template("login/login_form.html", tipos = query_tipos_sanguineos, identificacao = query_identificacao, estado_civil = query_estado_civil, data_hoje=date.today())


    @app.route('/login_auth_forgot_password', methods=["GET", "POST"])
    def page_login_auth_forgot_password():
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
                    flash(f"A senha é igual que deseja alterar!", "error")
                    
                
                
            return redirect(url_for('page_login_access'))

        return render_template("login/login_auth_forgot_password.html")
        
        
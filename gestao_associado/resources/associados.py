from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import date
from functions import validacao_cpf
from flask_sqlalchemy import SQLAlchemy
# from models.associados import AssociadosModel

app = Flask(__name__)
db = SQLAlchemy


class Associado():
        
    @app.route('/associado_lista')
    def page_associado_lista():
        query_lista = db.engine.execute("SELECT * FROM associados ORDER BY ID;")
        return render_template("associado/associado_lista.html", lista_associados = query_lista)


    @app.route('/<int:id>/associado_atualiza' , methods=["GET", "POST"])
    # mesmo sendo get ou post vc vai retornar uma pagina html e não um json
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

        return render_template("associado/associado_atualiza.html", _query_associados = query_associados, identificacao = query_identificacao, tipos_sanguineos = query_tipos_sanguineos, estado_civil = query_estado_civil)

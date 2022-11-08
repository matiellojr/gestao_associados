
# import re
# string = 'Geeksforgeeks'
# pattern = 'for'
# match=(re.search('.', '008.441.670-02'))
 

# #getting the starting index using match.start()
# print ("starting index", match.start())
 
# #Getting the start and end index in tuple format using match.span()
# print ("start and end index", match.span())


# cpf = '008.441.670-02'
# print(cpf.find('.') > 0)

# print(cpf)
# cpf = cpf.replace(".", "")
# cpf = cpf.replace("-", "")

# print(cpf)

# import datetime
# today = datetime.strftime("%d/%m/%Y")

# from datetime import datetime
# print(datetime.today().strftime('%d/%m/%Y'))

# import time
# today = time.strftime("%d/%m/%Y")

# import datetime

# datetoday = datetime.date.today()

# print(datetoday.format('DD/MM/YYYY'))


# formatted_date = datetime.date.strftime(datetoday, "%d/%m/%Y")
# print("\n Formatted Date String:", formatted_date, "\n")

# db.engine.execute(
#                 f"""
#                     UPDATE ASSOCIADOS SET DATA_CADASTRO='{data_cadastro}', DATA_ATUALIZADA='{data_atualizada}', CPF='{cpf}', NOME_COMPLETO='{nome_completo}', ENDERECO='{endereco}', CIDADE='{cidade}', UF='{uf}', EMAIL='{email}', DATA_NASCIMENTO='{data_nascimento}', TELEFONE='{telefone}', ESTADO_CIVIL='{estado_civil}', como_identifica='{como_identifica}', SITUACAO_TRABALHO='{situacao_trabalho}', TIPO_SANGUINEO='{tipo_sanguineo}', QUANTIDADES_FILHOS={quantidades_filhos}, STATUS_ASSOCIADO={status_associado} WHERE ID={id};
#                 """)

from pyUFbr.baseuf import ufbr

cidades = ufbr.list_cidades('PR')

for x in cidades:
    print(x)


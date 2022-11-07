from flask import Flask
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class LoginModel(db.Model):

    __tablename__ = 'login'
    id = sa.Column(sa.Integer, primary_key = True)
    cpf_login = sa.Column(sa.String(30))
    password_login = sa.Column(sa.String())

    def __init__(self, id, cpf_login, password_login):
        self.id = id
        self.cpf_login = cpf_login
        self.password_login = password_login
        

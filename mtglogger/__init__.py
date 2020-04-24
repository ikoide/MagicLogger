from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FRuZSEkDdmg3FVrTAN9YzTDmRhXP4Dyw7NPZjeK4ns4wQ6gGBAd6HnBQTWD7cMnF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from mtglogger import routes
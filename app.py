from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'dsadwe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['UPLOAD_FOLDER'] = './static/imagenes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from controlador import *

            

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=('micertificado.pem', 'llaveprivada.pem'))



from flask import Flask, render_template, Response, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config


#Models
from models.ModelUser import ModelUser
#Entities
from models.entities.Profesor import Profesor

app = Flask(__name__)

#configurar MySql
app.config['SECRET_KEY'] = '123456!qwerty'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sirf'

#inicializar MySql
db = MySQL(app)

#login_manager_app = LoginManager(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['rut'])
        #print(request.form['password'])
        profesor = Profesor(0,request.form['rut'],request.form['password'])
        logged_user = ModelUser.login(db,profesor)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash('password invalida')
                return render_template('auth/login.html')

        else:
            flash('Usuario no encontrado..')
            return render_template('auth/login.html')
        
    else:
        return render_template('auth/login.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()





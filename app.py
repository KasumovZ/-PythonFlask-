from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml, secrets
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
Bootstrap(app)
secret = secrets.token_urlsafe(32)

#DB configuration
db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = secret
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    #return redirect(url_for('about'))



@app.route('/Регистрация', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_datails = request.form
        if user_datails['password'] != user_datails['conpassword']:
            flash('Пароли не совпадают! Повторите ещё раз!', 'error')
            return render_template('Страница-регистрации.html')
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO user( email, user_name, password) VALUES (%s, %s, %s)', (user_datails['email'], user_datails['username'], generate_password_hash(user_datails['password'])))
        mysql.connection.commit()
        cursor.close()
        flash('Регистрация прошла успешно! Пожалуйства войдите в аккаунт! ', 'success')
        return redirect('/ВХОД')
    return render_template('Страница-регистрации.html')  

@app.route('/ВХОД', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_datails = request.form
        username = user_datails['username']
        cursor = mysql.connection.cursor()
        result_value = cursor.execute("SELECT * FROM user WHERE user_name = %s", ([username]))
        if result_value > 0:
            user = cursor.fetchone()
            if check_password_hash(user['password'], user_datails['password']):
                session['login'] = True
                session['username'] = user['user_name']
                flash('Добро пожаловать, ' + session['username'] + '!', 'success')
                return redirect('/Курорты') 
            else:
                cursor.close()
                flash('НЕТ такого пользователя! Попробуйте снова!', 'error')
                return render_template('Страница-входа.html')   
        else:
            cursor.close()
            flash('НЕТ такого пользователя! Попробуйте снова!', 'error')
            return render_template('Страница-входа.html')  
        cursor.close()
        return redirect('/')     

    return render_template('Страница-входа.html')
    #return redirect(url_for('about'))

@app.route('/')
def BOSS1():
    return render_template('index.html')     

@app.errorhandler(404)    
def page_not_found(e):
    return render_template('error.html')

@app.route('/Главная')
def BOSS2():
    return render_template('Главная.html')

@app.route('/Главная2')
def BOSS3():
    return render_template('Главная2.html')

@app.route('/Контакты')
def Contacts():
    return render_template('Контакты.html')

@app.route('/Контакты2')
def Contacts2():
    return render_template('Контакты2.html')

@app.route('/О-нас')
def Onas():
    return render_template('О-нас.html')

@app.route('/О-нас2')
def Onas2():
    return render_template('О-нас2.html')

@app.route('/Курорты')
def Curorts():
    return render_template('Курорты.html')

@app.route('/Карта')
def Carts():
    return render_template('Карта.html')
   


if __name__ == '__main__':
    app.run(debug=True)

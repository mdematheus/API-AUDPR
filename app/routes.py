from werkzeug.utils import secure_filename

from flask import Flask, render_template, redirect, url_for, flash, request, session
from models import db, User, Product
from utils import allowed_file, parse_excel
import pandas as pd
import cv2
import os
from pyzbar.pyzbar import decode

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['Login']
        password = request.form['Senha']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('USUARIO REGRISTRADO COM SUCESSO!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Login']
        password = request.form['Senha']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login bem sucedido. Entrando')
            return redirect(url_for('Inicio'))
        else:
            flash('Nome de Usuário ou senha inválidos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado!')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = parse_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            for index, row in data.iterrows():
                product = Product(barcode=row['Barcode'], section=row['Section'])
                db.session.add(product)
            db.session.commit()
            flash('Produto adicionado com Sucesso!')
        return redirect(url_for('scan'))
    return render_template('scan.html')

@app.route('/verify', methods=['POST'])
def verify():
    barcode = request.form['barcode']
    section = request.form['section']
    product = Product.query.filter_by(barcode=barcode).first()
    if product and product.section == section:
        flash('Produto não pertence a esta sessão.')
    else:
        flash('Produto não pertence a sua sessão.')
    return redirect(url_for('scan'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xls', 'xlsx'}

def parse_excel(filepath):
    df = pd.read_excel(filepath)
    return df

if __name__ == '__main__':
    app.run(debug=True)

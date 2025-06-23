from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_change_in_production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True, unique=True)

@app.route('/')
def index():
    return 'Flask App Running on Render!'

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email')
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match!'

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists!'

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return 'Welcome to your dashboard'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def create_app():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    app = create_app()

from flask import Flask, request, redirect, url_for, render_template, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import xlsxwriter

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_change_in_production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True, unique=True)

@app.route('/')
def index():
    return 'Flask App Running on Render!'

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email')
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match!'

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists!'

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return 'Welcome to your dashboard'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        life_expectancy = 85 if gender == 'female' else 80
        result = life_expectancy - age
    return render_template('calculator.html', result=result)

@app.route('/premium_estimator', methods=['GET', 'POST'])
def premium_estimator():
    result = None
    if request.method == 'POST':
        age = int(request.form['age'])
        coverage_amount = float(request.form['coverage_amount'])
        premium = coverage_amount / (100 - age)
        result = premium
    return render_template('premium_estimator.html', result=result)

@app.route('/pension_projection', methods=['GET', 'POST'])
def pension_projection():
    result = None
    if request.method == 'POST':
        current_age = int(request.form['current_age'])
        retirement_age = int(request.form['retirement_age'])
        current_savings = float(request.form['current_savings'])
        annual_contribution = float(request.form['annual_contribution'])
        annual_return = float(request.form['annual_return']) / 100

        years_to_retirement = retirement_age - current_age
        future_value = np.fv(annual_return, years_to_retirement, -annual_contribution, -current_savings)
        result = future_value
    return render_template('pension_projection.html', result=result)

@app.route('/annuity_calculator', methods=['GET', 'POST'])
def annuity_calculator():
    result = None
    if request.method == 'POST':
        payment_amount = float(request.form['payment_amount'])
        interest_rate = float(request.form['interest_rate']) / 100
        number_of_payments = int(request.form['number_of_payments'])

        present_value = np.pv(interest_rate, number_of_payments, -payment_amount)
        result = present_value
    return render_template('annuity_calculator.html', result=result)

@app.route('/loss_reserve_estimator', methods=['GET', 'POST'])
def loss_reserve_estimator():
    result = None
    if request.method == 'POST':
        incurred_losses = float(request.form['incurred_losses'])
        paid_losses = float(request.form['paid_losses'])
        loss_reserve = incurred_losses - paid_losses
        result = loss_reserve
    return render_template('loss_reserve_estimator.html', result=result)

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    data = request.form['data']
    filename = 'report.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, data)
    c.save()
    return send_file(filename, as_attachment=True)

@app.route('/export/excel', methods=['POST'])
def export_excel():
    data = request.form['data']
    filename = 'report.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', data)
    workbook.close()
    return send_file(filename, as_attachment=True)

def create_app():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    app = create_app()

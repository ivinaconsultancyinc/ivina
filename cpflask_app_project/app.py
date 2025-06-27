import forecasting
import reserves
import mortality_lapse
import esg

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

@app.route('/forecast')
def forecast():
    data = forecasting.simulate_historical_policy_data()
    model, forecast = forecasting.forecast_cash_flows(data)
    forecasting.plot_forecast(model, forecast)
    return 'Forecast generated'

@app.route('/reserves')
def calculate_reserves():
    dates, cash_flows = reserves.simulate_policy_data()
    reserve_values = reserves.calculate_reserves(dates, cash_flows, 0.03)
    reserves.plot_reserves(dates, reserve_values)
    return 'Reserves calculated'

@app.route('/mortality_lapse')
def mortality_lapse_model():
    data = mortality_lapse.simulate_mortality_lapse_data()
    mortality_model = mortality_lapse.train_mortality_model(data)
    lapse_model = mortality_lapse.train_lapse_model(data)
    predictions = mortality_lapse.predict_mortality_lapse(data, mortality_model, lapse_model)
    mortality_lapse.plot_mortality_lapse(predictions)
    return 'Mortality and lapse predictions generated'

@app.route('/esg')
def economic_scenarios():
    data = esg.simulate_economic_scenarios()
    esg.plot_economic_scenarios(data)
    return 'Economic scenarios simulated'

@app.route('/insurance_valuation')
def insurance_valuation():
    import pandas as pd
    import numpy as np
    from prophet import Prophet
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    import os

    # Step 1: Simulate Historical Claims Data
    np.random.seed(42)
    dates = pd.date_range(start='2015-01-01', periods=365*5, freq='D')
    claims = np.random.poisson(lam=50, size=len(dates))
    data = pd.DataFrame({'ds': dates, 'y': claims})

    # Step 2: Simulate Risk Factors
    age = np.random.randint(18, 70, size=len(dates))
    location_risk = np.random.normal(loc=1.0, scale=0.1, size=len(dates))
    health_risk = np.random.normal(loc=1.0, scale=0.1, size=len(dates))
    risk_factors = pd.DataFrame({'age': age, 'location_risk': location_risk, 'health_risk': health_risk})

    # Step 3: Risk Scoring Model
    X = risk_factors[['age', 'location_risk', 'health_risk']]
    y = claims
    risk_model = LinearRegression()
    risk_model.fit(X, y)
    risk_scores = risk_model.predict(X)

    # Step 4: Premium Calculation
    base_premium = 100
    premiums = base_premium + risk_scores * 0.1

    # Step 5: Forecast Future Claims
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Save plots to static folder
    os.makedirs('static/valuation', exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(data['ds'], data['y'], label='Historical Claims')
    plt.title('Historical Insurance Claims')
    plt.xlabel('Date')
    plt.ylabel('Number of Claims')
    plt.legend()
    plt.savefig('static/valuation/historical_claims.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(dates, risk_scores, label='Risk Scores')
    plt.title('Risk Scores Over Time')
    plt.xlabel('Date')
    plt.ylabel('Risk Score')
    plt.legend()
    plt.savefig('static/valuation/risk_scores.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(dates, premiums, label='Premiums')
    plt.title('Premiums Over Time')
    plt.xlabel('Date')
    plt.ylabel('Premium Amount')
    plt.legend()
    plt.savefig('static/valuation/premiums.png')
    plt.close()

    model.plot(forecast)
    plt.title('Forecast of Future Insurance Claims')
    plt.xlabel('Date')
    plt.ylabel('Number of Claims')
    plt.savefig('static/valuation/forecast.png')
    plt.close()

    model.plot_components(forecast)
    plt.savefig('static/valuation/forecast_components.png')
    plt.close()

    return render_template('insurance_valuation.html',
                           images=[
                               'valuation/historical_claims.png',
                               'valuation/risk_scores.png',
                               'valuation/premiums.png',
                               'valuation/forecast.png',
                               'valuation/forecast_components.png'
                           ])



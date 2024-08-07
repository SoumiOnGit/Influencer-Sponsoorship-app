from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a5f3c3d7e9c3b60b75c16d2ef2a9c8f3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    reach = db.Column(db.Integer, nullable=False)

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    companyname = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.Float, nullable=False)





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account_type')
def account_type():
    choice = request.args.get('choice')
    if choice == 'influencer':
        return redirect(url_for('influencer'))
    elif choice == 'sponsor':
        return redirect(url_for('sponsor'))
    return render_template('account_type.html')


@app.route('/influencer')
def influencer():
    return render_template('influencer.html')

@app.route('/sponsor')
def sponsor():
    return render_template('sponsor.html')


@app.route('/influencer/register', methods=['GET', 'POST'])
def influencer_register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        followers = request.form['followers']
        niche = request.form['niche']
        reach = request.form['reach']

        # Create a new influencer record
        new_influencer = Influencer(
            username=username,
            name=name,
            password=password,
            email=email,
            followers=int(followers),
            niche=niche,
            reach=int(reach)
        )

        try:
            db.session.add(new_influencer)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
    return render_template('influencer_register.html')

@app.route('/sponsor/register', methods=['GET', 'POST'])
def sponsor_register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        company_name = request.form['company_name']
        industry = request.form['industry']
        budget = request.form['budget']

        # Create a new sponsor record
        new_sponsor = Sponsor(
            username=username,
            name=name,
            password=password,
            email=email,
            companyname=company_name,
            industry=industry,
            budget=float(budget)
        )

        try:
            db.session.add(new_sponsor)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')

    return render_template('sponsor_register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user is an Influencer
        user = Influencer.query.filter_by(username=username, email=email, password=password).first()
        
        # Check if user is a Sponsor
        if not user:
            user = Sponsor.query.filter_by(username=username, email=email, password=password).first()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')

    return render_template('login.html')


@app.route('/influencer/dashboard')
def influencer_dashboard():
    return 'Influencer Dashboard'

@app.route('/sponsor/dashboard')
def sponsor_dashboard():
    return 'Sponsor Dashboard'





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

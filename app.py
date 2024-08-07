from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Influencer, Sponsor, Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a5f3c3d7e9c3b60b75c16d2ef2a9c8f3'
db.init_app(app)

def create_default_admin():
    with app.app_context():
        if not Admin.query.first():
            default_admin = Admin(username='admin', name='admin', password='admin', email='admin@mail.com')
            db.session.add(default_admin)
            db.session.commit()

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
        
        # Check admin login
        admin = Admin.query.filter_by(username=username, email=email, password=password).first()
        if admin:
            # Set session or handle admin login
            session['user'] = 'admin'
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        
        # Check influencer login
        influencer = Influencer.query.filter_by(username=username, email=email, password=password).first()
        if influencer:
            # Set session or handle influencer login
            session['user'] = 'influencer'
            flash('Login successful!', 'success')
            return redirect(url_for('influencer_dashboard')) # or relevant page
        
        # Check sponsor login
        sponsor = Sponsor.query.filter_by(username=username, email=email, password=password).first()
        if sponsor:
            # Set session or handle sponsor login
            session['user'] = 'sponsor'
            flash('Login successful!', 'success')
            return redirect(url_for('sponsor_dashboard')) # or relevant page
        
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
        create_default_admin()  
    app.run(debug=True)

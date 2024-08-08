from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db
from models import Influencer, Sponsor, Admin, Campaign, AdRequest
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a5f3c3d7e9c3b60b75c16d2ef2a9c8f3'

db.init_app(app)

def create_default_admin():
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
        
        admin = Admin.query.filter_by(username=username, email=email, password=password).first()
        if admin:
            session['user'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        
        influencer = Influencer.query.filter_by(username=username, email=email, password=password).first()
        if influencer:
            session['user'] = 'influencer'
            return redirect(url_for('influencer_dashboard', username=username))
        
        sponsor = Sponsor.query.filter_by(username=username, email=email, password=password).first()
        if sponsor:
            session['user'] = 'sponsor'
            return redirect(url_for('sponsor_dashboard', username=username))
        
        flash('Login failed. Check your credentials and try again.', 'danger')
    
    return render_template('login.html')

@app.route('/influencer/<username>/dashboard')
def influencer_dashboard(username):
    influencer = Influencer.query.filter_by(username=username).first_or_404()
    campaigns = []  # This should be replaced with actual campaign data
    return render_template('influencer_dashboard.html', influencer=influencer, campaigns=campaigns)

@app.route('/sponsor/<username>/dashboard')
def sponsor_dashboard(username):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    return render_template('sponsor_dashboard.html', sponsor=sponsor)

@app.route('/sponsor/<username>/dashboard/campaign', methods=['GET', 'POST'])
def sponsor_campaigns(username):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        # Extract form data
        category = request.form.get('category')
        product_link = request.form.get('product_link')
        requirements = request.form.get('requirements')
        budget = request.form.get('budget')
        live_date = request.form.get('live_date')
        target_gender = request.form.get('target_gender')
        target_age = request.form.get('target_age')
        target_location = request.form.get('target_location')
        
        # Create new campaign instance
        new_campaign = Campaign(
            name=request.form.get('campaign_name'),  # Assuming you have a field for campaign name
            description=request.form.get('campaign_description'),  # Assuming you have a field for campaign description
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),
            budget=budget,
            visibility=request.form.get('visibility'),
            goals=request.form.get('goals'),
            sponsor_id=sponsor.id,
            product_link=product_link,
            requirements=requirements,
            target_gender=target_gender,
            target_age=target_age,
            target_location=target_location,
            live_date=live_date
        )
        
        db.session.add(new_campaign)
        db.session.commit()
        
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('sponsor_dashboard', username=username))
    
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    return render_template('sponsor_campaigns.html', sponsor=sponsor, campaigns=campaigns)

@app.route('/admin/dashboard')
def admin_dashboard():
    return 'Admin Dashboard'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        create_default_admin()  
    app.run(debug=True)

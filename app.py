from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a5f3c3d7e9c3b60b75c16d2ef2a9c8f3'
db = SQLAlchemy(app)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account_type', methods=['GET', 'POST'])
def account_type():
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        if account_type == 'influencer':
            return redirect(url_for('influencer'))
        elif account_type == 'sponsor':
            return redirect(url_for('sponsor'))
        else:
            flash('Please select a valid account type.', 'warning')
    return render_template('account_type.html')

@app.route('/influencer')
def influencer():
    return 'Influencer dashboard or landing page'

@app.route('/sponsor')
def sponsor():
    return 'Sponsor dashboard or landing page'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

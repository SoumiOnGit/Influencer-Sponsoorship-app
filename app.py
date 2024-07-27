from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'a5f3c3d7e9c3b60b75c16d2ef2a9c8f3'


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


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    root_access = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        followers = request.form.get('followers', type=int)
        niche = request.form.get('niche')
        reach = request.form.get('reach', type=int)

        print(f"Received data: username={username}, name={name}, password={password}, email={email}, followers={followers}, niche={niche}, reach={reach}")

        if not (username and name and password and email and followers is not None and niche and reach is not None):
            flash("All fields are required.")
            return redirect(url_for('register'))

        # Create new Influencer
        new_influencer = Influencer(
            username=username,
            name=name,
            password=password,
            email=email,
            followers=followers,
            niche=niche,
            reach=reach
        )

        try:
            db.session.add(new_influencer)
            db.session.commit()
            flash("Registration successful.")
            print(f"Saved new influencer: {new_influencer}")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}")
            print(f"Error: {e}")

        return redirect(url_for('index'))
    
    return render_template('register.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

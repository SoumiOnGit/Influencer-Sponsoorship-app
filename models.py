from database import db

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    companyname = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, name, password, email):
        self.username = username
        self.name = name
        self.password = password
        self.email = email


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    goals = db.Column(db.Text, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    product_link = db.Column(db.String(255))
    requirements = db.Column(db.Text)
    target_gender = db.Column(db.String(10))
    target_age = db.Column(db.String(50))
    target_location = db.Column(db.String(100))
    live_date = db.Column(db.Date)
    flagged = db.Column(db.Boolean, default=False)
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)

    def __repr__(self):
        return f'<Campaign {self.name}>'


class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False)

from flask import Flask, render_template, request, redirect, url_for, flash, session ,abort
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
    accepted_ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='Accepted').all()
    return render_template('influencer_dashboard.html', influencer=influencer, accepted_ad_requests=accepted_ad_requests)


@app.route('/influencer/<username>/edit_profile', methods=['GET', 'POST'])
def edit_influencer_profile(username):
    influencer = Influencer.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        # Update influencer details
        influencer.name = request.form.get('name')
        influencer.password = request.form.get('password')
        influencer.email = request.form.get('email')
        influencer.followers = int(request.form.get('followers'))
        influencer.niche = request.form.get('niche')
        influencer.reach = int(request.form.get('reach'))

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('influencer_dashboard', username=username))

    return render_template('edit_influencer_profile.html', influencer=influencer)



@app.route('/sponsor/<username>/dashboard')
def sponsor_dashboard(username):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    return render_template('sponsor_dashboard.html', sponsor=sponsor, campaigns=campaigns)


@app.route('/sponsor/<username>/dashboard/campaign')
def sponsor_campaign_dashboard(username):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    return render_template('sponsor_campaign_dashboard.html', sponsor=sponsor, campaigns=campaigns)




@app.route('/sponsor/<username>/dashboard/campaign/create', methods=['GET', 'POST'])
def create_campaign(username):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        # Extract form data
        campaign_name = request.form.get('campaign_name')
        campaign_description = request.form.get('campaign_description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        budget = float(request.form.get('budget'))
        visibility = request.form.get('visibility')
        goals = request.form.get('goals')
        product_link = request.form.get('product_link')
        requirements = request.form.get('requirements')
        target_gender = request.form.get('target_gender')
        target_age = request.form.get('target_age')
        target_location = request.form.get('target_location')
        live_date = request.form.get('live_date')

        # Create new campaign instance
        new_campaign = Campaign(
            name=campaign_name,
            description=campaign_description,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
            budget=budget,
            visibility=visibility,
            goals=goals,
            sponsor_id=sponsor.id,
            product_link=product_link,
            requirements=requirements,
            target_gender=target_gender,
            target_age=target_age,
            target_location=target_location,
            live_date=datetime.strptime(live_date, '%Y-%m-%d').date()
        )

        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for('sponsor_campaign_dashboard', username=username))

    return render_template('create_campaign.html', sponsor=sponsor)



@app.route('/sponsor/<username>/campaign/<campaignid>')
def view_campaign(username, campaignid):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaign = Campaign.query.get_or_404(campaignid)
    return render_template('view_campaign.html', campaign=campaign, sponsor=sponsor)



@app.route('/sponsor/<username>/campaign/<campaignid>/ad_request/create', methods=['GET', 'POST'])
def create_ad_request(username, campaignid):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaign = Campaign.query.get_or_404(campaignid)
    influencers = Influencer.query.all()  # Query all influencers

    if request.method == 'POST':
        influencer_username = request.form.get('influencer_username')
        influencer = Influencer.query.filter_by(username=influencer_username).first_or_404()
        
        new_ad_request = AdRequest(
            campaign_id=campaign.id,
            influencer_id=influencer.id,
            messages=request.form.get('messages'),
            requirements=request.form.get('requirements'),
            payment_amount=float(request.form.get('payment_amount')),
            status='Pending'
        )
        
        db.session.add(new_ad_request)
        db.session.commit()

        # Redirect to the campaign page
        return redirect(url_for('view_campaign', username=username, campaignid=campaignid))
    
    return render_template('create_ad_request.html', campaign=campaign, sponsor=sponsor, influencers=influencers)





@app.route('/sponsor/<username>/campaign/<campaignid>/ad_request/<ad_request_id>')
def view_ad_request(username, campaignid, ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    campaign = Campaign.query.get_or_404(campaignid)
    
    if ad_request.campaign_id == campaign.id and ad_request.campaign.sponsor.username == username:
        return render_template('view_ad_request.html', ad_request=ad_request, campaign=campaign)
    else:
        abort(404)


@app.route('/influencer/<username>/campaigns')
def influencer_campaigns(username):
    influencer = Influencer.query.filter_by(username=username).first_or_404()
    ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id).all()
    
    return render_template('influencer_campaigns.html', influencer=influencer, ad_requests=ad_requests)



@app.route('/ad_request/<ad_request_id>/update_status', methods=['POST'])
def update_ad_request_status(ad_request_id):
    ad_request = AdRequest.query.get_or_404(ad_request_id)
    new_status = request.form.get('status')

    if new_status in ['Accepted', 'Rejected']:
        ad_request.status = new_status
        db.session.commit()
    
    return redirect(url_for('influencer_campaigns', username=ad_request.influencer.username))


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user' not in session or session['user'] != 'admin':
        abort(403)
    
    
    total_influencers = Influencer.query.count()
    total_sponsors = Sponsor.query.count()
    total_campaigns = Campaign.query.count()
    total_ad_requests = AdRequest.query.count()
    
    # Flagged data
    flagged_influencers = Influencer.query.filter_by(flagged=True).all()
    flagged_sponsors = Sponsor.query.filter_by(flagged=True).all()
    flagged_campaigns = Campaign.query.filter_by(flagged=True).all()
    
    # Active Users - Influencers who accepted ad requests
    accepted_influencers = db.session.query(AdRequest.influencer_id).distinct().count()
    no_ad_requests_influencers = total_influencers - accepted_influencers
    
    # Active Campaigns - Public vs Private
    public_campaigns = Campaign.query.filter_by(visibility='public').count()
    private_campaigns = Campaign.query.filter_by(visibility='private').count()

    # Fetch all influencers and sponsors
    all_influencers = Influencer.query.all()
    all_sponsors = Sponsor.query.all()

    return render_template(
        'admin_dashboard.html', 
        total_influencers=total_influencers, 
        total_sponsors=total_sponsors,
        total_campaigns=total_campaigns, 
        total_ad_requests=total_ad_requests,
        flagged_influencers=flagged_influencers,
        flagged_sponsors=flagged_sponsors,
        flagged_campaigns=flagged_campaigns,
        accepted_influencers=accepted_influencers,
        no_ad_requests_influencers=no_ad_requests_influencers,
        public_campaigns=public_campaigns,
        private_campaigns=private_campaigns,
        all_influencers=all_influencers,
        all_sponsors=all_sponsors
    )


@app.route('/sponsor/<username>/campaign/<campaignid>/update', methods=['GET', 'POST'])
def update_campaign(username, campaignid):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaign = Campaign.query.get_or_404(campaignid)
    
    if request.method == 'POST':
        # Update campaign details
        campaign.name = request.form.get('campaign_name')
        campaign.description = request.form.get('campaign_description')
        campaign.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        campaign.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        campaign.budget = float(request.form.get('budget'))
        campaign.visibility = request.form.get('visibility')
        campaign.goals = request.form.get('goals')
        campaign.product_link = request.form.get('product_link')
        campaign.requirements = request.form.get('requirements')
        campaign.target_gender = request.form.get('target_gender')
        campaign.target_age = request.form.get('target_age')
        campaign.target_location = request.form.get('target_location')
        campaign.live_date = datetime.strptime(request.form.get('live_date'), '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('view_campaign', username=username, campaignid=campaignid))
    
    return render_template('update_campaign.html', campaign=campaign, sponsor=sponsor)



@app.route('/sponsor/<username>/campaign/<campaignid>/delete', methods=['POST'])
def delete_campaign(username, campaignid):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaign = Campaign.query.get_or_404(campaignid)
    
    db.session.delete(campaign)
    db.session.commit()
    
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('sponsor_campaign_dashboard', username=username))


@app.route('/sponsor/<username>/campaign/<campaignid>/ad_request/<ad_request_id>/edit', methods=['GET', 'POST'])
def edit_ad_request(username, campaignid, ad_request_id):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaign = Campaign.query.get_or_404(campaignid)
    ad_request = AdRequest.query.get_or_404(ad_request_id)

    if ad_request.campaign_id != campaign.id or campaign.sponsor_id != sponsor.id:
        abort(403)  # Prevent unauthorized access

    if request.method == 'POST':
        ad_request.influencer_id = request.form.get('influencer_id')
        ad_request.requirements = request.form.get('requirements')
        ad_request.payment_amount = float(request.form.get('payment_amount'))
        ad_request.status = request.form.get('status')

        db.session.commit()
        flash('Ad request updated successfully!', 'success')
        return redirect(url_for('view_campaign', username=username, campaignid=campaignid))

    influencers = Influencer.query.all()
    return render_template('edit_ad_request.html', ad_request=ad_request, campaign=campaign, sponsor=sponsor, influencers=influencers)




@app.route('/sponsor/<username>/campaign/<campaignid>/ad_request/<ad_request_id>/delete', methods=['POST'])
def delete_ad_request(username, campaignid, ad_request_id):
    sponsor = Sponsor.query.filter_by(username=username).first_or_404()
    campaign = Campaign.query.get_or_404(campaignid)
    ad_request = AdRequest.query.get_or_404(ad_request_id)

    if ad_request.campaign_id != campaign.id or campaign.sponsor_id != sponsor.id:
        abort(403)  # Prevent unauthorized access

    db.session.delete(ad_request)
    db.session.commit()
    flash('Ad request deleted successfully!', 'success')
    return redirect(url_for('view_campaign', username=username, campaignid=campaignid))



@app.route('/admin/browse/influencers')
def browse_influencers():
    if 'user' not in session or session['user'] != 'admin':
        abort(403)
    
    influencers = Influencer.query.all()
    return render_template('browse_influencers.html', influencers=influencers)

@app.route('/admin/browse/sponsors')
def browse_sponsors():
    if 'user' not in session or session['user'] != 'admin':
        abort(403)
    
    sponsors = Sponsor.query.all()
    return render_template('browse_sponsors.html', sponsors=sponsors)

@app.route('/admin/browse/campaigns')
def browse_campaigns():
    if 'user' not in session or session['user'] != 'admin':
        abort(403)
    
    campaigns = Campaign.query.all()
    return render_template('browse_campaigns.html', campaigns=campaigns)



@app.route('/flag/influencer/<int:influencer_id>', methods=['POST'])
def flag_influencer(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    if influencer:
        influencer.flagged = True
        db.session.commit()
    return redirect(url_for('browse_influencers'))

@app.route('/unflag/influencer/<int:influencer_id>', methods=['POST'])
def unflag_influencer(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    if influencer:
        influencer.flagged = False
        db.session.commit()
    return redirect(url_for('browse_influencers'))

@app.route('/flag/sponsor/<int:sponsor_id>', methods=['POST'])
def flag_sponsor(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor:
        sponsor.flagged = True
        db.session.commit()
    return redirect(url_for('browse_sponsors'))

@app.route('/unflag/sponsor/<int:sponsor_id>', methods=['POST'])
def unflag_sponsor(sponsor_id):
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor:
        sponsor.flagged = False
        db.session.commit()
    return redirect(url_for('browse_sponsors'))

@app.route('/flag/campaign/<int:campaign_id>', methods=['POST'])
def flag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.flagged = True
        db.session.commit()
    return redirect(url_for('browse_campaigns'))

@app.route('/unflag/campaign/<int:campaign_id>', methods=['POST'])
def unflag_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.flagged = False
        db.session.commit()
    return redirect(url_for('browse_campaigns'))




@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login')) 





if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        create_default_admin()  
    app.run(debug=True)

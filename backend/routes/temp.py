@app.route('/sp_find', methods=['GET'])
def sp_find():
    selected_industry = request.args.get('industry', None)
    search_query = request.args.get('search', None)

    query = influencer.query


    # search influencers
    if search_query:
        search_filter = (influencer.name.ilike(f'%{search_query}%') | 
                         influencer.username.ilike(f'%{search_query}%') | 
                         influencer.email.ilike(f'%{search_query}%'))
        query = query.filter(search_filter)

    # executing the search query
    influencers = query.all()

    return render_template('sp_find.html', influencers=influencers, selected_industry=selected_industry, search_query=search_query)


#function for sponsor to accept a negotiated ad request
@app.route('/accept_negotiation/<int:ad_request_id>', methods=['POST'])
def accept_negotiation(ad_request_id):
    ad_request = adrequest.query.get_or_404(ad_request_id)
    ad_request.status = 'Request Accepted'
    db.session.commit()
    flash('Negotiated request accepted!', 'success')
    return redirect(url_for('view_ad_request', campaign_id=ad_request.campaign_id))

#function for sponsor to reject a negotiated ad request
@app.route('/reject_negotiation/<int:ad_request_id>', methods=['POST'])
def reject_negotiation(ad_request_id):
    ad_request = adrequest.query.get_or_404(ad_request_id)
    ad_request.status = 'Request Rejected'
    db.session.commit()
    flash('Negotiated request rejected!', 'danger')
    return redirect(url_for('view_ad_request', campaign_id=ad_request.campaign_id))

    class AdminDashboard(Resource):
    def get(self):
        # Only accessible by admin role
        pending_sponsors = Sponsor.query.filter_by(approval_status="Pending").all()
        pending_data = [{"id": s.id, "name": s.name, "email": s.email, "industry": s.industry} for s in pending_sponsors]
        
        return make_response(jsonify({"pending_sponsors": pending_data}), 200)

class ApproveSponsor(Resource):
    def post(self, sponsor_id):
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        sponsor.approval_status = "Approved"
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor approved"}), 200)

class RejectSponsor(Resource):
    def post(self, sponsor_id):
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        sponsor.approval_status = "Rejected"
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor rejected"}), 200)

from flask import request, jsonify, make_response, session
from flask_restful import Resource
from models import db, User, Role, SponsorProfile, InfluencerProfile, Campaign, AdRequest

# Ensure that your models have serialize methods
# Example:
# class SponsorProfile(db.Model):
#     # existing fields...
#     def serialize(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'name': self.name,
#             'industry': self.industry,
#             'flagged': self.flagged,
#             'approved': self.approved
#         }

#--------------------------------Admin Dashboard and Logout--------------------------------------------------------------
class AdminDashboardView(Resource):
    def get(self):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        # Fetch statistics
        total_users = SponsorProfile.query.count() + InfluencerProfile.query.count()
        number_of_sponsors = SponsorProfile.query.count()
        number_of_influencers = InfluencerProfile.query.count()
        number_of_campaigns = Campaign.query.count()
        active_ad_requests = AdRequest.query.filter_by(status='Request Accepted').count()
        flagged_sponsors = SponsorProfile.query.filter_by(flagged='yes').count()
        flagged_influencers = InfluencerProfile.query.filter_by(flagged='yes').count()
        flagged_campaigns = Campaign.query.filter_by(flagged='yes').count()
        flagged_ad_requests = AdRequest.query.filter_by(flagged='yes').count()

        data = {
            'total_users': total_users,
            'number_of_sponsors': number_of_sponsors,
            'number_of_influencers': number_of_influencers,
            'number_of_campaigns': number_of_campaigns,
            'active_ad_requests': active_ad_requests,
            'flagged_sponsors': flagged_sponsors,
            'flagged_influencers': flagged_influencers,
            'flagged_campaigns': flagged_campaigns,
            'flagged_ad_requests': flagged_ad_requests
        }

        return make_response(jsonify(data), 200)

class AdminLogoutView(Resource):
    def post(self):
        session.clear()
        return make_response(jsonify({"message": "You have been logged out."}), 200)

#--------------------------------Sponsor Management---------------------------------------------------------------------
class AdminSponsorApprovalListView(Resource):
    def get(self):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        pending_sponsors = SponsorProfile.query.filter_by(approved=False).all()
        sponsors_data = [sponsor.serialize() for sponsor in pending_sponsors]
        return make_response(jsonify({"pending_sponsors": sponsors_data}), 200)

class AdminApproveSponsorView(Resource):
    def post(self, sponsor_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        sponsor = SponsorProfile.query.get_or_404(sponsor_id)
        sponsor.approved = True
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor has been approved."}), 200)

class AdminSponsorListView(Resource):
    def get(self):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        sponsors = SponsorProfile.query.all()
        sponsors_data = [sponsor.serialize() for sponsor in sponsors]
        return make_response(jsonify({"sponsors": sponsors_data}), 200)

class AdminFlagSponsorView(Resource):
    def post(self, sponsor_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        sponsor = SponsorProfile.query.get_or_404(sponsor_id)
        sponsor.flagged = 'yes' if sponsor.flagged == 'no' else 'no'
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor flag status has been toggled."}), 200)

class AdminDeleteSponsorView(Resource):
    def delete(self, sponsor_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        sponsor = SponsorProfile.query.get_or_404(sponsor_id)

        # Delete associated ad requests through campaigns
        ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_profile_id == sponsor_id).all()
        for ad_request in ad_requests:
            db.session.delete(ad_request)

        # Delete associated campaigns
        campaigns = Campaign.query.filter_by(sponsor_profile_id=sponsor_id).all()
        for campaign in campaigns:
            db.session.delete(campaign)

        # Delete the sponsor profile
        db.session.delete(sponsor)
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor and all associated data have been deleted."}), 200)

#-------------------------------------------Influencer Management------------------------------------------------------
class AdminInfluencerListView(Resource):
    def get(self):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        influencers = InfluencerProfile.query.all()
        influencers_data = [influencer.serialize() for influencer in influencers]
        return make_response(jsonify({"influencers": influencers_data}), 200)

class AdminFlagInfluencerView(Resource):
    def post(self, influencer_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        influencer = InfluencerProfile.query.get_or_404(influencer_id)
        influencer.flagged = 'yes' if influencer.flagged == 'no' else 'no'
        db.session.commit()
        return make_response(jsonify({"message": "Influencer flag status has been toggled."}), 200)

class AdminDeleteInfluencerView(Resource):
    def delete(self, influencer_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        influencer = InfluencerProfile.query.get_or_404(influencer_id)

        # Delete associated ad requests
        ad_requests = AdRequest.query.filter_by(influencer_profile_id=influencer_id).all()
        for ad_request in ad_requests:
            db.session.delete(ad_request)

        # Delete the influencer profile
        db.session.delete(influencer)
        db.session.commit()
        return make_response(jsonify({"message": "Influencer and their associated ad requests have been deleted."}), 200)

#----------------------------------------Campaign Management--------------------------------------------------
class AdminCampaignListView(Resource):
    def get(self):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        campaigns = Campaign.query.all()
        campaigns_data = [campaign.serialize() for campaign in campaigns]
        return make_response(jsonify({"campaigns": campaigns_data}), 200)

class AdminFlagCampaignView(Resource):
    def post(self, campaign_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        campaign = Campaign.query.get_or_404(campaign_id)
        campaign.flagged = 'yes' if campaign.flagged == 'no' else 'no'
        db.session.commit()
        return make_response(jsonify({"message": "Campaign flag status has been toggled."}), 200)

class AdminDeleteCampaignView(Resource):
    def delete(self, campaign_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        campaign = Campaign.query.get_or_404(campaign_id)

        # Delete associated ad requests
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
        for ad_request in ad_requests:
            db.session.delete(ad_request)

        # Delete the campaign
        db.session.delete(campaign)
        db.session.commit()
        return make_response(jsonify({"message": "Campaign and all associated data have been deleted."}), 200)

#----------------------------------------Ad Request Management--------------------------------------------------
class AdminAdRequestListView(Resource):
    def get(self):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        ad_requests = AdRequest.query.all()
        ad_requests_data = [ad_request.serialize() for ad_request in ad_requests]
        return make_response(jsonify({"ad_requests": ad_requests_data}), 200)

class AdminFlagAdRequestView(Resource):
    def post(self, ad_request_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        ad_request = AdRequest.query.get_or_404(ad_request_id)
        ad_request.flagged = 'yes' if ad_request.flagged == 'no' else 'no'
        db.session.commit()
        return make_response(jsonify({"message": "Ad request flag status has been toggled."}), 200)

class AdminDeleteAdRequestView(Resource):
    def delete(self, ad_request_id):
        if not session.get('admin_logged_in'):
            return make_response(jsonify({"message": "Admin login required"}), 401)

        ad_request = AdRequest.query.get_or_404(ad_request_id)
        db.session.delete(ad_request)
        db.session.commit()
        return make_response(jsonify({"message": "Ad request has been deleted."}), 200)


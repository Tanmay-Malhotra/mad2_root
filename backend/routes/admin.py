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

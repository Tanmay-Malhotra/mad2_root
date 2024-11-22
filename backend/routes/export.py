from flask import Blueprint, Response
from flask_security import auth_token_required, roles_accepted, current_user
import csv
from io import StringIO
from backend.models import Campaign

export_bp = Blueprint('export', __name__)

@export_bp.route('/export-campaigns-csv', methods=['GET'])
@auth_token_required
@roles_accepted('sponsor')
def export_campaigns_csv():
    # Get the current user's sponsor profile
    sponsor_profile = current_user.sponsor_profile
    if not sponsor_profile:
        return {'message': 'Sponsor profile not found'}, 404

    # Get the campaigns created by the sponsor
    campaigns = sponsor_profile.campaigns

    # Prepare CSV content
    csv_data = []
    # Define header row
    csv_data.append([
        'Name',
        'Start Date',
        'End Date',
        'Budget',
        'Visibility',
        'Category',
        'Status'
    ])

    for campaign in campaigns:
        csv_data.append([
            campaign.name,
            campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else '',
            campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else '',
            campaign.budget,
            campaign.type,  # 'type' field represents visibility (public/private)
            campaign.category,
            campaign.status
        ])

    # Create a CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerows(csv_data)
    output = si.getvalue()
    si.close()

    # Prepare the response with the CSV file
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=campaigns.csv'
    return response

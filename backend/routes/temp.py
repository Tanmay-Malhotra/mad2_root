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

from celery import shared_task
from backend.models import Role, User, AdRequest
from send_mail import send_email
from jinja2 import Template
from datetime import datetime, timedelta
import os
from json import dumps
from httplib2 import Http
from flask import current_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# ------------------------- Monthly Reminder Task -------------------------
@shared_task(bind=True)
def monthly_reminder(self):
    try:
        
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            logger.warning("No admin role found.")
            return "No admin role found."

        admin = User.query.filter(User.roles.contains(admin_role)).first()
        if not admin:
            logger.warning("No admin user found.")
            return "No admin user found."

        template_path = os.path.join(os.path.dirname(__file__), 'template.html')
        with open(template_path, 'r') as file:
            template = Template(file.read())

        
        total_users = User.query.count()
        total_influencers = User.query.filter_by(user_type='influencer').count()
        total_sponsors = User.query.filter_by(user_type='sponsor').count()
        total_ad_requests = AdRequest.query.count()

        send_email(
            "malhotratanmay04@gmail.com",
            "Monthly Report",
            template.render(
                total_users=total_users,
                total_influencers=total_influencers,
                total_sponsors=total_sponsors,
                total_ad_requests=total_ad_requests
            )
        )
        logger.info("Monthly report sent to admin.")
        return "Monthly report sent to admin."
    except Exception as e:
        logger.error(f"Error in monthly_reminder task: {str(e)}")
        return f"Error in monthly_reminder task: {str(e)}"

# ------------------------- Daily Reminder Task -------------------------
@shared_task(bind=True)
def daily_reminder(self):
    try:
        influencers = User.query.filter(User.user_type == 'influencer').all()

        if not influencers:
            current_app.logger.info("No influencers found in the database.")
            return "No influencers found in the database."

        for influencer in influencers:

            pending_ad_requests = AdRequest.query.filter_by(
                influencer_profile_id=influencer.influencer_profile.id,
                status='Request Sent'
            ).all()


            if pending_ad_requests:
                message = (
                    f"Hello {influencer.influencer_profile.name}, "
                    f"You have {len(pending_ad_requests)} pending ad requests. "
                    "Please log in to your account and respond to them."
                )
            else:
                message = (
                    f"Hello {influencer.influencer_profile.name}, "
                    "You have no pending ad requests at the moment. "
                    "Check out public ad requests for new opportunities!"
                )

            send_notification(message)
            logger.info(f"Notification sent to influencer")

        return "Daily reminders sent to all influencers successfully."
    except Exception as e:
        current_app.logger.error(f"Error in daily_reminder task: {str(e)}")
        return f"Error in daily_reminder task: {str(e)}"

# ------------------------- Send Notification -------------------------
def send_notification(message):
    try:

        url = "https://chat.googleapis.com/v1/spaces/AAAA3x4WEOQ/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=xVyXbbh2sn--sHugovpCi8TVpIPcMMP7hB6jp4be_Cw"
        app_message = {"text": message}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        return f"Notification sent to influencer"
    except Exception as e:
        print(f"Error in send_notification task: {e}")
        return f"Error in send_notification task: {e}"



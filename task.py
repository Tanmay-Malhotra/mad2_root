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
        # Fetch the admin role
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            logger.warning("No admin role found.")
            return "No admin role found."

        # Fetch the admin user
        admin = User.query.filter(User.roles.contains(admin_role)).first()
        if not admin:
            logger.warning("No admin user found.")
            return "No admin user found."

        # Load email template
        template_path = os.path.join(os.path.dirname(__file__), 'template.html')
        with open(template_path, 'r') as file:
            template = Template(file.read())

        # Gather statistics for the report
        total_users = User.query.count()
        total_influencers = User.query.filter_by(user_type='influencer').count()
        total_sponsors = User.query.filter_by(user_type='sponsor').count()
        total_ad_requests = AdRequest.query.count()

        # Send the email
        send_email(
            admin.email,
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
        # Fetch influencers with pending ad requests
        pending_users = User.query.join(AdRequest, User.influencer_profile.has()).filter(
            AdRequest.status == 'Request Sent',
            User.user_type == 'influencer'
        ).all()

        if not pending_users:
            current_app.logger.info("No pending ad requests for influencers today")
            return "No pending ad requests for influencers today"

        for user in pending_users:
            send_notification(user.email, user.influencer_profile.name)

        return "Notifications sent to influencers successfully"
    except Exception as e:
        current_app.logger.error(f"Error in daily_reminder task: {str(e)}")
        return f"Error in daily_reminder task: {str(e)}"

# ------------------------- Send Notification -------------------------
def send_notification(email, username):
    try:
        webhook_url = current_app.config.get('GOOGLE_CHAT_WEBHOOK_URL')
        if not webhook_url:
            raise ValueError("Google Chat webhook URL is not configured")

        app_message = {
            "text": f"Hello {username}! You have pending ad requests. Please check your account."
        }
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()

        response, content = http_obj.request(
            uri=webhook_url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )

        if response.status == 200:
            logger.info(f"Notification sent to {username}")
        else:
            logger.error(f"Failed to send notification to {username}: {content}")

        return response.status
    except Exception as e:
        logger.error(f"Error in send_notification: {str(e)}")
        return f"Error in send_notification: {str(e)}"


""" (proj) tan@DESKTOP-N1K8ALE:~/root_mad2$ redis-cli
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> 
(proj) tan@DESKTOP-N1K8ALE:~/root_mad2$ sudo systemctl stop redis
(proj) tan@DESKTOP-N1K8ALE:~/root_mad2$ sudo ss -tulnp | grep 6379
tcp   LISTEN 0      511           0.0.0.0:6379       0.0.0.0:*    users:(("redis-server",pid=9436,fd=6))   
tcp   LISTEN 0      511              [::]:6379          [::]:*    users:(("redis-server",pid=9436,fd=7))   
(proj) tan@DESKTOP-N1K8ALE:~/root_mad2$ sudo kill -9 9436
(proj) tan@DESKTOP-N1K8ALE:~/root_mad2$ sudo ss -tulnp | grep 6379
(proj) tan@DESKTOP-N1K8ALE:~/root_mad2$ redis-server """
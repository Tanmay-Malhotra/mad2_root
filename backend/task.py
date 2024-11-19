from celery import shared_task
from backend.models import Role, User
from backend.send_mail import send_email
from jinja2 import Template
from datetime import datetime, timedelta
import os
from flask import current_app
from json import dumps
from httplib2 import Http


# Monthly Reminder Task
@shared_task(ignore_result=False)
def monthly_reminder():
    try:
        # Ensure Flask context
        with current_app.app_context():
            # Fetch admin role and user
            admin_role = Role.query.filter_by(name='admin').first()
            admin = User.query.filter(User.roles.contains(admin_role)).first()

            if not admin:
                print("No admin user found.")
                return "No admin user found."

            # Load email template
            with open('report.html', 'r') as file:
                template = Template(file.read())

            # Gather stats
            total_books = 1
            total_users = 2
            total_sections =3
            total_requests = 4

            # Send email
            send_email(
                admin.email,
                "Monthly Report",
                template.render(
                    total_books=total_books,
                    total_users=total_users,
                    total_sections=total_sections,
                    total_requests=total_requests
                )
            )
            print("Monthly report sent to admin.")
            return "Monthly report sent to admin."
    except Exception as e:
        print(f"Error in monthly_reminder task: {e}")
        return f"Error in monthly_reminder task: {e}"


# Daily Reminder Task
@shared_task(ignore_result=False)
def daily_reminder():
    try:
        # Ensure Flask context
        with current_app.app_context():
            # Find users inactive for the last 24 hours
            timestamp = datetime.utcnow() - timedelta(hours=24)
            not_visited_users = User.query.filter(User.last_login_at < timestamp).all()

            if not not_visited_users:
                return "No inactive users today"

            for user in not_visited_users:
                username = user.username
                if username != 'admin':
                    send_notification(username)

            return "Notifications sent to Google Chat space"
    except Exception as e:
        print(f"Error in daily_reminder task: {e}")
        return f"Error in daily_reminder task: {e}"


# Function to send Google Chat notifications
def send_notification(username):
    try:
        # Load Google Chat webhook URL from environment
        url = os.getenv("https://chat.googleapis.com/v1/spaces/AAAA3x4WEOQ/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=xVyXbbh2sn--sHugovpCi8TVpIPcMMP7hB6jp4be_Cw")
        if not url:
            raise ValueError("Google Chat webhook URL is not configured")

        # Create and send notification
        app_message = {"text": f"Hello {username}! You haven't visited the web library today. Please visit the app and read some books."}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response, content = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )

        if response.status == 200:
            print(f"Notification sent to {username}")
        else:
            print(f"Failed to send notification to {username}: {content}")

        return response.status
    except Exception as e:
        print(f"Error in send_notification: {e}")
        return f"Error in send_notification: {e}"

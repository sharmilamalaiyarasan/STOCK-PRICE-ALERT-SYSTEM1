# backend/services/email_services.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.core.config import settings

def send_email_notification(to_email: str, subject: str, message: str):
    try:
        sender_email = settings.MAILJET_SENDER_EMAIL

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "html"))


        mail_server = smtplib.SMTP("in-v3.mailjet.com", 587)
        mail_server.starttls()
        mail_server.login(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY)
        mail_server.sendmail(sender_email, to_email, msg.as_string())
        mail_server.quit()

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

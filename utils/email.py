# utils/email.py
import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_password_reset_email(email: str, reset_token: str):
    msg = MIMEText(f"Please use this link to reset your password: "
                   f"http://yourdomain.com/reset-password?token={reset_token}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = SMTP_USER
    msg['To'] = email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, email, msg.as_string())

def send_otp_email(email: str, otp: str):
    msg = MIMEText(f"Your verification code is: {otp}")
    msg['Subject'] = 'Signup Verification OTP'
    msg['From'] = SMTP_USER
    msg['To'] = email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, email, msg.as_string())

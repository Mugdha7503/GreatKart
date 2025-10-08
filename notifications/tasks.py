from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(to_email, username):
    subject = "Welcome to Our Website!"
    message = f"Hi {username},\n\nThank you for registering on our website."
    send_mail(subject, message, None, [to_email])
    return f"Email sent to {to_email}"
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(to_email, username):
    subject = "Order Confirmation!"
    message = f"Hello {username},\n\nThank you for your order! We are processing it and will update you shortly.\n\nBest regards,\nEkart Team"
    send_mail(subject, message, None, [to_email])
    return f"Email sent to {to_email}"
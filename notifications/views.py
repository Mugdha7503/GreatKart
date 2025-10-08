from django.shortcuts import render

# Create your views here.from django.shortcuts import render
from .tasks import send_welcome_email

def test_email(request):
    send_welcome_email.delay("testuser@example.com", "TestUser")
    return render(request, "email_sent.html")
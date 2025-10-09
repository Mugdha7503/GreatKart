from django.urls import path
from . import views

urlpatterns = [
    path('test_email/', views.test_email, name='test_email'),
]
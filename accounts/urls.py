from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import RegisterAPI, ProfileAPI, LoginAPI

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword, name='resetpassword'),

    path('api/login/', LoginAPI.as_view(),name="login_api"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterAPI.as_view(), name='register_api'),
    path('api/profile/', ProfileAPI.as_view(), name='profile_api'),

]


# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('', views.dashboard, name='dashboard'),

#     # JWT Auth
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

#     # Register API
#     path('api/register/', RegisterAPI.as_view(), name='register_api'),

#     # Protected profile API
#     path('api/profile/', ProfileAPI.as_view(), name='profile_api'),
# ]

from django.urls import path
from .views import LogoutApi, SendVerficationAPI, ValidateVerificationView, PasswordResetAPI, PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('logout/', LogoutApi.as_view(), name  = 'logout'),
    path('login/', TokenObtainPairView.as_view(), name = 'login'),
    path('login/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('email-verification/', SendVerficationAPI.as_view(), name = 'send-email-verification'),
    path('email-verification/<id>/<token>/', ValidateVerificationView.as_view(), name = 'verify-email'),
    path('password-reset/', PasswordResetAPI.as_view(), name = 'password-reset'),
    path('password-reset-redirect/<id>/<token>/', PasswordResetView.as_view(), name = 'password-reset-redirect'),
]
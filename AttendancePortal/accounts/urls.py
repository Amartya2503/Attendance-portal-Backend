from django.urls import path
from .views import LogoutApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('Logout/', LogoutApi.as_view(), name  = 'logout'),
    path('Login/', TokenObtainPairView.as_view(), name = 'login'),
    path('Login/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
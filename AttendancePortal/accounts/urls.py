from django.urls import path
from .views import LogoutApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('logout/', LogoutApi.as_view(), name  = 'logout'),
    path('login/', TokenObtainPairView.as_view(), name = 'login'),
    path('login/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
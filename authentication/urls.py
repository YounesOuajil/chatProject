from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login),
    path('signup/',views.signup),
    path('email_verified/<str:uidb64>/<str:token>/',views.email_verified),
    path('reset_password/',views.reset_password),
    path('reseted_password/<str:uidb64>/<str:token>/',views.reseted_password),
    path('token/refresh/', views.CustomTokenRefreshView.as_view)

]

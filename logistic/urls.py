from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),    
    path('home/', views.home, name="home"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('result/', views.resultPage, name="result"),

    # Authentication
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]
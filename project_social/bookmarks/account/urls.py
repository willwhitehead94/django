from django.urls import path
from . import views

urlpatterns = [
    # account views
    path('login/', views.user_login, name='login'),
]
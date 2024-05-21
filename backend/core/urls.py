from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('me/',views.ManageUserView.as_view(), name='me'),
]

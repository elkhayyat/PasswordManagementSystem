from django.urls import path

from authentication import views as authentication_views

app_name = 'authentication'
urlpatterns = [
    path('login/', authentication_views.LoginView.as_view(), name='login'),
    path('register.json/', authentication_views.RegisterView.as_view(), name='register.json'),
]

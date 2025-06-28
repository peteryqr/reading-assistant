from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='reading_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_document, name='upload_document'),
    path('view/<int:document_id>/', views.view_document, name='view_document'),
    path('chat/', views.chat, name='chat'),
] 
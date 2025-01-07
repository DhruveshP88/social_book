from django.urls import path
from . import views
from djoser import views as djoser_views
from .views import UploadedFileListView

urlpatterns = [
    # User registration and authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('otp-login/', views.otp_login, name='otp_login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),

    # Authors and sellers, file upload
    path('authors_and_sellers/', views.authors_and_sellers, name='authors_and_sellers'),
    path("upload_file/", views.upload_file, name="upload_file"),
    path("uploaded_files/", views.uploaded_files, name="uploaded_files"),
    path('my-books/', views.my_books_dashboard, name='my_books_dashboard'),


    # Djoser endpoints
    path('token/login/', djoser_views.TokenCreateView.as_view(), name='login'),
    path('users/', djoser_views.UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<username>/', djoser_views.UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('api/v1/uploaded_files/', UploadedFileListView.as_view(), name='uploaded-files'),
  
    # Add more Djoser endpoints if necessary
]


   

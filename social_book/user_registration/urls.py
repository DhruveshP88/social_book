from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]
urlpatterns += [
    path('login/', views.login_view, name='login'),
]
urlpatterns +=[
    path('home/',views.home,name='home')
]

urlpatterns +=[
  path('logout/', views.logout_view, name='logout'),
]

urlpatterns +=[
    path('authors_and_sellers/', views.authors_and_sellers, name='authors_and_sellers'),
    path("upload_file/", views.upload_file, name="upload_file"),
    path("uploaded_files/", views.uploaded_files, name="uploaded_files"),
]
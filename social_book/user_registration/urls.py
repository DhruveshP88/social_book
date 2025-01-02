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
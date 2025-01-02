
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')  # Replace with your homepage URL
    else:
        form = RegisterForm()

    return render(request, 'user_registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage or any other page
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'user_registration/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'user_registration/home.html')

def logout_view(request):
    logout(request)
    return redirect('login') 
    

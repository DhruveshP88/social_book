
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import CustomUser, UploadedFileForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.public_visibility = form.cleaned_data['public_visibility']
            user.birth_year = form.cleaned_data['birth_year']
            user.address = form.cleaned_data['address']
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
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
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


@login_required
def authors_and_sellers(request):
    # Filter users who have opted for public visibility
    users = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'user_registration/authors_and_sellers.html', {'users': users})

@login_required
def upload_file(request):
    if request.method == "POST":
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect("uploaded_files")  # Redirect to uploaded files page
    else:
        form = UploadedFileForm()
    return render(request, "user_registration/upload_file.html", {"form": form})


@login_required
def uploaded_files(request):
    files = request.user.uploaded_files.all()  # Fetch files uploaded by the logged-in user
    return render(request, "user_registration/uploaded_files.html", {"files": files})


def logout_view(request):
    logout(request)
    return redirect('login') 
    


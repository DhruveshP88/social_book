
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUser, UploadedFileForm
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .upload_model import UploadedFile
from .serializers import UploadedFileSerializer


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
                send_otp_email(user)  # Send OTP after login
                return redirect('otp_login')  # Redirect to OTP page
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

@login_required
def my_books_dashboard(request):
    # Fetch files uploaded by the logged-in user
    user_files = request.user.uploaded_files.all()

    # If the user has uploaded files, show them
    if user_files:
        return render(request, "user_registration/my_books_dashboard.html", {"files": user_files})
    else:
        # If no files uploaded, redirect to the upload page
        return redirect("upload_file")


def logout_view(request):
    logout(request)
    return redirect('login') 



class UploadedFileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch files uploaded by the authenticated user
        files = UploadedFile.objects.filter(user=request.user)
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


#otp genration

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.utils import timezone
from datetime import timedelta
from .otp_model import OTP

# Define Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=49811)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
    return creds

def send_otp_email(user):
    otp_code = OTP.generate_otp()  # Generate OTP
    OTP.objects.create(
        user=user,
        otp_code=otp_code,
        expires_at=timezone.now() + timedelta(seconds=300)  # OTP expires in 5 minutes
    )
    
    # Create the email message
    email_message = f"To: {user.email}\nSubject: Your OTP Code\n\nYour OTP code is: {otp_code}"
    raw_message = base64.urlsafe_b64encode(email_message.encode('utf-8')).decode('utf-8')

    # Send the email using Gmail API
    creds = get_gmail_credentials()
    service = build('gmail', 'v1', credentials=creds)
    message = {'raw': raw_message}
    service.users().messages().send(userId='me', body=message).execute()


        
#otp verification

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .otp_model import OTP
from django.contrib import messages

def otp_login(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        user = request.user  # You need to ensure the user is logged in already

        try:
            otp = OTP.objects.get(user=user, otp_code=otp_code)

            if otp.is_expired():
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('otp_login')

            login(request, user)  # Log the user in if OTP is valid
            otp.delete()  # Delete OTP after successful login
            return redirect('home')  # Redirect to the homepage or dashboard

        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp_login')

    return render(request, 'user_registration/otp_login.html')






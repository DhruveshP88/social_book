from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .upload_model import UploadedFile

class RegisterForm(UserCreationForm):
    # The password fields will automatically be handled by UserCreationForm
    public_visibility = forms.BooleanField(required=False, initial=True)  # Default to True
    birth_year = forms.IntegerField(min_value=1900, max_value=2100, required=False)  # Optional birth year
    address = forms.CharField(max_length=255, required=False)  # Optional address

    class Meta:
        model = CustomUser
        fields = ('email', 'public_visibility', 'birth_year', 'address')  # Include the fields you want

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")  # UserCreationForm automatically uses password1 and password2
        password2 = cleaned_data.get("password2")  # UserCreationForm automatically uses password1 and password2

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file", "title", "description", "visibility", "cost", "year_published"]
    def clean_file(self):
        file = self.cleaned_data.get('file')
        # Check if file is provided
        if file:
            # Check if file is either a PDF or JPEG
            if not file.name.endswith('.pdf') and not file.name.endswith('.jpeg') and not file.name.endswith('.jpg'):
                raise forms.ValidationError("Only PDF and JPEG files are allowed.")
            # Optional: Check file size (e.g., limit to 10MB)
            if file.size > 10 * 1024 * 1024:  # 10 MB
                raise forms.ValidationError("File size should not exceed 10 MB.")
        return file

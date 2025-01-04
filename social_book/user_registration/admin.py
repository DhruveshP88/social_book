from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterForm
from .models import CustomUser
from .upload_model import UploadedFile



class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm  # Form used for adding new users
    form = RegisterForm  # Form used for editing existing users
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "public_visibility", "birth_year", "address", "get_age")  # Add get_age method
    list_filter = ("email", "is_staff", "is_active", "public_visibility")
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Additional Info", {"fields": ("public_visibility", "birth_year", "address")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "public_visibility", "birth_year", "address")}
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)

    # Method to display age in the admin list view
    def get_age(self, obj):
        return obj.age  # Access the 'age' property

    get_age.short_description = 'Age'  # Optional: Change the column header to 'Age'

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "visibility", "uploaded_at")
    search_fields = ("title", "user__email")
    list_filter = ("visibility", "uploaded_at")



admin.site.register(CustomUser, CustomUserAdmin)

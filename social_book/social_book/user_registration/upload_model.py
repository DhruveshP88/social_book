from django.db import models
from django.conf import settings

class UploadedFile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically references the CustomUser model
        on_delete=models.CASCADE,
        related_name="uploaded_files",  # Allows reverse lookup: user.uploaded_files.all()
    )
    file = models.FileField(upload_to="uploads/")  # Files will be stored in 'media/uploads/'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visibility = models.BooleanField(default=True)  # Public or private visibility
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_published = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.email}"

from rest_framework import serializers
from .upload_model import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'title', 'file', 'description', 'visibility', 'cost', 'year_published', 'uploaded_at']

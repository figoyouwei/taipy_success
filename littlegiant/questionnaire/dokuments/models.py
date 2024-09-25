# documents/models.py

from django.db import models

class Dokument(models.Model):
    title = models.CharField(max_length=255)  # Title of the document
    content = models.TextField(blank=True, null=True)  # The content of the document, if stored as text
    # vector_index = 
    content_url = models.FileField(upload_to='rawdata/', blank=True, null=True)  # Optional file (PDF, DOCX, etc.)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the document is uploaded

    def __str__(self):
        return self.title
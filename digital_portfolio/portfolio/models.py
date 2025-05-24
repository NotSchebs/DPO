from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage  # optional, falls du es anderswo brauchst

class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=60)
    content = models.TextField(max_length=400)
    number = models.CharField(max_length=13)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
    upload_to='blog_files/',
    blank=True,
    null=True,
)

    def __str__(self):
        return self.title

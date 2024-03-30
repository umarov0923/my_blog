from django.db import models
from django.utils import timezone

from users.models import CustomUser
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='images/', default="images/default-post-pic.png")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    created_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment {self.content} by {self.user}"


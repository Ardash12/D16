from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Ads(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = RichTextUploadingField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'


class Answer(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text[:20]}...'


class News(models.Model):
    title = models.CharField(max_length=128)
    text = RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'


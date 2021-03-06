from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


# Create your models here.
class Entry(models.Model):
    """
    This class represents the entry model.
    """
    content = models.CharField(max_length=255, blank=False, unique=True)
    owner = models.ForeignKey('auth.user',
                              related_name="entries",
                              on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the model instance
        """
        return "{} : {}".format(self.date_created, self.content)


class Category(models.Model):
    """
    This class represents the Category model
    """
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey('auth.user',
                              related_name="categories",
                              on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        A representation of the model
        """
        return "{}: {}".format(self.name, self.description)


class Article(models.Model):
    """
    Class to represent the articles
    """
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=255)
    read_status = models.BooleanField(default=False)
    category = models.ForeignKey('Category',
                                 related_name="category",
                                 on_delete=models.CASCADE,
                                 null=True)
    owner = models.ForeignKey(
        'auth.user', related_name="owner", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


# This receiver handles token creation immediately a new user is created
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

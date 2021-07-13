from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField()  # Link unter dem das Video abrufbar ist


class Contact(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email_address = models.TextField()


class ContactList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField()
    contacts = models.ForeignKey(Contact, many=True, on_delete=models.SET_NULL, null=True)

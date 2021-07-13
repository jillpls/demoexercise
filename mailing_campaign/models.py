from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField()  # Link unter dem das Video abrufbar ist


class ContactList(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', related_name='contact_lists', on_delete=models.CASCADE)

    class Meta:
        ordering = ['creation_time']


class Contact(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email_address = models.TextField()
    contact_list = models.ForeignKey(ContactList, on_delete=models.CASCADE, related_name='contacts')



from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null= True)
    email = models.EmailField(unique=True , null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class room(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    topic = models.ForeignKey(topic , on_delete=models.SET_NULL , null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null= True , blank=True)
    participants = models.ManyToManyField(User, related_name='paticipants', blank=True)
    update =models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-create']

    def __str__(self) -> str:
        return str(self.name)

class message(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    room = models.ForeignKey(room , on_delete=models.CASCADE)
    body = models.TextField()
    update =models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-create']

    def __str__(self) -> str:
        return self.body[:50] 
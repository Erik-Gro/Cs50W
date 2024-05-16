from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    sex = models.CharField(max_length=30,blank=True,null=True)
    image = models.CharField(max_length=300)
    choosedpref = models.BooleanField(default=False)
    interestingsex = models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return f"{self.id} {self.username} is {self.sex} and choosed {self.choosedpref}" 


class Interests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_interests")
    male = models.BooleanField(default=False)
    female = models.BooleanField(default=False)
    alien = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} is interested in {self.male}, is interested in {self.female}, is interested in {self.alien}"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    message = models.CharField(max_length=30)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.user.username,
            "text": self.message,
        }

    def __str__(self):
        return f"{self.user} wrote {self.message}"
   
class Um(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_matrches")
    matches = models.ManyToManyField(User,blank=True, related_name="matches")

    def __str__(self):
        return f"{self.user} matches with {self.matches.all()} "

class Chatroom(models.Model):
    members = models.ManyToManyField(User,blank=True, related_name="members")
    mesages = models.ManyToManyField(Message,blank=True, related_name="chatroom_messages")

# python3 manage.py makemigrations dateapp
# python3 manage.py migrate
# python3 manage.py runserver
# python3 manage.py createsuperuser
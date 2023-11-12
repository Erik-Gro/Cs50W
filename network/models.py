from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} {self.username} "
    

class Post(models.Model):
    content = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Owner")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,null=True, blank=True, related_name="likes")

    def __str__(self):
        return f"Post {self.id} made by {self.owner} on {self.date.strftime('%d %b %Y %H:%M:%S')} liked by {self.likes.all()}"
    

class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="userFollow")
    userFollowing = models.ManyToManyField(User,null=True, blank=True, related_name="userFollowing")
    userFollowers = models.ManyToManyField(User,null=True, blank=True, related_name="userFollowers")
    
    def __str__(self):
        return f" id ={self.id} {self.user} is following {self.userFollowing.all()} and follows {self.userFollowers.all()}"
    

# class Like(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_like")
#     post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_like")
    
#     def __str__(self):
#         return f"{self.user} liked {self.post}"




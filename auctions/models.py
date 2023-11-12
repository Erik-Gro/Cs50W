from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name
    
class Bid(models.Model):
    bid_price = models.IntegerField()
    bidder = models.CharField(max_length=30)
    item = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.bidder} bidded with {self.bid_price}"
     
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=90)
    image = models.CharField(max_length=300)
    bid = models.ForeignKey(Bid,null=True,blank=True, on_delete=models.SET_NULL, related_name="bid")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User,null=True,blank=True, related_name="watchlist")

    def __str__(self):
        return self.title

 
    
class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    commentedItem = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentedItem")
    comment = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.writer} comment on {self.commentedItem} and said {self.comment}"

 

    
# python3 manage.py makemigrations auctions
# python3 manage.py migrate



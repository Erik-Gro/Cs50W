from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User , Categories, Bid , Listing , Comment

def index(request):
    actives = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "actives": actives
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    allCategories = Categories.objects.all()
    if request.user.is_authenticated:
     if request.method == "GET":
        return render(request, "auctions/createListing.html",{
            "categories": allCategories
        })
    if request.method == "POST":
        user = request.user
        description = request.POST["description"]
        img = request.POST["img"]
        price = int(request.POST["price"])
        title = request.POST["title"]
        option = request.POST["category"]
        thiscategory = Categories.objects.get(category_name=option)
        newbid = Bid(
            bid_price = price,
            bidder = user,
            item = title
        )
        newbid.save()
        newListing = Listing(
            title=title,
            image=img,
            description=description,
            bid = newbid,
            category=thiscategory,
            owner=user
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    else: return HttpResponseRedirect(reverse(index))


def allCategories(request):
    if request.method == "GET":
        categories = Categories.objects.all()
        return render(request, "auctions/allCategories.html",{
            "categories": categories
        })
    
def categorylist(request,ct):
    if request.method == "GET":
        category = Categories.objects.get(category_name=ct)
        mc = Listing.objects.filter(category=category,active=True)
        return render(request, "auctions/categoryList.html",{
            "mc": mc
        })


def showListing(request,item):
    if request.method == "GET":
        user = request.user
        mc = Listing.objects.get(title=item)
        isw = user in mc.watchlist.all()
        comments = Comment.objects.filter(commentedItem=mc)
        return render(request, "auctions/listing.html",{
         "mc": mc,
         "user": user,
         "isw": isw,
         "comments": comments
        })

def showWatchlist(request):
    if request.method == "GET":
        user = request.user
        mc = Listing.objects.filter(watchlist=user)
        return render(request, "auctions/watchlist.html",{
         "mc": mc,
         "user": user
        })

def addToWatchlist(request,id):
    if request.method == "POST":
        user = request.user
        mc = Listing.objects.get(title=id)
        mc.watchlist.add(user)
        return redirect(reverse('showListing',kwargs={'item' : mc.title}))

def removeFromWatchlist(request,id):
    if request.method == "POST":
        user = request.user
        mc = Listing.objects.get(title=id)
        mc.watchlist.remove(user)
        return redirect(reverse('showListing',kwargs={'item' : mc.title}))

def bid (request,t):
    if request.method == "POST":
        user = request.user
        money = int(request.POST["money"])
        mc = Listing.objects.get(title=t)
        isw = user in mc.watchlist.all()
        comments = Comment.objects.filter(commentedItem=mc)
        if mc.active == False:
            return render(request, "auctions/listing.html",{
         "mc": mc,
         "user": user,
         "isw": isw,
         "ms": "this listing in sold",
         "comments": comments
        })
        if mc.bid.bid_price >= money:
            return render(request, "auctions/listing.html",{
         "mc": mc,
         "user": user,
         "isw": isw,
         "ms": "your bid is too low",
         "comments": comments
        })
        else:
            oldbid = Bid.objects.get(bid_price = mc.bid.bid_price,item = mc.title)
            oldbid.delete()
            newprice = Bid(
            bid_price = money,
            bidder = user,
            item = mc.title
        )
            newprice.save()
            mc.bid = newprice
            mc.save()
            return render(request, "auctions/listing.html",{
         "mc": mc,
         "user": user,
         "isw": isw,
         "ms": "your bit beated last bid!",
         "comments": comments
        })

def comment(request,t):
    if request.method == "POST":
        user = request.user
        comment = request.POST["comment"]
        mc = Listing.objects.get(title=t)
        comments = Comment.objects.filter(commentedItem=mc)
        isw = user in mc.watchlist.all()
        newComment = Comment(
            writer = user,
            commentedItem = mc,
            comment = comment
        )
        newComment.save()
        return render(request, "auctions/listing.html",{
         "mc": mc,
         "user": user,
         "isw": isw,
         "ms": "your bit beated last bid!",
         "comments": comments
        })

def closeauc(request,t):
    if request.method == "POST":
        user = request.user
        mc = Listing.objects.get(title=t)
        comments = Comment.objects.filter(commentedItem=mc)
        isw = user in mc.watchlist.all()
        if user == mc.owner:
            mc.active = False
            mc.save()
            return render(request, "auctions/listing.html",{
         "mc": mc,
         "user": user,
         "isw": isw,
         "ms": "this auction is closed",
         "comments": comments
        })
            


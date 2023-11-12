import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Following


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        followinglist = Following(
            user = user
        )
        followinglist.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request):
    if request.method == "GET":
        return render(request, "network/newPost.html")
    if request.method == "POST":
        if request.user is not None:
            content = request.POST["content"]
            Post (
                content = content,
                owner = request.user
            ).save()
            return render(request, "network/newPost.html")

def allPosts(request,page):
 if request.method == "GET":
    listOfpage = Post.objects.all().order_by('-date')
    paginator = Paginator(listOfpage, 10)
    getPosts = paginator.get_page(page)
    listsubs = Following.objects.filter(userFollowing=request.user)
    subs = len(listsubs)
    return render(request, "network/allPosts.html", {
                "Posts": getPosts,
                "user": request.user,
                "Following": Following.objects.get(user=request.user),
                "subs": subs
                # "test": getPosts.previous_page_number()
            })
@csrf_exempt
def Change(request,page):
     if request.method == "PUT":
        try:
          post = Post.objects.get(owner=request.user, pk=page)
        except Post.DoesNotExist:
         return JsonResponse({"error": "Email not found."}, status=404)
        data = json.loads(request.body)
        if data.get("text") is not None:
            post.content = data["text"]
            post.save()
        return HttpResponse(status=204)
     else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
     
@csrf_exempt
def Like(request,page):
     if request.method == "PUT":   
         if request.user is not None:
              post = Post.objects.get(pk=page)
            #   if request.user == post.objects.filter(likes=request.user):
            #    post.likes.remove(request.user)
              if request.user in post.likes.all():     
                post.likes.remove(request.user)
                return  JsonResponse({"boolean": False}, status=201)
            #   like = Post.objects.filter(pk=page,likes=request.user)
            #   post.likes.remove(like)
              else:
               post.likes.add(request.user)
               return  JsonResponse({"boolean": True}, status=201)
              
@csrf_exempt
def Follow(request,id):
     if request.method == "PUT":
         if request.user is not None:
            #  post = Post.objects.get(pk=owner)
            #  userfollowinglist = Following.objects.get(user=request.user)
            #  z = post.owner
            #  if z in userfollowinglist.userFollowing.all():
            #      userfollowinglist.userFollowing.remove(z)
            #      return  JsonResponse({"boolean": False}, status=201)
            #  else:
            #       userfollowinglist.userFollowing.add(z)
            #       return  JsonResponse({"boolean": True}, status=201)
             userfollowinglist = Following.objects.get(user=request.user)
             owner = User.objects.get(pk=id)
             if owner in userfollowinglist.userFollowing.all():
                 userfollowinglist.userFollowing.remove(owner)
                 return JsonResponse({"boolean": True}, status=201)
             else:
               userfollowinglist.userFollowing.add(owner)
               return  JsonResponse({"boolean": False}, status=201)
             
# def test(request)

def Profile(request,id,page):
    # post = Post.objects.get(pk=id)
    # owner = post.owner
    owner = User.objects.get(pk=id)
    listsubs = Following.objects.filter(userFollowing=owner)
    subs = len(listsubs)
    pageownerfollowinglist = Following.objects.get(user=owner)
    userFollowing = pageownerfollowinglist.userFollowing.all()
    lengthofuserFollowing = len(userFollowing)
    userfollow = Following.objects.get(user=request.user).userFollowing.all()
    listOfpage = Post.objects.filter(owner=owner).order_by('-date')
    paginator = Paginator(listOfpage, 10)
    getPosts = paginator.get_page(page)
    return render(request, "network/Profile.html", {
                "owner": owner,
                "subs": subs,
                "hefollows": lengthofuserFollowing,
                "userfollow": userfollow,
                "Posts": getPosts,
            })
    
def Followposts(request,page):
    if  request.user.is_authenticated:
        # id = request.user.id
        # user = User.objects.get(pk=id)
        listingfollowing = Post.objects.exclude(owner=request.user).order_by('-date')
        # listOfpage = Post.objects.filter(owner=owner).order_by('-date')
        paginator = Paginator(listingfollowing, 10)
        getPosts = paginator.get_page(page)
        return render(request, "network/allPosts.html", {
                "Posts": getPosts,
            })
    else: return
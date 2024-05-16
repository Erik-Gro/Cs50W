from django.shortcuts import render,HttpResponseRedirect
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Um, Chatroom,Interests,Message
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def dateapp(request):
 if request.user.is_authenticated:
     chatrooms = Chatroom.objects.filter(members=request.user) 
     return render(request, "dateapp.html", {
        "chatrooms": chatrooms
            })

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dateapp"))
    else:
        return HttpResponseRedirect(reverse("login"))

def preferences(request):
    if request.user.is_authenticated:
        return render(request, "preferences.html")

def login_view(request):
    if request.method == "POST":
        nick = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=nick, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "login.html")
    
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        img = request.POST["image"]
        gender = request.POST["gender"]
        password = request.POST["password"]
        preference = request.POST["preference"]
        confirmation = request.POST["confirmation"]
        # return render(request, "test.html", {
        #         "test1": img,
        #     }) 
        if password != confirmation:
            return render(request, "mail/register.html", {
                "message": "Passwords must match."
            })
        try:
            curruser = User.objects.create_user(username, email, password)
            curruser.save()
        except IntegrityError as e:
            print(e)
            return render(request, "login.html", {
                "message": "Email address already taken."
            })  
        login(request, curruser)
        curruser.image = img
        if gender == '1':
            curruser.sex = 'male'
            curruser.save()
        elif gender == '2': 
            curruser.sex = 'female'
            curruser.save()
        if preference == '3':
            curruser.interestingsex = 'male'
            curruser.save()
        elif preference == '4': 
            curruser.interestingsex = 'female'
            curruser.save()
            curruser.save()
        usermatches = Um(
                 user = curruser
            )
        usermatches.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
@csrf_exempt
def loadmessagges(request,id):
    if request.method == "POST":
        chatroom = Chatroom.objects.get(id=id)
        messages = chatroom.mesages.all()
        return JsonResponse([message.serialize() for message in messages], safe=False)

@csrf_exempt    
def loadcards(request,id):
    if request.method == "POST":
        array = []
        interestingpeope = User.objects.filter(sex=request.user.interestingsex)
        usermatches = Um.objects.get(user=request.user)
        for man in interestingpeope:
          if man not in usermatches.matches.all() and man.interestingsex == request.user.sex:array.append({"id":man.id,"name":man.username,"img":man.image})
        return JsonResponse(array, safe=False)
    
@csrf_exempt    
def add(request,id):
    if request.method == "POST":
        me = User.objects.get(id=request.user.id)
        partner = User.objects.get(id=id)
        usermatches = Um.objects.get(user=me)
        usermatches.matches.add(partner)
        usermatches.matches.add(me)
        if Um.objects.get(user=me,matches=partner) is not None and Um.objects.get(user=partner,matches=me) is not None:
         chatroom = Chatroom  (
         )
         chatroom.save()
         chatroom.members.add(me)
         chatroom.members.add(partner)
         chatroom.save()
        return  JsonResponse({"mess": "success"}, status=201)

@csrf_exempt 
def newmes(request,id):
    if request.method == "PUT":
        data = json.loads(request.body)
        message = Message (
        )
        message.user = request.user
        message.message = data.get("mes")
        message.save()
        chatroom = Chatroom.objects.get(id=id)
        chatroom.mesages.add(message)
        chatroom.save()
        return  JsonResponse({"mess": "success"}, status=201)

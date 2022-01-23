from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.contrib.auth.models import AbstractUser

from .models import User, Post

def index(request):
    if request.method == "POST":
        poster = User.objects.get(username = request.user.username)
        p = Post(postContent = request.POST["newPostText"], postedBy = poster)
        p.save()


    return render(request, "network/index.html", {
        "allPosts": Post.objects.all()
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profilePage(request,userId):
    profileUser = User.objects.get(id=userId)
    loggedUser = User.objects.get(username = request.user.username)
    followStatus = False
    if loggedUser in profileUser.followers.all():
        followStatus = True
    if request.method == 'POST' and loggedUser.id != profileUser.id:
        # if (request.POST["follow"])
        print ("Run TEST")
        if followStatus:
            print("ELSE TEST")
            print (loggedUser.following.filter(id=profileUser.id))
            loggedUser.following.remove(profileUser)
            print (loggedUser.following.filter(id=profileUser.id))
        else:
            print("Add TEST")
            loggedUser.following.add(profileUser)
        loggedUser.save()
        return HttpResponseRedirect(reverse( "profilePage",args=(userId) )) 

    return render(request, "network/profilePage.html", {
        "userObj": profileUser,
        "ownPostList": profileUser.ownPosts.all(),
        "followStatus": followStatus,
    })

    #  {% for post in userObj.ownPosts %}
    #         {{post.postContent}}
    #     {%endfor%}
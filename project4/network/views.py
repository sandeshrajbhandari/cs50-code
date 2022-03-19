from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.contrib.auth.models import AbstractUser
from django.core.paginator import Paginator #for displaying only 10 posts per page. 

from .models import User, Post

def index(request):
    if request.user.is_authenticated:
        print("User is logged in "+ request.user.username)
    else:
        return HttpResponseRedirect(reverse("login")) #redirect to login page if not logged in. 
    if request.method == "POST":
        poster = User.objects.get(username = request.user.username)
        p = Post(postContent = request.POST["newPostText"], postedBy = poster)
        p.save()
    # code for edit Post. 
    if request.method == "PUT":
        editor = User.objects.get(username = request.user.username)
        bodyData = json.loads(request.body)
        bodyPostId=bodyData["postId"]
        editingPost = Post.objects.get(id=bodyPostId)
        postAuthor = editingPost.postedBy
        if editor == postAuthor:
            print ("edited to: "+ bodyData["newPostText"])
            editingPost.postContent = bodyData["newPostText"]
            print ("Changed  : " + editingPost.postContent)
            editingPost.save()

    #paginator code, boilerplate modify.
    post_list = Post.objects.all().order_by('-postDate') 
    #to change order by postDate, '-' in -postDate for reversed.
    paginator = Paginator(post_list, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
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
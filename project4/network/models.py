from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from django.db.models.fields import related


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False, blank=True, null=True)

class Post(models.Model):
    postDate= models.DateTimeField(auto_now_add=True)
    postContent = models.TextField(max_length=500)
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownPosts")
    likes = models.ManyToManyField(User, related_name="likedPosts", blank=True)
# class Likes(models.Model):
#     likedPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
#     liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

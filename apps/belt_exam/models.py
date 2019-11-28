from django.db import models
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.messages import get_messages
import re
from datetime import date, datetime, timedelta
import timeago 

class UserManager(models.Manager):
    def is_reg_valid(self, request):

        if len(request.POST['first_name']) < 2:
            messages.error(request, "First Name should be at least 2 characters")

        if len(request.POST['last_name']) < 2:
            messages.error(request, "Last Name should be at least 2 characters")

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, "Invalid email")

        if len(request.POST['password']) < 8:
            messages.error(request, "Password should be at least 8 characters")

        if request.POST['password'] != request.POST['confirm_password']:
            messages.error(request, "Passwords do not match")
    
        if (request.POST['birthday']) == '':
            messages.error(request, "Must enter a birthday")
        
        else:
            birthday = datetime.strptime(request.POST['birthday'], "%Y-%m-%d")
            


            today = date.today()
            now = datetime.now()
            age = (today.year - birthday.year -
            ((today.month, today.day) <
            (birthday.month, birthday.day)))

            if birthday > datetime.today():
                messages.error(request, "Birthday can not be a future date")
            
            if age < 13:
                messages.error(request, "Must be at least 13 to register")

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0
        

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.DateField()
    objects = UserManager()

class WishManager(models.Manager):
    def is_wish_valid(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors["item"] = "A wish must consist of at least 3 characters"

        if len(postData['desc']) == 0:
            errors["desc"] = "A description must be provided!"
        return errors


class Wish(models.Model):
    item = models.CharField(max_length=100, null=True)
    desc = models.TextField(default="Description of item")
    status = models.CharField(max_length=100, default="Pending")
    user = models.ForeignKey(User, related_name="wishes")
    likers = models.ManyToManyField(User, related_name="liked_wishes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
    

# class Like(models.Model):
#     wish = models.ForeignKey(Wish, related_name="liked_wishes")
#     user = models.ForeignKey(User, related_name="likes")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
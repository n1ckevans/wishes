from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from apps.belt_exam.models import *
import bcrypt
from datetime import date, datetime


def index(request):
    return render(request, "belt_exam/index.html")

def login(request):
    valid_user = User.objects.filter(email=request.POST['email'])
    if valid_user:
        current_user = valid_user[0]

        pw_match = bcrypt.checkpw(request.POST['password'].encode(), current_user.password.encode())

        if pw_match:
            request.session['user_id'] = current_user.id
        else:
            messages.error(request, "Invalid credentials")
            return redirect("/")
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Please try again")
        return redirect("/")
    return redirect ("/wishes")

def register(request):
    taken_user = User.objects.filter(email=request.POST['email'])
    if taken_user:
        messages.error(request, "Invalid credentials")
        return redirect("/")

    if not User.objects.is_reg_valid(request):
        return redirect("/")

    hashed = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())


    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed, birthday=request.POST['birthday'])
    request.session['user_id'] = new_user.id
    print(new_user.id)
    return redirect("/wishes")

def wishes(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)
    

    # wish_id = request.session.get('wish_id')
    # wish = Wish.objects.get(id=wish_id)
    all_users = User.objects.all()
    all_wishes = Wish.objects.all()
    granted_wishes = Wish.objects.filter(status="Granted")
    print(user.liked_wishes.count())
    # print(likes)
   
    context = {"user": user, "wishes" : all_wishes, "granted" : granted_wishes}
    return render(request, "belt_exam/home.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def new_wish(request):
    

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)
   
    context = {"user": user}

    return render(request, "belt_exam/new.html", context)


def make_wish(request):
    errors = Wish.objects.is_wish_valid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/wishes/new')
    else: 
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect("/")

        user = User.objects.get(id=user_id)
    
        new_wish = Wish.objects.create(item=request.POST['item'], desc=request.POST['desc'], status="Pending", user=user)
        request.session['wish_id'] = new_wish.id
        print(new_wish.id)
        return redirect("/wishes")

def cancel(request):
   
    return redirect("/wishes")

def remove(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    print(wish)
    wish.delete()
    return redirect("/wishes")

def edit(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
   

    context = {"wish" : wish}

    return render(request, "belt_exam/edit.html", context)

def edit_wish(request, wish_id):
    errors = Wish.objects.is_wish_valid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/wishes/edit/'+wish_id)
    else:
        wish = Wish.objects.get(id=wish_id)
        wish.item = request.POST['item']
        wish.desc = request.POST['desc']
        wish.save()
        return redirect("/wishes")

def granted(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.status = "Granted"
    wish.save()

    return redirect("/wishes")

def stats(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)
   
    all_granted = Wish.objects.filter(status__contains="Granted").count()
    user_granted = Wish.objects.filter(user=user, status__contains="Granted").count()
    user_pending = Wish.objects.filter(user=user, status__contains="Pending").count()

    print(user_pending)

  

    context = {"user": user, "all_granted" : all_granted, "user_granted" : user_granted, "user_pending" : user_pending}



    return render(request, "belt_exam/stats.html", context)

def wishes_like(request, wish_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect("/")

    user = User.objects.get(id=user_id)
    wish = Wish.objects.get(id=wish_id)
    user.liked_wishes.add(wish)
    
    return redirect("/wishes")

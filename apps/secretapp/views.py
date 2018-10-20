from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count

import bcrypt
from .models import *
#------------------------------------------------------------------------
def signin(request):
    return render(request, 'secretapp/login.html')
#------------------------------------------------------------------------
def register(request):
    return render(request, 'secretapp/register.html')
#------------------------------------------------------------------------
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/signin')
    request.session['email']=request.POST['email']
    user=User.objects.get(email=request.POST['email'])
    return redirect('/secrets')
#------------------------------------------------------------------------
def add(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
        # check if the errors object has anything in it
    
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/register')
    
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the user to be updated, make the changes, and save
        request.session['email']=request.POST['email']
        user = User.objects.create()
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.email = request.POST['email']
        user.pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.save()
        messages.success(request, "User successfully added")
        # redirect to a success route
        return redirect('/secrets')
def logout(request):
    del request.session['email']
    return redirect('/')
def secretindex(request):
    if 'email' in request.session:
        user=User.objects.get(email=request.session['email'])
        context={
            'secrets':Secret.objects.all(),
            'user':user
        }
        return render(request,'secretapp/secrets.html',context)
    else:
        return redirect('/')
def addsecret(request):
    errors = Secret.objects.basic_validator(request.POST)
        # check if the errors object has anything in it
    print(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the Secret back to the form to fix the errors
        return redirect('/secrets')
    
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the Secret to be updated, make the changes, and save
        user=User.objects.get(email=request.session['email'])
        Secret.objects.create(content = request.POST['content'],uploaded_by=user)
        # secret.
        messages.success(request, "secret successfully added")
        print('========================================================')
        # redirect to a success route
        return redirect('/secrets')
def like(request,postid,userid):
    if 'email' not in request.session:
        return redirect('/')
    post=Secret.objects.get(id=postid)
    user=User.objects.get(id=userid)
    try:
        Check_if_Liked = post.likes.get(user_id=userid,post_id=postid)
    except:
        flag=False
    if flag is False:
        post.likes.add(user)
    return redirect('/secrets')
def popular(request):
    user=User.objects.get(email=request.session['email'])
    context={
        'posts':Secret.objects.annotate(like_count=Count('likes')).order_by('-like_count'),
        'user':user
    }
    return render(request,'secretapp/popular.html',context)

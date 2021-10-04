from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            )
        messages.success(request, f"Welcome {user.first_name}")
        request.session['userid'] = user.id
        request.session['firstName'] = user.first_name
        return redirect('/success')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        messages.success(request, "User Logged In")
        return redirect('/success')

def success(request):
    context = {'users': User.objects.all()}
    return render(request, 'success.html', context)

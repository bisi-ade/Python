from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User
from .models import Message
from .models import Comment

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/success')

def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        messages.success(request, "Welcome {{ user.first_name }}")
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/success')

def success(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'user_messages': Message.objects.all().order_by("-created_at"),
        'comments': Comment.objects.all()
    }
    return render(request, 'wall.html', context)

def logoff(request):
    request.session.clear()
    return redirect('/')

def post_message(request):
    Message.objects.create(message = request.POST['message'], user = User.objects.get(id=request.session['id']))
    return redirect('/success')

def post_comment(request):
    Comment.objects.create(comment= request.POST['comment'], user = User.objects.get(id=request.session['id']), message = Message.objects.get(id=request.POST['message_id']))
    return redirect('/success')  

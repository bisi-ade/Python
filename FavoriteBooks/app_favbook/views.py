from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=request.POST['first-name'], last_name=request.POST['last-name'], email=request.POST['email'], password=pw_hash)
        user.save()
        request.session['uuid'] = user.id
        return redirect('/books/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        logged_user = user[0]
        request.session['uuid'] = logged_user.id
        return redirect('/books/')

def books(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        "logged_user": User.objects.get(id=request.session['uuid']),
        "books": Book.objects.all(),
    }
    return render(request, 'books.html', context)

def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/')
    else:
        book = Book.objects.create(
            title=request.POST['title'], description=request.POST['desc'], uploaded_by=User.objects.get(id=request.session['uuid']))
        book.liked_by.add(User.objects.get(id=request.session['uuid']))
        return redirect('/books/')

def add_to_favorite(request, book_id):
    Book.objects.get(id=book_id).liked_by.add(User.objects.get(id=request.session['uuid']))
    return redirect('/books/')

def book_info(request, book_id):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        "logged_user": User.objects.get(id=request.session['uuid']),
        "book": Book.objects.get(id=book_id)
    }
    return render(request, 'fav_books.html', context)

def update_book(request, book_id):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    else:
        Book.objects.filter(id=book_id).update(title=request.POST['title'], description=request.POST['desc'])
        return redirect('/books')

def remove_from_favorite(request, book_id):
    Book.objects.get(id=book_id).liked_by.remove(User.objects.get(id=request.session['uuid']))
    return redirect('/books')

def delete_book(request, book_id):
    print('ENTERED DELETE')
    Book.objects.get(id=book_id).delete()
    print('IS IT STILL HERE??? --->')
    return redirect('/books')

def homepage(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        "logged_user": User.objects.get(id=request.session['uuid'])
    }
    return render(request, 'home.html', context)
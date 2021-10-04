from django.shortcuts import render, redirect
from .models import User, Job, Category
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create (
                first_name= request.POST['first_name'],
                last_name= request.POST['last_name'],
                email= request.POST['email'],
                password= pw_hash,
            )
            user = User.objects.last()
            request.session['userid'] = user.id
            return redirect('/dashboard')

def login(request):
    if request.method == "POST":
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['userid'] = user.id
            return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'jobs': Job.objects.all(),
    }

    return render(request, 'dashboard.html', context)

def jobsEdit(request, id):
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'job': Job.objects.get(id=id),
        'jobs': Job.objects.all(),
    }

    return render(request, 'edit_jobs.html', context)

def jobsNew(request):
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'jobs': Job.objects.all(),
    }

    return render(request, 'add_jobs.html', context)

def jobs_info(request, id):
    if len(Category.objects.filter(jobs=Job.objects.get(id=id))) == 0:
        categories = 'None'
        lastcat = 'None'
    else:
        categories = Job.objects.get(id=id).categories.all()
        lastcat = Job.objects.get(id=id).categories.last()
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'job': Job.objects.get(id=id),
        'jobs': Job.objects.all(),
        'categories': categories,
        'lastcat': lastcat,
    }

    return render(request, 'jobs_details.html', context)

def new_job(request):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/jobs/new')
        else:
            Job.objects.create(
                title= request.POST['title'],
                location= request.POST['location'],
                description= request.POST['description'],
                made_by_user= User.objects.get(id=request.session['userid']),
            )

            for category in request.POST.getlist('categories'):
                if len(category) == 0:
                    pass
                elif len(Category.objects.filter(name=category)) == 0:
                    Category.objects.create(name=category)
                    Category.objects.last().jobs.add(Job.objects.last())
                else:
                    Category.objects.get(name=category).jobs.add(Job.objects.last())
            return redirect('/dashboard')

def edit_job(request, id):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/jobs/edit/{id}')
        else:
            job = Job.objects.get(id=id)
            job.title = request.POST['title']
            job.location = request.POST['location']
            job.description = request.POST['description']
            job.save()
            return redirect('/dashboard')

def remove_job(request, id):
    Job.objects.get(id=id).delete()
    return redirect('/dashboard')

def take_job(request, id):
    job = Job.objects.get(id=id)
    job.owned_by_user = User.objects.get(id=request.session['userid'])
    job.save()
    return redirect('/dashboard')

def give_up_job(request, id):
    job = Job.objects.get(id=id)
    job.owned_by_user = None
    job.save()
    return redirect('/dashboard')

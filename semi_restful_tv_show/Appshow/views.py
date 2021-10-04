from django.shortcuts import render, redirect
from Appshow.models import Show

# Create your views here.
def shows(request):
    context = {
        "all_shows" : Show.objects.all()
    }
    return render(request, "shows.html", context)

def new_show(request):
    return render(request, 'new.html')

def create_new_show(request):
    #add a new show to the database
    new_show = Show.objects.create(title = request.POST['title'], network = request.POST['network'], release_date=request.POST['date'], desc=request.POST['desc'])
    

    return redirect(f'/shows/{new_show.id}')

def edit(request, id):
    context = {
        "selected_show" : Show.objects.get(id=id)
    }

    return render(request, "edit.html", context)

def destroy(request, id):
    Show.objects.get(id=id).delete()

    return redirect('/')

def update(request):
    to_update = Show.objects.get(id=request.POST['id'])

    if(request.POST['title'] != ''):
        to_update.title = request.POST['title']
    if(request.POST['network'] != ''):
        to_update.network = request.POST['network']
    if(request.POST['date'] != ''):
        to_update.release_date = request.POST['date']
    if(request.POST['desc'] != ''):
        to_update.desc = request.POST['desc']
    to_update.save()

    context = {
        'selected_show' : Show.objects.get(id=request.POST['id'])
    }

    return render(request, "show.html", context)

def show(request, id):
    context = {
        "selected_show" : Show.objects.get(id = id)
    }

    return render(request, "show.html", context)


# Create your views here.

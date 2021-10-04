from app_invtmgr.models import Stock
from .forms import StockCreateForm
from django.shortcuts import render, redirect
# from models import *

# Create your views here.

def home(request):
	title = 'Welcome: This is an Inventory manager'
	context = {
	    "title": title,
	}
	return render(request, "home.html",context)


def list_item(request):
	title = 'List of Items'
	queryset = Stock.objects.all()
	context = {
		"title": title,
		"queryset": queryset,
	}
	return render(request, "list_item.html", context)

# Making items available in database

def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list_item')		#Redirect you to this page after clicking Save
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)
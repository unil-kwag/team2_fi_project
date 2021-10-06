from django.shortcuts import render
import os
# Create your views here.

def index(request):
    return render(request, 'test1/index.html',{})

def selection(request):
    return render(request, 'test1/selection.html',{})

def search(request):
    return render(request, 'test1/search.html',{})


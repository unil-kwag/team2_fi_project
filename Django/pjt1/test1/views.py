from django.shortcuts import render
import os
# Create your views here.

def index(request):
    return render(request, 'test1/index.html',{})

def selection(request):
    return render(request, 'test1/selection.html',{})

def search(request):
    return render(request, 'test1/search.html',{})

def news(request):
    return render(request, 'test1/news.html',{})

def board_main(request):
    return render(request, 'test1/board_main.html',{})

def board_write(request):
    return render(request, 'test1/board_write.html',{})    

def board_view(request):
    return render(request, 'test1/board_view.html',{})    

def board_edit(request):
    return render(request, 'test1/board_edit.html',{})    


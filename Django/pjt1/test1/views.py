from django.shortcuts import render
import os
# Create your views here.

def index(request):
    msg = "My MEssage"
    return render(request, 'test1/index.html',{'message':msg})

from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import *
from django.utils import timezone

import os
 
import pandas as pd
import json


import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from django_plotly_dash import DjangoDash
# Create your views here.

# def index(request):
#     # seoul_d = Seoul.objects.all() # ClusterData 테이블의 모든 객체 불러옴
#     # seoul_gu = seoul_d.values_list('address_gu', flat=True).distinct().order_by('-address_gu')
#     return render(request, 'test1/index.html', {'seoul_d':seoul_d})

# def index(request):
#     cursor = connection.cursor()
#     strSql = f'SELECT DISTINCT  address_gu FROM seoul'
#     result = cursor.execute(strSql)
#     search_result = cursor.fetchall()
#     connection.commit()
#     connection.close()
#     data = []
#     for i in search_result:
#         row = {'gu':i[0]}
#         data.append(row)
#     context = {'search_result1': data}
#     return render(request, 'test1/index.html', context)

def index(request):
    gu = request.GET.get('select_gu')
    kind = request.GET.get('select_kind')
    name = request.GET.get('select_name')
    cursor = connection.cursor()
    strSql = f'SELECT DISTINCT  address_gu FROM seoul'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'gu':i[0]}
        data.append(row)
    context = {}
    context['search_result1'] = data;
    if gu != None and gu != '':
        cursor = connection.cursor()
        strSql = f'SELECT DISTINCT supply_type FROM seoul WHERE address_gu = "{gu}"'
        result = cursor.execute(strSql)
        search_result = cursor.fetchall()
        connection.commit()
        connection.close()
        data = []
        for i in search_result:
            row = {'kind': i[0]}
            data.append(row)
        context['select_gu'] = gu
        context['housing_kind'] = data
        
    if kind != None and kind != '':
        cursor = connection.cursor()
        strSql = f'SELECT DISTINCT land_name FROM seoul WHERE address_gu = "{gu}" and supply_type = "{kind}"'
        result = cursor.execute(strSql)
        search_result = cursor.fetchall()
        connection.commit()
        connection.close()
        data = []
        for i in search_result:
            row = {'name': i[0]}
            data.append(row)
        context['select_kind'] = kind
        context['housing_name'] = data
        context['select_name'] = name
    return render(request, 'test1/index.html', context)



# def select_gu(request):
#     gu = request.GET.get('select_gu')
#     data = []
#     if gu != None:
#         row = {'kind': "11"}
#         data.append(row)
#         context = {'housing_kind': data}
#     else:
#         row = {'kind': "22"}
#         data.append(row)
#         context = {'housing_kind': data}
#     return render(request, 'test1/index.html', context)


##====================================================================================================================
##====================================================================================================================
## 도준 ===============================================================================================================
from .forms import Form

def selection(request):
    test = request.GET.get('name')
    return render(request, 'test1/selection.html',{'test':test})

def seoul(request):
    return render(request, 'test1/map/seoul.html',{})
def map(request):
    return render(request, 'test1/map/songpa_result.html',{})
##====================================================================================================================
##====================================================================================================================
##=================================================================================================================도준

def search(request):
    gu = request.GET.get('select_gu')
    kind = request.GET.get('select_kind')
    name = request.GET.get('select_name')
    context = {}
    context['select_gu'] = gu
    context['select_kind'] = kind
    context['select_name'] = name
    return render(request, 'test1/search.html',context)

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

def home(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'test1/home.html', {'blogs':blogs})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고 
    # 이 때, blogs 객체도 함께 넘겨주도록 하겠다.

def detail(request, blog_id): 
    blog_detail = get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    return render(request, 'test1/detail.html', {'blog':blog_detail})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고 
    # 이 때, blog 객체도 함께 넘겨주도록 하겠다.

def new(request):
    return render(request, 'test1/new.html')

def create(request):
    blog = Blog() # 객체 틀 하나 가져오기
    blog.title = request.GET['title']
    blog.writer = request.GET['writer']  # 내용 채우기
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.save() # 객체 저장하기
    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))

def edit(request,blog_id):
    blog= get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    return render(request, 'test1/edit.html', {'blog':blog})

def delete(request, blog_id):
    blog= get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    blog.delete()
    return redirect('home') # home 이름의 url 로

# U - update(기존 글 객체 가져와서 수정하기)
def update(request,blog_id):
    blog= get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    blog.title = request.GET['title']
    # blog.writer = request.GET['writer']
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.save() # 저장하기
    return redirect('/blog/' + str(blog.id))
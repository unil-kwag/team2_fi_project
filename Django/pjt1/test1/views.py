from decimal import Context
from django.shortcuts import render
from django.db import connection
from .models import *
import os
# Create your views here.

# def index(request):
#     # seoul_d = Seoul.objects.all() # ClusterData 테이블의 모든 객체 불러옴
#     # seoul_gu = seoul_d.values_list('address_gu', flat=True).distinct().order_by('-address_gu')
#     return render(request, 'test1/index.html', {'seoul_d':seoul_d})

def index(request):
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
    context = {'search_result1': data}
    return render(request, 'test1/index.html', context)

def select_gu(request):
   gu = request.GET.get('select_gu')
   if gu != None:
        cursor = connection.cursor()
        strSql = f'SELECT DISTINCT housing_type FROM seoul WHERE address_gu = "{gu}"'
        result = cursor.execute(strSql)
        search_result = cursor.fetchall()
        connection.commit()
        connection.close()
        data = []
        for i in search_result:
            row = {'kind': i[0]}
            data.append(row)
        context = {'housing_kind': data}
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

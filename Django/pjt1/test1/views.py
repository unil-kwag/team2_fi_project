
from django.shortcuts import render
from django.db import connection
from .models import *
import os

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
    app = DjangoDash('folium')    

    app.layout = html.Div(
    [
        html.Iframe(id='map',srcDoc=open('test1/ML/서울군집_지도/songpa_result.html','r').read(), width='100%', height='600')
    ])

    test = request.POST.get('test')
    # test = request.GET.values
    return render(request, 'test1/selection.html',{'request':test})
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

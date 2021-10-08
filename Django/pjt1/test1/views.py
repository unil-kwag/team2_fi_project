from django.shortcuts import render
from .models import *
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from django_plotly_dash import DjangoDash
# Create your views here.

def index(request):
    seoul_d = Seoul.objects.all() # ClusterData 테이블의 모든 객체 불러옴
    seoul_gu = seoul_d.values_list('address_gu', flat=True).distinct().order_by('-address_gu')
    return render(request, 'test1/index.html', {'seoul_d': seoul_d, 'seoul_gu': seoul_gu})

def selection(request):
    app = DjangoDash('simple')
    
    df = px.data.iris()  # iris is a pandas DataFrame
    fig = px.scatter(df, x="sepal_width", y="sepal_length")

    app.layout = html.Div(
    [
       dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i, 'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'),
        dcc.Graph(figure=fig)
    ])
    
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

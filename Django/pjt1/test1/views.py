from .forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import *
from django.utils import timezone

import os

import requests
import re
import pandas as pd
import json


import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from django_plotly_dash import DjangoDash

import pandas as pd
import numpy as np
import folium
import folium.plugins as plugins
import json
from haversine import haversine

# Create your views here.



# ====================================================================================================================
# 도영 ===============================================================================================================
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
        row = {'gu': i[0]}
        data.append(row)
    context = {}
    context['search_result1'] = data
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

def search(request):
    gu = request.GET.get('select_gu')
    print(gu)
    kind = request.GET.get('select_kind')
    name = request.GET.get('select_name')
    context = {}
    context['select_gu'] = gu
    context['select_kind'] = kind
    context['select_name'] = name
# 아파트 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, land_name, longitude, latitude FROM cluster_data WHERE land_name = "{name}"'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'apt_name' : i[1], 'apt_lon' : i[2], 'apt_lat' : i[3]}
        data.append(row)
    context['select_apt'] = data
    apt_df = pd.DataFrame(context['select_apt'])
# 버스 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM bus'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'bus_name' : i[1], 'bus_lon' : i[2], 'bus_lat' : i[3]}
        data.append(row)
    context['all_bus'] = data
    bus_df = pd.DataFrame(context['all_bus'])
# 어린이집 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM care'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'care_name' : i[1], 'care_lon' : i[2], 'care_lat' : i[3]}
        data.append(row)
    context['all_care'] = data
    care_df = pd.DataFrame(context['all_care'])
# 편의점 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM convenience'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'convenience_name' : i[0], 'convenience_lon' : i[1], 'convenience_lat' : i[2]}
        data.append(row)
    context['all_convenience'] = data
    convenience_df = pd.DataFrame(context['all_convenience'])
# 백화점 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM depart'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'depart_name' : i[0], 'depart_lon' : i[1], 'depart_lat' : i[2]}
        data.append(row)
    context['all_depart'] = data
    depart_df = pd.DataFrame(context['all_depart'])
# 소방서 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, name, longitude, latitude FROM fire'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'fire_name' : i[1], 'fire_lon' : i[2], 'fire_lat' : i[3]}
        data.append(row)
    context['all_fire'] = data
    fire_df = pd.DataFrame(context['all_fire'])
# 병원 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM hospital'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'hospital_name' : i[1], 'hospital_lon' : i[2], 'hospital_lat' : i[3]}
        data.append(row)
    context['all_hospital'] = data
    hospital_df = pd.DataFrame(context['all_hospital'])
# 유치원 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, edu_name, longitude, latitude FROM kinder'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'kinder_name' : i[1], 'kinder_lon' : i[2], 'kinder_lat' : i[3]}
        data.append(row)
    context['all_kinder'] = data
    kinder_df = pd.DataFrame(context['all_kinder'])
# 주차장 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM parking'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'parking_name' : i[0], 'parking_lon' : i[1], 'parking_lat' : i[2]}
        data.append(row)
    context['all_parking'] = data
    parking_df = pd.DataFrame(context['all_parking'])    
# 약국 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, name, longitude, latitude FROM pharmacy'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'pharmacy_name' : i[1], 'pharmacy_lon' : i[2], 'pharmacy_lat' : i[3]}
        data.append(row)
    context['all_pharmacy'] = data
    pharmacy_df = pd.DataFrame(context['all_pharmacy'])    
# 경찰서 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, police_station, longitude, latitude FROM police'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'police_name' : i[1], 'police_lon' : i[2], 'police_lat' : i[3]}
        data.append(row)
    context['all_police'] = data
    police_df = pd.DataFrame(context['all_police'])    
# 우체국 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM post'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'post_name' : i[0], 'post_lon' : i[1], 'post_lat' : i[2]}
        data.append(row)
    context['all_post'] = data
    post_df = pd.DataFrame(context['all_post'])    
# 학교 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM school'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'school_name' : i[1], 'school_lon' : i[2], 'school_lat' : i[3]}
        data.append(row)
    context['all_school'] = data
    school_df = pd.DataFrame(context['all_school'])    
# 상점 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, small_category, longitude, latitude FROM store'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'store_name' : i[1], 'store_lon' : i[2], 'store_lat' : i[3]}
        data.append(row)
    context['all_store'] = data
    store_df = pd.DataFrame(context['all_store'])        
# 지하철 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, station_num, longitude, latitude FROM subway'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'subway_name' : i[1], 'subway_lon' : i[2], 'subway_lat' : i[3]}
        data.append(row)
    context['all_subway'] = data
    subway_df = pd.DataFrame(context['all_subway'])        
# 아파트-버스 1km 필터---------------------------------------
    make_distance = pd.DataFrame()
    for i in range(len(bus_df)):
        distance = haversine( tuple(apt_df.iloc[0, 1:]), tuple(bus_df.iloc[:, 1:].values[i]), unit = 'km')
        if distance <= 1:
            one_k = {
                'apt_name' : apt_df.iloc[0, 0],
                'bus_name' : bus_df.iloc[:, 0].values[i],
                'bus_lon' : bus_df.iloc[:, 1].values[i],
                'bus_lat' : bus_df.iloc[:, 2].values[i]
            }
            make_distance = make_distance.append(one_k, ignore_index=True)
    lat = apt_df.iloc[0, 2]
    lon = apt_df.iloc[0, 1]
    name = apt_df.iloc[0, 0]
    map = folium.Map(location = [lat, lon], zoom_start=14)
    folium.Marker( [lat, lon],
                  icon = (folium.Icon(icon='home', prefix='fa', color='green')),
                  tooltip = name
    ).add_to(map)
    folium.Circle( [lat, lon],
                    radius = 1000, popup = '편의시설 범위'
    ).add_to(map)
    maps=map._repr_html_()
    return render(request, 'test1/search.html',{'map' : maps})

# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================
# 도준 ===============================================================================================================


def selection(request):
    test = request.GET.get('name')
    return render(request, 'test1/selection.html', {'test': test})


def seoul(request):
    return render(request, 'test1/map/seoul.html', {})


def map(request):
    return render(request, 'test1/map/songpa_result.html', {})
# ====================================================================================================================
# ====================================================================================================================
# =================================================================================================================도준


def news(request):
    return render(request, 'test1/news.html', {})


def board_main(request):
    return render(request, 'test1/board_main.html', {})


def board_write(request):
    return render(request, 'test1/board_write.html', {})


def board_view(request):
    return render(request, 'test1/board_view.html', {})


def board_edit(request):
    return render(request, 'test1/board_edit.html', {})


def home(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'test1/home.html', {'blogs': blogs})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고
    # 이 때, blogs 객체도 함께 넘겨주도록 하겠다.


def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    return render(request, 'test1/detail.html', {'blog': blog_detail})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고
    # 이 때, blog 객체도 함께 넘겨주도록 하겠다.


def new(request):
    return render(request, 'test1/new.html')


def create(request):
    blog = Blog()  # 객체 틀 하나 가져오기
    blog.title = request.GET['title']
    blog.writer = request.GET['writer']  # 내용 채우기
    blog.body = request.GET['body']  # 내용 채우기
    blog.pub_date = timezone.datetime.now()  # 내용 채우기
    blog.save()  # 객체 저장하기
    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))


def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    return render(request, 'test1/edit.html', {'blog': blog})


def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    blog.delete()
    return redirect('home')  # home 이름의 url 로

# U - update(기존 글 객체 가져와서 수정하기)


def update(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    blog.title = request.GET['title']
    # blog.writer = request.GET['writer']
    blog.body = request.GET['body']  # 내용 채우기
    blog.pub_date = timezone.datetime.now()  # 내용 채우기
    blog.save()  # 저장하기
    return redirect('/blog/' + str(blog.id))


def news(request):
    search = request.GET.get('search')
    page = request.GET.get('page')

    client_id = "6HlcFx6Fi1uXNPCW7pmG"
    client_secret = "6Hx6DIiFP_"

    encode_type = 'json'  # 출력 방식 json 또는 xml
    max_display = 5  # 출력 뉴스 수
    sort = 'date'  # 결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1  # 출력 위치

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

    # 헤더에 아이디와 키 정보 넣기
    headers = {'X-Naver-Client-Id': client_id,
               'X-Naver-Client-Secret': client_secret
               }

    # HTTP요청 보내기
    r = requests.get(url, headers=headers)
    return render(request, 'test1/news.html', {'result': r.json()})

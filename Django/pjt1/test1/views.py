from .forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import *
from django.utils import timezone

import os

import requests
import re

import pandas as pd
import folium
import json
from sklearn.ensemble import RandomForestClassifier  # RandomForest 모델
from sklearn.model_selection import GridSearchCV  # 파라미터 최적화를 위한 GridSearchCV


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

# ====================================================================================================================
# ====================================================================================================================
# 도준 ===============================================================================================================


def selection(request):
    test = request.GET.get('name')
    return render(request, 'test1/selection.html', {'test': test})


def test(request):
    geo_path = './test1/templates/test1/map/seoul_municipalities_geo.json'
    seoul = json.load(open(geo_path, encoding='utf-8'))
    kmeans_final_score = pd.read_csv(
        './test1/templates/test1/map/군집결과_입지점수계산.csv', encoding='cp949')  # 모델학습용 파일
    X = kmeans_final_score.iloc[:, 1:-1]  # 독립변수 X 분리
    y = kmeans_final_score.iloc[:, [-1]]  # 종속변수 Y 분리
    songpa = pd.read_csv('./test1/templates/test1/map/송파구_거리계산결과.csv',
                         encoding='cp949')  # 송파 군집 csv 파일 불러오기 송파구 입지선정용

    Model = RandomForestClassifier(random_state=40)  # RandomForest 객체 생성
    params = {'max_depth': [4], 'n_estimators': [30]}
    grid_dt = GridSearchCV(Model,  # estimator 객체,
                           param_grid=params,
                           cv=5)  # 교차횟수 5회
    grid_dt.fit(X, y)  # 모델 학습
    songpa_predict = grid_dt.predict(songpa.iloc[:, 3:])  # 모델 예측
    songpa_result = pd.concat([songpa.iloc[:, :3], pd.DataFrame(
        songpa_predict, columns=['입지점수'])], axis=1)  # 송파구 데이터프레임의 입지점수 concat

    lat = 37.508182
    lon = 127.110053
    map = folium.Map(location=[lat, lon], zoom_start=14)
    for i in range(len(songpa_result)):
        lat = songpa_result.loc[i, '위도']
        lng = songpa_result.loc[i, '경도']

        if songpa_result.loc[i, '입지점수'] == 1:  # 입지점수가 1이면 초록으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='green')),).add_to(map)
        elif songpa_result.loc[i, '입지점수'] == 2:  # 입지점수가 2이면 빨강으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='red')),).add_to(map)
        elif songpa_result.loc[i, '입지점수'] == 3:  # 입지점수가 3이면 보라로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='purple')),).add_to(map)
        elif songpa_result.loc[i, '입지점수'] == 4:  # 입지점수가 2이면 빨강으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='orange')),).add_to(map)
        elif songpa_result.loc[i, '입지점수'] == 0:  # 입지점수가 2이면 빨강으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='blue')),).add_to(map)
        else:
            continue

    if request.GET.get('name') == 'dojun':
        folium.Marker([lat, lon], icon=(folium.Icon(
            icon='home', prefix='fa', color='black')),).add_to(map)

    map.choropleth(geo_data=seoul, fill_color='white')
    map = map._repr_html_()
    # test = request.GET.get('name')

    return render(request, 'test1/test.html', {'test': songpa_result, 'test2': map})


def seoul(request):
    return render(request, 'test1/map/seoul.html', {})


def map(request):
    return render(request, 'test1/map/songpa_result.html', {})
# ====================================================================================================================
# ====================================================================================================================
# =================================================================================================================도준


def search(request):
    gu = request.GET.get('select_gu')
    kind = request.GET.get('select_kind')
    name = request.GET.get('select_name')
    context = {}
    context['select_gu'] = gu
    context['select_kind'] = kind
    context['select_name'] = name
    return render(request, 'test1/search.html', context)


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


def clean_html(x):
    x = re.sub("\&\w*\;", "", x)
    x = re.sub("<.*?>", "", x)
    return x


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
    result = []
    for i in r.json()['items']:
        tmp_dic = {'title': clean_html(i['title']),
                   'originallink': i['originallink'],
                   'link': i['link'],
                   'description': clean_html(i['description']),
                   'pubDate': i['pubDate']}
        result.append(tmp_dic)
    return render(request, 'test1/news.html', {'result': result})

from .forms import Form
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import *
from django.utils import timezone
from django.views.generic import TemplateView
from plotly.offline import plot
import plotly.graph_objects as go
from django.core.paginator import Paginator

import os

import requests
import re
import numpy as np
import pandas as pd
import folium
import json
from sklearn.ensemble import RandomForestClassifier  # RandomForest 모델
from sklearn.model_selection import GridSearchCV  # 파라미터 최적화를 위한 GridSearchCV


import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from django_plotly_dash import DjangoDash

import pandas as pd
import folium
import folium.plugins as plugins
import json
from haversine import haversine

import random  # 랜덤 뉴스
# Create your views here.


# ====================================================================================================================
# 도영 ===============================================================================================================
def make_distance(apt_df, bus_df, bus_distance, name, lon, lat):
    bus_distance = pd.DataFrame()
    for i in range(len(bus_df)):
        distance = haversine(tuple(apt_df.iloc[0, 1:]),
                             tuple(bus_df.iloc[:, 1:].values[i]), unit='km')
        if distance <= 1:
            one_k = {
                'apt_name': apt_df.iloc[0, 0],
                name: bus_df.iloc[:, 0].values[i],
                lon: bus_df.iloc[:, 1].values[i],
                lat: bus_df.iloc[:, 2].values[i]
            }
            bus_distance = bus_distance.append(one_k, ignore_index=True)
    return bus_distance

# def make_map(bus_distance, bus_lat, bus_lon, bus, bus_name, g1):
#         for i in range( len(bus_distance)):
#             lat = bus_distance.loc[i, bus_lat]
#             lon = bus_distance.loc[i, bus_lon]
#             folium.Marker([lat, lon],
#                         icon = (folium.Icon(icon=bus, prefix='fa', color='red')),
#                         tooltip = bus_distance.loc[i, bus_name]).add_to(g1)


def index_option2(request):
    supply_type = Seoul.objects.filter(address_gu=request.GET.get(
        'select_gu')).values('supply_type').distinct()
    return render(request, 'test1/index_option2.html', {'supply_type': supply_type})


def index_option3(request):
    land_name = Seoul.objects.filter(supply_type=request.GET.get(
        'select_kind'), address_gu=request.GET.get('select_gu')).values('land_name').distinct()
    return render(request, 'test1/index_option3.html', {'land_name': land_name})


def index(request):
    ###seoul = Seoul.objects.all().values('address_gu','supply_type','land_name').distinct() ####################
    seoul = Seoul.objects.values('address_gu').distinct()

    search = '서울 부동산'
    page = request.GET.get('page')

    client_id = "6HlcFx6Fi1uXNPCW7pmG"
    client_secret = "6Hx6DIiFP_"

    encode_type = 'json'  # 출력 방식 json 또는 xml
    max_display = 2  # 출력 뉴스 수
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
    # 게시판 제목을 index.html에 주기
    jemok = Blog.objects.all().order_by('-id')
    notice = NoticeBlog.objects.all().order_by('-id')

    return render(request, 'test1/index.html', {'result': result, 'jemok': jemok, 'notice': notice, 'seoul': seoul})


def search(request):
    gu = request.GET.get('select_gu')
    kind = request.GET.get('select_kind')
    name = request.GET.get('select_name')
    context = {}
    context['select_gu'] = gu
    context['select_kind'] = kind
    context['select_name'] = name
# 아파트 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT land_name, longitude, latitude FROM seoul WHERE land_name = "{name}" and supply_type = "{kind}"'
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'apt_name': i[0], 'apt_lon': i[1], 'apt_lat': i[2]}
        try:
            row = {'apt_name': i[0],
                   'apt_lon': float(i[1]), 'apt_lat': float(i[2].replace(r'\r', ''))}
            data.append(row)
        except:
            pass
    context['select_apt'] = data
    apt_df = pd.DataFrame(context['select_apt'])
    APT_LON_prev = apt_df['apt_lon'][0]-0.01
    APT_LON_next = apt_df['apt_lon'][0]+0.01
    APT_LAT_prev = apt_df['apt_lat'][0]-0.015
    APT_LAT_next = apt_df['apt_lat'][0]+0.015

# 버스 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM bus WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'bus_name': i[1], 'bus_lon': i[2], 'bus_lat': i[3]}
        data.append(row)
    context['all_bus'] = data
    bus_df = pd.DataFrame(context['all_bus'])
# 어린이집 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM care WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'care_name': i[1], 'care_lon': i[2],
               'care_lat': float(i[3].replace('\r', ''))}
        data.append(row)
    context['all_care'] = data
    care_df = pd.DataFrame(context['all_care'])
# 편의점 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM convenience WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'convenience_name': i[0],
               'convenience_lon': i[1], 'convenience_lat': float(i[2].replace('\r', ''))}
        data.append(row)
    context['all_convenience'] = data
    convenience_df = pd.DataFrame(context['all_convenience'])
# 백화점 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM depart WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'depart_name': i[0], 'depart_lon': i[1],
               'depart_lat': float(i[2].replace('\r', ''))}
        data.append(row)
    context['all_depart'] = data
    depart_df = pd.DataFrame(context['all_depart'])
# 소방서 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, name, longitude, latitude FROM fire WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'fire_name': i[1], 'fire_lon': i[2],
               'fire_lat': float(i[3].replace('\r', ''))}
        data.append(row)
    context['all_fire'] = data
    fire_df = pd.DataFrame(context['all_fire'])
# 병원 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM hospital WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        try:
            row = {'hospital_name': i[1],
                   'hospital_lon': float(i[2]), 'hospital_lat': float(i[3].replace(r'\r', ''))}
            data.append(row)
        except:
            pass
    context['all_hospital'] = data
    hospital_df = pd.DataFrame(context['all_hospital'])
# 유치원 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, edu_name, longitude, latitude FROM kinder WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'kinder_name': i[1], 'kinder_lon': i[2],
               'kinder_lat': float(i[3].replace('\r', ''))}
        data.append(row)
    context['all_kinder'] = data
    kinder_df = pd.DataFrame(context['all_kinder'])
# 주차장 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM parking WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'parking_name': i[0], 'parking_lon': i[1],
               'parking_lat': float(i[2].replace('\r', ''))}
        data.append(row)
    context['all_parking'] = data
    parking_df = pd.DataFrame(context['all_parking'])
# 약국 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, name, longitude, latitude FROM pharmacy WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        try:
            row = {'pharmacy_name': i[1],
                   'pharmacy_lon': float(i[2]), 'pharmacy_lat': float(i[3].replace('\r', ''))}
            data.append(row)
        except:
            pass
    context['all_pharmacy'] = data
    pharmacy_df = pd.DataFrame(context['all_pharmacy'])
# 경찰서 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, police_station, longitude, latitude FROM police WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'police_name': i[1], 'police_lon': i[2], 'police_lat': i[3]}
        data.append(row)
    context['all_police'] = data
    police_df = pd.DataFrame(context['all_police'])
# 우체국 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT  id, longitude, latitude FROM post WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'post_name': i[0], 'post_lon': i[1],
               'post_lat': float(i[2].replace('\r', ''))}
        data.append(row)
    context['all_post'] = data
    post_df = pd.DataFrame(context['all_post'])
# 학교 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, name, longitude, latitude FROM school WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'school_name': i[1], 'school_lon': i[2],
               'school_lat': float(i[3].replace('\r', ''))}
        data.append(row)
    context['all_school'] = data
    school_df = pd.DataFrame(context['all_school'])
# 전통시장 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, store_name, longitude, latitude FROM store WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'store_name': i[1], 'store_lon': i[2],
               'store_lat': float(i[3].replace('\r', ''))}
        data.append(row)
    context['all_store'] = data
    store_df = pd.DataFrame(context['all_store'])
# 지하철 데이터 불러오기---------------------------------------
    cursor = connection.cursor()
    strSql = f'SELECT  DISTINCT id, station_num, longitude, latitude FROM subway WHERE longitude <=' + str(APT_LON_next) +' AND longitude >=' + str(APT_LON_prev) + ' AND latitude <= '+ str(APT_LAT_next) + ' AND latitude >= '+ str(APT_LAT_prev)
    result = cursor.execute(strSql)
    search_result = cursor.fetchall()
    connection.commit()
    connection.close()
    data = []
    for i in search_result:
        row = {'subway_name': i[1], 'subway_lon': i[2],
               'subway_lat': float(i[3].replace('\r', ''))}
        data.append(row)
    context['all_subway'] = data
    subway_df = pd.DataFrame(context['all_subway'])
# 아파트 1km 필터---------------------------------------
    # bus_distance = make_distance(
    #     apt_df, bus_df, 'bus_distance', 'bus_name', 'bus_lon', 'bus_lat')
    # care_distance = make_distance(
    #     apt_df, care_df, 'care_distance', 'care_name', 'care_lon', 'care_lat')
    # convenience_distance = make_distance(
    #     apt_df, convenience_df, 'convenience_distance', 'convenience_name', 'convenience_lon', 'convenience_lat')
    # depart_distance = make_distance(
    #     apt_df, convenience_df, 'depart_distance', 'depart_name', 'depart_lon', 'depart_lat')
    # fire_distance = make_distance(
    #     apt_df, fire_df, 'fire_distance', 'fire_name', 'fire_lon', 'fire_lat')
    # hospital_distance = make_distance(
    #     apt_df, hospital_df, 'hospital_distance', 'hospital_name', 'hospital_lon', 'hospital_lat')
    # kinder_distance = make_distance(
    #     apt_df, kinder_df, 'kinder_distance', 'kinder_name', 'kinder_lon', 'kinder_lat')
    # parking_distance = make_distance(
    #     apt_df, parking_df, 'parking_distance', 'parking_name', 'parking_lon', 'parking_lat')
    # pharmacy_distance = make_distance(
    #     apt_df, pharmacy_df, 'pharmacy_distance', 'pharmacy_name', 'pharmacy_lon', 'pharmacy_lat')
    # police_distance = make_distance(
    #     apt_df, police_df, 'police_distance', 'police_name', 'police_lon', 'police_lat')
    # post_distance = make_distance(
    #     apt_df, post_df, 'post_distance', 'post_name', 'post_lon', 'post_lat')
    # school_distance = make_distance(
    #     apt_df, school_df, 'school_distance', 'school_name', 'school_lon', 'school_lat')
    # store_distance = make_distance(
    #     apt_df, store_df, 'store_distance', 'store_name', 'store_lon', 'store_lat')
    # subway_distance = make_distance(
    #     apt_df, subway_df, 'subway_distance', 'subway_name', 'subway_lon', 'subway_lat')
    lat = apt_df.iloc[0, 2]
    lon = apt_df.iloc[0, 1]
    name = apt_df.iloc[0, 0]
    map = folium.Map(location=[lat, lon], zoom_start=14)
    g1 = folium.FeatureGroup(name='버스 정류장')
    g2 = folium.FeatureGroup(name='어린이집')
    g3 = folium.FeatureGroup(name='편의점')
    g4 = folium.FeatureGroup(name='백화점')
    g5 = folium.FeatureGroup(name='소방서')
    g6 = folium.FeatureGroup(name='병원')
    g7 = folium.FeatureGroup(name='유치원')
    g8 = folium.FeatureGroup(name='주차장')
    g9 = folium.FeatureGroup(name='약국')
    g10 = folium.FeatureGroup(name='경찰서')
    g11 = folium.FeatureGroup(name='우체국')
    g12 = folium.FeatureGroup(name='학교')
    g13 = folium.FeatureGroup(name='전통시장')
    g14 = folium.FeatureGroup(name='지하철')
    g_category = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14]
    for i in g_category:
        map.add_child(i)
    folium.LayerControl().add_to(map)
    folium.Marker([lat, lon],
                  icon=(folium.Icon(icon='home', prefix='fa', color='green')),
                  tooltip=name
                  ).add_to(map)
    folium.Circle([lat, lon],
                  radius=1500, popup='편의시설 범위', color='grey', fill_color=1
                  ).add_to(map)
    for i in range(len(bus_df)):
        lat = bus_df.loc[i, 'bus_lat']
        lon = bus_df.loc[i, 'bus_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='bus', prefix='fa', color='red')),
                      tooltip=bus_df.loc[i, 'bus_name']).add_to(g1)
    for i in range(len(care_df)):
        lat = care_df.loc[i, 'care_lat']
        lon = care_df.loc[i, 'care_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='child', prefix='fa', color='blue')),
                      tooltip=care_df.loc[i, 'care_name']).add_to(g2)
    for i in range(len(convenience_df)):
        lat = convenience_df.loc[i, 'convenience_lat']
        lon = convenience_df.loc[i, 'convenience_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='green')),
                      tooltip='편의점').add_to(g3)
    for i in range(len(depart_df)):
        lat = depart_df.loc[i, 'depart_lat']
        lon = depart_df.loc[i, 'depart_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='purple')),
                      tooltip='백화점').add_to(g4)
    for i in range(len(fire_df)):
        lat = fire_df.loc[i, 'fire_lat']
        lon = fire_df.loc[i, 'fire_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='orange')),
                      tooltip=fire_df.loc[i, 'fire_name']).add_to(g5)
    for i in range(len(hospital_df)):
        lat = hospital_df.loc[i, 'hospital_lat']
        lon = hospital_df.loc[i, 'hospital_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='darkred')),
                      tooltip=hospital_df.loc[i, 'hospital_name']).add_to(g6)
    for i in range(len(kinder_df)):
        lat = kinder_df.loc[i, 'kinder_lat']
        lon = kinder_df.loc[i, 'kinder_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='child',
                            prefix='fa', color='lightred')),
                      tooltip=kinder_df.loc[i, 'kinder_name']).add_to(g7)
    for i in range(len(parking_df)):
        lat = parking_df.loc[i, 'parking_lat']
        lon = parking_df.loc[i, 'parking_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='lightred')),
                      tooltip='주차장').add_to(g8)
    for i in range(len(pharmacy_df)):
        lat = pharmacy_df.loc[i, 'pharmacy_lat']
        lon = pharmacy_df.loc[i, 'pharmacy_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='beige')),
                      tooltip=pharmacy_df.loc[i, 'pharmacy_name']).add_to(g9)
    for i in range(len(police_df)):
        lat = police_df.loc[i, 'police_lat']
        lon = police_df.loc[i, 'police_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='darkblue')),
                      tooltip=police_df.loc[i, 'police_name']).add_to(g10)
    for i in range(len(post_df)):
        lat = post_df.loc[i, 'post_lat']
        lon = post_df.loc[i, 'post_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='darkgreen')),
                      tooltip=post_df.loc[i, 'post_name']).add_to(g11)
    for i in range(len(school_df)):
        lat = school_df.loc[i, 'school_lat']
        lon = school_df.loc[i, 'school_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='cadetblue')),
                      tooltip=school_df.loc[i, 'school_name']).add_to(g12)
    for i in range(len(store_df)):
        lat = store_df.loc[i, 'store_lat']
        lon = store_df.loc[i, 'store_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='darkpurple')),
                      tooltip=store_df.loc[i, 'store_name']).add_to(g13)
    for i in range(len(subway_df)):
        lat = subway_df.loc[i, 'subway_lat']
        lon = subway_df.loc[i, 'subway_lon']
        folium.Marker([lat, lon],
                      icon=(folium.Icon(icon='building',
                            prefix='fa', color='pink')),
                      tooltip=ssubway_df.loc[i, 'subway_name']).add_to(g14)
    maps = map._repr_html_()
    context['map'] = maps
# 막대그래프 만들기
    fig = go.Figure(
        go.Bar(
            y=['버스 정류장', '어린이집', '편의점', '백화점', '소방서', '병원', '유치원',
                '주차장', '약국', '경찰서', '우체국', '학교', '전통시장', '지하철'],
            x=[len(bus_df), len(care_df), len(convenience_df), len(depart_df), len(fire_df), len(hospital_df), len(kinder_df), len(
                parking_df), len(pharmacy_df), len(police_df), len(post_df), len(school_df), len(store_df), len(subway_df)],
            orientation='h',
            marker=dict(
                color='rgba(253, 198, 0, 1.0)',
                line=dict(color='rgba(253, 198, 0, 1.0)', width=3)
            )
        ))
    # layout = {
    # 'title': 'Title of the figure',
    # 'xaxis_title': 'X',
    # 'yaxis_title': 'Y',
    # 'height': 1000,
    # 'width': 1000,
    # }
    bar_chart = plot({'data': fig}, output_type='div')
    context['bar_chart'] = bar_chart
# 레이더차트 그리기
    group1 = [len(bus_df), len(subway_df)]
    group2 = [len(post_df), len(
        convenience_df), len(store_df)]
    group3 = [len(care_df), len(kinder_df), len(school_df)]
    # df = pd.DataFrame(dict(
    # r=[np.mean(group1), np.mean(group2), np.mean(group3)],
    # theta=['편의시설', '교육시설', '기피시설']))
    # fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    # layout = {
    # 'title': 'Title of the figure',
    # 'height': 420,
    # 'width': 560,
    # }
    fig = go.Figure(data=go.Scatterpolar(
        r=[np.mean(group1), np.mean(group2), np.mean(group3)],
        theta=['교통입지', '편의입지', '교육입지'],
        fill='toself',
        line_color='rgba(253, 198, 0, 1.0)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )
    radar_chart = plot({'data': fig}, output_type='div')
    context['radar_chart'] = radar_chart
    return render(request, 'test1/search.html', context)

# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================
# 도준 ===============================================================================================================


def selection(request):
    test = request.GET.get('name')
    return render(request, 'test1/selection.html', {'test': test})


def test(request):
    feature1 = request.GET.get('feature1')+' 평균거리'
    feature2 = request.GET.get('feature2')+' 평균거리'
    feature3 = request.GET.get('feature3')+' 평균거리'
    location_name = request.GET.get('location_features_name')
    print(location_name)
    geo_path = './test1/templates/test1/map/seoul_municipalities_geo.json'
    seoul = json.load(open(geo_path, encoding='utf-8'))

    kmeans_final_score = pd.read_csv(
        './test1/templates/test1/map/군집결과_입지점수계산.csv', encoding='cp949')  # 모델학습용 파일
    # X = kmeans_final_score.iloc[:, 1:-1]  # 독립변수 X 분리
    X2 = kmeans_final_score.loc[:, [feature1, feature2, feature3]]
    y = kmeans_final_score.iloc[:, [-1]]  # 종속변수 Y 분리

    seoul_result = pd.read_csv(
        './test1/templates/test1/map/서울전역_결과.csv', encoding='cp949')

    # songpa = pd.read_csv('./test1/templates/test1/map/송파구_거리계산결과.csv',
    #                      encoding='cp949')  # 송파 군집 csv 파일 불러오기 송파구 입지선정용
    # print("SONGPA :", songpa)

    Model = RandomForestClassifier(random_state=40)  # RandomForest 객체 생성
    params = {'max_depth': [4], 'n_estimators': [30]}
    grid_dt = GridSearchCV(Model,  # estimator 객체,
                           param_grid=params,
                           cv=5)  # 교차횟수 5회
    grid_dt.fit(X2, y)  # 모델 학습
    seoul_predict = grid_dt.predict(seoul_result.loc[seoul_result['시군구'] == location_name].loc[:, [
                                    feature1, feature2, feature3]])  # 서울 모델 예측
    seoul_location = seoul_result.loc[seoul_result['시군구'] ==
                                      location_name].iloc[:, :4].reset_index()  # 인덱스를 리셋해주기 위함
    seoul_location = seoul_location[['주소', '위도', '경도', '시군구']]
    seoul_predict_result = pd.concat([seoul_location, pd.DataFrame(
        seoul_predict, columns=['입지점수'])], axis=1)  # 서울 데이터프레임의 입지점수 concat

    # songpa_predict = grid_dt.predict(songpa.loc[:, [feature1, feature2, feature3]])  # 모델 예측
    # songpa_result = pd.concat([songpa.iloc[:, :3], pd.DataFrame(songpa_predict, columns=['입지점수'])], axis=1)  # 송파구 데이터프레임의 입지점수 concat
    # if location_name == '강남구' :
    #     latt = 561561
    #     lonn = 165156
    # elif location_name =='도봉구':
    #     latt = 37.657891
    #     lonn = 127.039005
    latt = 37.508182
    lonn = 127.110053
    map = folium.Map(location=[latt, lonn], zoom_start=14)
    for i in range(len(seoul_predict_result)):
        lat = seoul_predict_result.loc[i, '위도']
        lng = seoul_predict_result.loc[i, '경도']
        if seoul_predict_result.loc[i, '입지점수'] == 1:  # 입지점수가 1이면 초록으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='green')),).add_to(map)
        elif seoul_predict_result.loc[i, '입지점수'] == 2:  # 입지점수가 2이면 빨강으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='red')),).add_to(map)
        elif seoul_predict_result.loc[i, '입지점수'] == 3:  # 입지점수가 3이면 보라로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='purple')),).add_to(map)
        elif seoul_predict_result.loc[i, '입지점수'] == 4:  # 입지점수가 2이면 빨강으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='orange')),).add_to(map)
        elif seoul_predict_result.loc[i, '입지점수'] == 0:  # 입지점수가 2이면 파랑으로 마커 지정
            folium.Marker([lat, lng], icon=(folium.Icon(
                icon='home', prefix='fa', color='blue')),).add_to(map)
        else:
            continue

    map.choropleth(geo_data=seoul, fill_color='white')
    map = map._repr_html_()

    return render(request, 'test1/test.html', {'map': map, 'feature1': feature1, 'feature2': feature2, 'feature3': feature3})


def seoul(request):
    return render(request, 'test1/map/seoul.html', {})


def dobong(request):
    return render(request, 'test1/map/dobong_result.html')


def songpa(request):
    return render(request, 'test1/map/songpa_result.html', {})


def dongdaemoon(request):
    return render(request, 'test1/map/dongdaemoon_result.html')


def dongjak(request):
    return render(request, 'test1/map/dongjak_result.html')


def eunpyeong(request):
    return render(request, 'test1/map/eunpyeong_result.html')


def gangbook(request):
    return render(request, 'test1/map/gangbook_result.html')


def gangdong(request):
    return render(request, 'test1/map/gangdong_result.html')


def gangnam(request):
    return render(request, 'test1/map/gangnam_result.html')


def gangseo(request):
    return render(request, 'test1/map/gangseo_result.html')


def geumcheon(request):
    return render(request, 'test1/map/geumcheon_result.html')


def guro(request):
    return render(request, 'test1/map/guro_result.html')


def gwanak(request):
    return render(request, 'test1/map/gwanak_result.html')


def gwangjin(request):
    return render(request, 'test1/map/gwangjin_result.html')


def jongro(request):
    return render(request, 'test1/map/jongro_result.html')


def joong(request):
    return render(request, 'test1/map/joong_result.html')


def joongrang(request):
    return render(request, 'test1/map/joongrang_result.html')


def mapo(request):
    return render(request, 'test1/map/mapo_result.html')


def noone(request):
    return render(request, 'test1/map/noone_result.html')


def seocho(request):
    return render(request, 'test1/map/seocho_result.html')


def seodaemoon(request):
    return render(request, 'test1/map/seodaemoon_result.html')


def seongbook(request):
    return render(request, 'test1/map/seongbook_result.html')


def seongdong(request):
    return render(request, 'test1/map/seongdong_result.html')


def yangcheon(request):
    return render(request, 'test1/map/yangcheon_result.html')


def yeongdeung(request):
    return render(request, 'test1/map/yeongdeung_result.html')


def yongsan(request):
    return render(request, 'test1/map/yongsan_result.html')
# ====================================================================================================================
# ====================================================================================================================
# =================================================================================================================도준


def blog(request):
    notice = NoticeBlog.objects.all().order_by('-id')[:5]

    all_blog = Blog.objects.all().order_by('-id')
    paginator = Paginator(all_blog, 10)
    page = int(request.GET.get('page', 1))
    blog_list = paginator.get_page(page)

    return render(request, 'test1/home.html', {'blog_list': blog_list, 'notices': notice})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고
    # 이 때, blogs 객체도 함께 넘겨주도록 하겠다.


def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    blog_comment = Commet.objects.filter(blog_id=blog_id)
    # 조회수 증가
    pk = blog_id
    cursor = connection.cursor()
    strsql = "UPDATE Blog SET hit = hit+1 WHERE id="+str(pk)
    result = cursor.execute(strsql)
    blog = cursor.fetchall()
    connection.commit()
    connection.close()

    return render(request, 'test1/detail.html', {'blog': blog_detail, 'comment': blog_comment})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고
    # 이 때, blog 객체도 함께 넘겨주도록 하겠다.


def comment_insert(request, blog_id):
    comment = Commet()
    comment.body = request.GET['comment_body']
    comment.name = request.GET['user_name']  # id로 수정
    comment.date = timezone.datetime.now()  # 현재시간 등록
    comment.blog_id = blog_id
    comment.save()
    return redirect('/detail/'+str(blog_id))


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
    return redirect('/blog/')


def notice_create(request):
    notice = NoticeBlog()
    notice.title = request.GET['title']
    notice.name = '관리자'
    notice.body = request.GET['body']
    notice.date = timezone.datetime.now()
    notice.save()

    return redirect('/blog/')


def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)

    return render(request, 'test1/edit.html', {'blog': blog})


def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    comment = Commet.objects.filter(blog_id=blog_id)
    comment.delete()
    blog.delete()
    return redirect('/blog/')  # home 이름의 url 로


def notice_delete(request, notice_id):
    notice = get_object_or_404(NoticeBlog, pk=notice_id)
    notice.delete()
    return redirect('/blog/')


def update(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)  # 특정 객체 가져오기(없으면 404 에러)
    blog.title = request.GET['title']
    blog.body = request.GET['body']  # 내용 채우기
    blog.pub_date = timezone.datetime.now()  # 내용 채우기
    blog.save()  # 저장하기

    return redirect('/blog/')


def clean_html(x):
    x = re.sub("\&\w*\;", "", x)
    x = re.sub("<.*?>", "", x)
    return x


def news(request,news_index):
    search = request.GET.get('search')
    search = '부동산'
    page = request.GET.get('page')
    client_id = "6HlcFx6Fi1uXNPCW7pmG"
    client_secret = "6Hx6DIiFP_"

    encode_type = 'json'  # 출력 방식 json 또는 xml
    # max_display = 5  # 출력 뉴스 수
    max_display = news_index
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
    result=result[(news_index-5):news_index]
    return render(request, 'test1/news.html', {'result': result, 'next_index':news_index+5, 'prev_index':news_index-5})


# -------------------END, 다음페이지, 이전페이지 뉴스 2 HTML--------------------------------------------

def notice(request, notice_id):
    notice_pk = get_object_or_404(
        NoticeBlog, pk=notice_id)  # 특정 객체 가져오기(없으면 404 에러)
    notice_hit = NoticeBlog.objects.get(id=notice_id)
    notice_hit.hit = notice_hit.hit + 1
    notice_hit.save()

    return render(request, 'test1/notice.html', {'notice_pk': notice_pk})


def notice_register(request):

    return render(request, 'test1/notice_register.html', {})


def loginregister(request):
    return render(request, 'test1/loginregister.html', {})


def logout(request):
    return render(request, 'test1/logout.html')


def contact(request):
    return render(request, 'test1/contact.html')

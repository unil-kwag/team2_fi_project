"""pjt1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path

from test1.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='main'),

    # ======================================================입지선정
    path('selection/', selection, name='Location_Selection'),
    path('songpa/', songpa, name='map'),
    path('dobong/', dobong, name='dobong'),
    path('dongdaemoon/', dongdaemoon, name='map'),
    path('dongjak/', dongjak, name='map'),
    path('eunpyeong/', eunpyeong, name='map'),
    path('gangbook/', gangbook, name='map'),
    path('gangdong/', gangdong, name='map'),
    path('gangnam/', gangnam, name='map'),
    path('gangseo/', gangseo, name='map'),
    path('geumcheon/', geumcheon, name='map'),
    path('guro/', guro, name='map'),
    path('gwanak/', gwanak, name='map'),
    path('gwangjin/', gwangjin, name='map'),
    path('jongro/', jongro, name='map'),
    path('joong/', joong, name='map'),
    path('joongrang/', joongrang, name='map'),
    path('mapo/', mapo, name='map'),
    path('noone/', noone, name='map'),
    path('seocho/', seocho, name='map'),
    path('seodaemoon/', seodaemoon, name='map'),
    path('seongbook/', seongbook, name='map'),
    path('seongdong/', seongdong, name='map'),
    path('yangcheon/', yangcheon, name='map'),
    path('yeongdeung/', yeongdeung, name='map'),
    path('yongsan/', yongsan, name='map'),
    path('seoul/', seoul, name='seoul'),
    path('test/', test, name='test'),
    path('seoul/', seoul, name='seoul'),
    path('test/', test, name='test'),
    # ======================================================입지선정

    path('search/', search, name='Search'),
    path('news/<int:news_index>', news, name='news'),




    path('django_dash/', include('django_plotly_dash.urls')),

    path('blog/', blog, name='blog'),

    path('detail/<int:blog_id>', detail, name="detail"),
    path('detail/comment_insert/<int:blog_id>',comment_insert, name='comment_insert'),
    path('blog/new', new, name="new"),
    path('blog/create', create, name='create'),
    path('blog/edit/<int:blog_id>', edit, name="edit"),
    path('blog/update/<int:blog_id>', update, name="update"),
    path('blog/delete/<int:blog_id>', delete, name="delete"),
    path('loginregister/', loginregister, name='loginregister'),

    # 네이버 API 가져오기
    path('accounts/', include('allauth.urls')),

    path('notice/<int:notice_id>', notice, name="notice"),
    path('notice_register/', notice_register, name='notice_register'),
    path('notice_register/notice_create', notice_create, name='notice_create'),
    path('notice/notice_delete/<int:notice_id>',notice_delete, name='notice_delete'),
    path('logout/', logout, name="logout"),
    path('contact/', contact, name='contact'),

    path('index_option2/', index_option2, name='index_option2'),
    path('index_option3/', index_option3, name='index_option3')
]

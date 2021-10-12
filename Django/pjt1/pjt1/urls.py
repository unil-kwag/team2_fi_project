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
from django.contrib import admin
from django.urls import path,include

from test1.views import *
import test1.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='main'),
    

    path('selection/',selection,name='Location_Selection'),
    path('map/',map,name='map'),
    path('seoul/',seoul,name='seoul'),
    path('test/',test,name='test'),


    path('search/',search,name='Search'),
    path('news/',news,name='News'),
    path('board_main/',board_main,name='Board_main'),
    path('board_write/',board_write,name='Board_write'),
    path('board_view/',board_view,name='Board_view'),
    path('board_edit/',board_edit,name='Board_edit'),
    
    path('django_dash/', include('django_plotly_dash.urls')),
    path('blog/', home, name='home'),
    path('blog/<int:blog_id>', detail, name="detail"),
    path('blog/new', new, name="new"),
    path('blog/create', create, name='create'),
    path('blog/edit/<int:blog_id>',edit, name="edit"),
    path('blog/update/<int:blog_id>', update, name="update"),
    path('blog/delete/<int:blog_id>', delete, name="delete"),
]

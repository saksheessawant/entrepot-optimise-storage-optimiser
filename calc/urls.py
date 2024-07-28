from django.urls import path
from django.contrib import admin
from . import views

urlpatterns=[
path('',views.home,name="home"),
path('home1',views.home1,name="home1"),
#path('', views.button),
#path('output/', views.output,name="script"),
#path('calc/external/', views.external),

]
from django.urls import path
from app01 import views
from django.conf.urls import url
import app01
urlpatterns = [

    path('index/',views.index,name='publisher_list'),
    path('predict/',views.predict),
    path('draw/',views.draw,name='stock_list'),
    path('income/',views.d_stoke),


]
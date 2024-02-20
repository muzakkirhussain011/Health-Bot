from django.urls import path
from . import views

urlpatterns = [
    path('bot_reply/', views.bot_reply, name='bot_reply'),
    path('reset_app/', views.reset_app, name='reset_app'),
    path('', views.index, name='index'),
    path('FAQ.html', views.faq, name='FAQ'),
    path('index.html', views.index, name='index')

]

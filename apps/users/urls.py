__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/9 13:28'

from django.urls import path

from .views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(),  name='login'),
    path('register/', RegisterView.as_view(),  name='register'),
    path('forget/', RegisterView.as_view(),  name='forget'),
    path('active/', LoginView.as_view(),  name='active'),
]

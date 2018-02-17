__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/17 21:46'


from django.urls import path

from .views import AddFavView

urlpatterns = [
    path('add_fav', AddFavView.as_view(), name='add_fav')
]
__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/15 8:23'

from django.urls import path

from .views import OrgListView

urlpatterns = [
    path('list/', OrgListView.as_view(), name='org_list')
]
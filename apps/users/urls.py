__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/9 13:28'

from django.urls import path

from .views import LoginView, RegisterView, ActiveView, ForgetView, LogoutView, ResetView, ModifyView

urlpatterns = [
    path('login/', LoginView.as_view(),  name='login'),
    path('logout/', LogoutView.as_view(),  name='logout'),
    path('register/', RegisterView.as_view(),  name='register'),
    path('forget/', ForgetView.as_view(),  name='forget'),
    path('active/<str:email_code>/', ActiveView.as_view()),
    path('reset/<str:email_code>/', ResetView.as_view()),
    path('modify/', ModifyView.as_view(), name='modify_pwd')
]

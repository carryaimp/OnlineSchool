"""OnlineSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.static import serve
import xadmin

from OnlineSchool.settings import MEDIA_ROOT
from users.views import HomeView

urlpatterns = [
    # xadmin后台
    path('xadmin/', xadmin.site.urls),
    # 主页
    path('', HomeView.as_view(), name='index'),
    # 用户相关的业务
    path('user/', include('users.urls')),
    # 简单验证码
    path('captcha/', include('captcha.urls')),
    # 课程机构业务
    path('org/', include('organization.urls')),
    # # 图片前端显示, 这个是静态文件, 默认不展示，静态文件通过第三方如nginx或http进行代理
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # 用户操作逻辑业务
    path('operation/', include('operation.urls')),
    # 课程相关
    path('course/', include('course.urls')),
    # 用户中心
    path('center/', include('operation.urls')),
]

# django全局错误页面处理
# 全局404错误
handler404 = 'apps.handler_error_view.handler_404_error'
# 全局403错误
handler403 = 'apps.handler_error_view.handler_403_error'
# 全局500错误
handler500 = 'apps.handler_error_view.handler_500_error'

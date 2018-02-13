from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
# django 中验证类
from django.contrib.auth.backends import ModelBackend
# django的or查询
from django.db.models import Q


from .models import UserProfile
from .forms import LoginForm


class CustomBackend(ModelBackend):
    """
    自定义 authenticate 认证，用于邮箱、用户名、手机账号登录
    需要在setting中配置
    AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
    )
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(password=password))

            if user.check_password(raw_password=password):
                return user
        except Exception as e:
            print(e)
            return None


class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', None)
            password = request.POST.get('password', None)
            # 验证用户是否在数据库中存在, 返回是一个对象
            user = authenticate(username=user_name, password=password)
            # 验证如果用户验证通过，通过login函数创建session，本质上在request中写入了东西
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {
                    'msg': '用户名或密码错误'
                })
        else:
            return render(request, 'login.html', {
                'login_form': login_form
            })


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        pass


class ForgetView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class ActiveView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass

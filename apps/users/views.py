from django.shortcuts import render,  redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
# django 中验证类
from django.contrib.auth.backends import ModelBackend
# django的or查询
from django.db.models import Q


from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm
from .tools import send_email


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
                # 判断用户是否激活，激活才让其登录
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {
                        'msg': '用户未激活'
                    })
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
        register_form = RegisterForm()
        return render(request, 'register.html', {
            'register_form': register_form
        })

    def post(self, request):
        # 返回渲染模版数据字典
        render_data = dict()
        register_form = RegisterForm(request.POST)
        user_email = request.POST.get('email', None)
        user_pwd = request.POST.get('password', None)
        render_data['register_form'] = register_form

        if register_form.is_valid():
            send_status = send_email(email_address=user_email, email_type='register')
            if send_status:
                user_profile = UserProfile()
                user_profile.username = user_email
                user_profile.email = user_email
                user_profile.password = make_password(user_pwd)
                user_profile.is_active = 0
                user_profile.save()
                # 跳转到登录邮箱验证页面？或者跳转到登录页面
                return redirect(to='login')
            else:
                render_data['email_error'] = '该邮箱不存在'
                return render(request, 'register.html', render_data)
        else:
            render_data['email_error'] = ''
            return render(request, 'register.html', render_data)
        pass


class ForgetView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class ActiveView(View):
    """
    用户注册账号激活,如果表中有则跳到登录页面，没有则返回注册，这里要确认这个随机的字符串唯一则对应唯一有效用户
    """
    def get(self, request, email_code):
        record_code = EmailVerifyRecord.objects.get(code=email_code)
        if record_code:
            user_active = UserProfile.objects.get(username=record_code.email)
            user_active.is_active = True
            user_active.save()
            return redirect(to='login')
        else:
            return redirect(to='register')

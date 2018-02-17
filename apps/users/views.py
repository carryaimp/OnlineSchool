from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
# django 中验证类
from django.contrib.auth.backends import ModelBackend
# django的or查询
from django.db.models import Q


from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .tools import send_email, get_mail_url


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
        return render(request, 'user/login.html')

    def post(self, request):
        render_data = dict()
        login_form = LoginForm(request.POST)
        user_name = request.POST.get('username', None)
        password = request.POST.get('password', None)
        render_data['login_form'] = login_form
        render_data['user_name'] = user_name if user_name else ''
        render_data['password'] = password if password else ''
        if login_form.is_valid():
            # 验证用户是否在数据库中存在, 返回是一个对象
            user = authenticate(username=user_name, password=password)
            # 验证如果用户验证通过，通过login函数创建session，本质上在request中写入了东西
            if user is not None:
                # 判断用户是否激活，激活才让其登录
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    render_data['msg'] = '用户未激活'
                    return render(request, 'user/login.html', render_data)
            else:
                render_data['msg'] = '用户名或密码错误'
                return render(request, 'user/login.html', render_data)
        else:
            render_data['msg'] = ''
            return render(request, 'user/login.html', render_data)


class LogoutView(View):
    """
    用户退出登录
    """
    def get(self, request):
        logout(request)
        return redirect(to='index')


class RegisterView(View):
    """
    用户注册处理，包括验证码，发送邮件验证，判读邮箱是否注册的要求
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {
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
            # 判断这个邮箱是否注册
            if UserProfile.objects.filter(email=user_email):
                render_data['email_error'] = '该邮箱已经注册'
                return render(request, 'user/register.html', render_data)
            # 通过send_status判断是否发送成功判断这个邮箱是否存在
            send_status = send_email(email_address=user_email, email_type='register')
            if send_status:
                # 把注册的用户is_active为未激活状态
                user_profile = UserProfile()
                user_profile.username = user_email
                user_profile.email = user_email
                user_profile.password = make_password(user_pwd)
                user_profile.is_active = 0
                user_profile.save()
                # 跳转到登录邮箱验证页面？或者跳转到登录页面
                email_url = get_mail_url(email=user_email)
                return redirect(to=email_url)
            else:
                render_data['email_error'] = '该邮箱不存在'
                return render(request, 'user/register.html', render_data)
        else:
            render_data['email_error'] = ''
            return render(request, 'user/register.html', render_data)


class ForgetView(View):
    """
    用户忘记密码逻辑,需要检查该邮箱是否注册
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'user/forgetpwd.html', {
            'forget_form': forget_form
        })

    def post(self, request):
        render_data = dict()
        forget_form = ForgetForm(request.POST)
        email = request.POST.get('email', None)
        render_data['forget_form'] = forget_form
        render_data['email'] = email if email else ''
        if forget_form.is_valid():
            if UserProfile.objects.filter(email=email):
                send_status = send_email(email_address=email, email_type='forget')
                if send_status:
                    # 自动跳转到邮箱登录页面
                    email_url = get_mail_url(email=email)
                    return redirect(to=email_url)
            else:
                render_data['email_error'] = '该邮箱未注册'
                return render(request, 'user/forgetpwd.html', render_data)
        else:
            render_data['email_error'] = ''
            return render(request, 'user/forgetpwd.html', render_data)


class ResetView(View):
    """
    返回修改密码页面，包含2个信息，一个是验证码和邮箱信息注入到html页面的input中
    """
    def get(self, request, email_code):
        try:
            user_email = EmailVerifyRecord.objects.get(code=email_code, send_type='forget').email
        except:
            return redirect(to='index')
        if user_email:
            return render(request, 'user/password_reset.html', {
                'email': user_email,
                'email_code': email_code
            })
        else:
            return redirect(to='index')


class ModifyView(View):
    """
    为了解决url匹配规则中含有正则规范错误，正则和提交分开
    """
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        render_data = dict()
        render_data['reset_pwd_form'] = modify_pwd_form
        email = request.POST.get('email', None)
        email_code = request.POST.get('email_code', None)
        render_data['email'] = email if email else ''
        render_data['email_code'] = email_code if email_code else ''
        # 验证提交数据是否合法
        if modify_pwd_form.is_valid():
            first_password = request.POST.get('first_password', None)
            sure_password = request.POST.get('sure_password', None)
            # 验证两次密码是否正确
            if first_password == sure_password:
                # 验证这个邮箱是否有发送过验证码记录
                try:
                    user_email = EmailVerifyRecord.objects.get(code=email_code, send_type='forget', email=email).email
                except:
                    return redirect(to='login')
                if user_email:
                    # 验证邮箱是否更改
                    if email == user_email:
                        # 更改密码
                        user_profile = UserProfile.objects.get(email=email)
                        user_profile.password = make_password(sure_password)
                        user_profile.save()
                        return redirect(to='login')
                    else:
                        return redirect(to='login')
                else:
                    return redirect(to='login')
            else:
                render_data['pwd_error'] = '两次密码不相同'
                return render(request, 'user/password_reset.html', render_data)
        else:
            render_data['pwd_error'] = ''
            return render(request, 'user/password_reset.html', render_data)


class ActiveView(View):
    """
    用户注册账号激活,如果表中有则跳到登录页面，没有则返回注册，这里要确认这个随机的字符串唯一则对应唯一有效用户
    """
    def get(self, request, email_code):
        try:
            # 随机12个字符串，有可能出现一样的，可能出错，要保证这个注册时候code唯一，还有并没有检查过期时间
            record_code = EmailVerifyRecord.objects.get(code=email_code, send_type='register')
        except:
            return redirect(to='register')
        if record_code:
            user_active = UserProfile.objects.get(username=record_code.email)
            if user_active:
                user_active.is_active = True
                user_active.save()
                return redirect(to='login')
            else:
                return redirect(to='register')
        else:
            return redirect(to='register')

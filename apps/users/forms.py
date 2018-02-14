__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/10 13:22'


from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    """
    用户登录验证前端提交的用户名和密码
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
    用户注册需要提交的信息，验证码使用第三方模块
    """
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    password = forms.CharField(required=True, min_length=5, error_messages={'required': '密码不能为空',
                                                                            'min_length': '密码至少为5位'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误', 'required': '验证码不能为空'})


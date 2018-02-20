__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/17 21:50'

from django import forms

from .models import CourseComment
from users.models import UserProfile, EmailVerifyRecord


class CourseCommentForm(forms.ModelForm):
    """课程评价表单提交验证"""
    class Meta:
        model = CourseComment
        fields = ['user', 'course', 'comment']


class ImageUploadForm(forms.ModelForm):
    """用户上传图片表单验证，文件在django中存放在FIlES中"""
    class Meta:
        model = UserProfile
        fields = ['head_image']


class UpdatePwdForm(forms.Form):
    """用户中心修改密码表单验证"""
    first_password = forms.CharField(required=True, min_length=6, max_length=20)
    sure_password = forms.CharField(required=True, min_length=6, max_length=20)


class UpdateEmailForm(forms.ModelForm):
    """用户更改邮箱，对邮箱和验证码两个字段进行验证"""
    class Meta:
        model = EmailVerifyRecord
        fields = ['email', 'code']


class UpdateUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']
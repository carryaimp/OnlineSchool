__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/16 22:27'

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    继承 form.ModelForm 使用表约束对字段进行验证
    需要指定 表， 需要验证的字段
    通过 ModelForm可以新增非数据表中的字段， 也可以对某个字段自定义验证字段
    还可以通过 ModelForm 直接保存数据
    """
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
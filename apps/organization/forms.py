__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/16 22:27'

import re

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

    def clean_mobile(self):
        """
        自定义一个mobile自定义验证规则，验证手机输入是否合法
        通过 clean_字段 方式，自定义字段验证
        :return:
        """
        mobile = self.cleaned_data['mobile']
        print(mobile, type(mobile))
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            # 自定义异常
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/17 21:50'

from django import forms

from .models import CourseComment


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['user', 'course', 'comment']
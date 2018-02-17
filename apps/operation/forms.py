__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/17 21:50'

from django import forms

from .models import UserFavorite


class UserFavoriteForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['user', 'fav_id', 'fav_type']
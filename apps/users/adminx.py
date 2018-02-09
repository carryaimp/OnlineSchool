__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/8 22:03'

from .models import EmailVerifyRecord, Banner, UserProfile

import xadmin


class EmailVerifyRecordAdmin(object):
    # 设置后台表显示的列，并且按这个列表的顺序显示
    # 这里有三个字段，分别为 list_display search_fields list_filter, 显示的列,搜索字段，过滤字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    pass


class BannerAdmin(object):
    list_display = ['title', 'banner_image', 'index', 'url', 'add_time']
    search_fields = ['title', 'banner_image', 'index', 'url']
    list_filter = ['title', 'banner_image', 'index', 'url', 'add_time']


class UserProfileAdmin(object):
    list_display = ['username', 'email', 'nick_name', 'birthday', 'gender', 'address', 'mobile', 'add_time']
    search_fields = ['username', 'email','nick_name', 'birthday', 'gender', 'address', 'mobile']
    list_filter = ['username', 'email','nick_name', 'birthday', 'gender', 'address', 'mobile', 'add_time']


# 注册
xadmin.site.unregister(UserProfile)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
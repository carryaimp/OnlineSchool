__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/8 22:03'

from .models import EmailVerifyRecord, Banner, UserProfile

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserProfileAdmin


class BaseSetting(object):
    """
    是否使用主题
    """
    enable_themes = True
    use_bootswatch = True


class CommonSetting(object):
    """
    更改后台的标题和落脚，并且让菜单可以收起来
    """
    # 后台标题
    site_title = '在线视频后台'
    # 后台落脚
    site_footer = '北门吹雪'
    # 收缩菜单
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    # 设置后台表显示的列，并且按这个列表的顺序显示
    # 这里有三个字段，分别为 list_display search_fields list_filter, 显示的列,搜索字段，过滤字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-envelope'
    pass


class BannerAdmin(object):
    list_display = ['title', 'banner_image', 'index', 'url', 'add_time']
    search_fields = ['title', 'banner_image', 'index', 'url']
    list_filter = ['title', 'banner_image', 'index', 'url', 'add_time']
    model_icon = 'fa fa-picture-o'


# class UserProfileAdmin(object):
#     list_display = ['username', 'email', 'nick_name', 'birthday', 'gender', 'address', 'mobile', 'add_time']
#     search_fields = ['username', 'email', 'nick_name', 'birthday', 'gender', 'address', 'mobile']
#     list_filter = ['username', 'email', 'nick_name', 'birthday', 'gender', 'address', 'mobile', 'add_time']


# 全局注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, CommonSetting)

# 表注册，也就决定后台的models显示的顺序
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

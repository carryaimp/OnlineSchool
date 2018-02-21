from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # 给后台显示的中文app名字
    verbose_name = '用户信息'

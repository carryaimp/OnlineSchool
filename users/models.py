from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息表，并扩展了django默认user表，
    还需要再setting中配置 AUTH_USER_MODEL = 'users.UserProfile'
    用这张扩展的表替换django默认的用户表，需要注意点不能在工程开始就初始化表工作，
    这会和这张表冲突并发送不可描叙的错误，这酸爽，你懂得
    """
    sex = (
        ('male', '男'),
        ('female', '女')
    )
    nick_name = models.CharField(max_length=50, verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=6, choices=sex, default='male', verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    head_image = models.ImageField(upload_to='image/%Y/%m', default='default.png', max_length=100, verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username



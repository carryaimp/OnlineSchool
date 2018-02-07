from datetime import datetime

from django.db import models

from users.models import UserProfile
from course.models import Course
# Create your models here.


class UserAsk(models.Model):
    """
    课程咨询留言表，包含用户名、用户手机号码、咨询课程名、添加时间
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机毫秒')
    course_name = models.CharField(max_length=50, verbose_name='课程名')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComment(models.Model):
    """
    课程评论表，需要关联两个表： 用户表和课程表
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    comment = models.CharField(max_length=200, verbose_name='评论')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class UserFavorite(models.Model):
    """
    用户收藏表，可以通过外键关联实现，分别为课程表、机构表、用户表
    我们也可以使用 ID + 类型 来进行设计实现，ID指对应的表数据id，类型指该ID对应的数据表
    """
    fav_type_choice = (
        ('1', '课程'),
        ('2', '课程机构'),
        ('3', '讲师')
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    # 通过 存放课程或机构对应的id，再指明对应收藏的类别，就可以实现类似外键的功能
    fav_id = models.IntegerField(default=0, verbose_name='数据ID')
    fav_type = models.IntegerField(choices=fav_type_choice, verbose_name='收藏类型')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fav_id


class UserMessage(models.Model):
    """
    消息分为两种，一种是用户定向消息，一种是系统发给所有人的消息，如果只是定向给
    用户，那么使用外键完成，如果定向为所有用户，则不能使用外键
    我们约定，0 表示发给所有用户，其他整数表示发给指定的用户id，就有了两种状态
    """
    user = models.IntegerField(default=0, verbose_name='接收用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    # 约定has 该字段为boolean类型,False 为未读， True为已读
    has_read = models.BooleanField(default=False, verbose_name='是否已读')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class UserCourse(models.Model):
    """
    用户学习课程，，通过两个外键关联用户表和课程表
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


from django.db import models

# Create your models here.

from organization.models import CourseOrg, Teacher
from users.models import UserProfile


class Course(models.Model):
    """
    定义课程表，包含课程名、课程封面图、课程简介、课程详情（为富文本编辑框）、课程时长（分钟）
    定义记录统计信息： 学习该课程人数、课程收藏数、课程点击量
    """
    # 课程难度等级
    course_degree = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级')
    )
    org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=True, verbose_name='课程机构',)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=True, verbose_name='讲师')
    name = models.CharField(max_length=50, verbose_name='课程名')
    course_image = models.ImageField(upload_to='course/%Y/%m', verbose_name='课程封面图')
    desc = models.CharField(max_length=300, verbose_name='课程简介')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(max_length=2, choices=course_degree, verbose_name='课程难度')
    learn_time = models.IntegerField(default=0, verbose_name='学习总时长(分钟)')
    category = models.CharField(max_length=20, null=True, blank=True, verbose_name='课程类别')
    message = models.CharField(max_length=20, null=True, blank=True, verbose_name='课程公告')
    need_know = models.CharField(max_length=50, null=True, blank=True, verbose_name='课程须知')
    can_learn = models.CharField(max_length=50, null=True, blank=True, verbose_name='学到知识')
    # 统计
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='课程点击量')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_num(self):
        # 获得单个实例的章节数
        return self.lesson_set.all().count()

    def learn_user(self):
        # 获得学习该课程的学生，只取5个
        return self.usercourse_set.all().order_by('-add_time')[:5]


class Lesson(models.Model):
    """
    章节表，只包含章节名、添加时间、一个关联课程表的外键
    """
    # 章节与课程是多对一关系，需要在多关系的一方建立一个外键关联少的一方主键
    # 关联外键，通过django的 ForeignKey 只需要注明想要关联的表
    # 会自动获取关联表的ID并创建关联字段
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    name = models.CharField(max_length=100, verbose_name='章节名')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    """
    定义章节下视频信息。包含关联Lesson表的外键、视频名字、添加时间
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=200, null=True, blank=True, verbose_name='访问地址')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """
    课程资源信息，包含 关联课程外键、资源名称、下载资源地址、添加时间信息
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    # 需要从后台上传资源到指定目录
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='资源地址')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

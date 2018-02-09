from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    """
    城市相关信息，包含 城市名、城市相关描叙 信息
    """
    name = models.CharField(max_length=20, verbose_name='城市名')
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='城市描叙')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """
    机构，包含 机构名、机构封面、机构地址、机构描叙 相关信息
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所在城市')
    name = models.CharField(max_length=50, verbose_name='机构名称')
    org_image = models.ImageField(upload_to='org/%Y/%m', verbose_name='机构封面图')
    desc = models.TextField(verbose_name='机构描叙')
    address = models.CharField(max_length=150, verbose_name='机构地址')

    # 统计
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    课程教师相关信息，包含 所属机构、名字、工作年限、工作公司、职位、教学风格等信息
    还包含统计 点击量、收藏数信息
    """
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
    name = models.CharField(max_length=20, verbose_name='教师名')
    work_years = models.IntegerField(verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='就职公司')
    points = models.CharField(max_length=50, verbose_name='教学特点')

    # 统计
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')

    add_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '机构教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/8 22:03'


from .models import Course, Lesson, Video, CourseResource


import xadmin


class LessonInline(object):
    """可以再添加数据的时候，同时添加有外键关联我的数据"""
    # 指定那张表关联我
    model = Lesson
    # 指定默认的外键表数据
    extra = 4


class CourseAdmin(object):
    list_display = ['name', 'course_image', 'desc', 'detail', 'degree', 'learn_time',
                    'students', 'fav_num', 'click_num', 'add_time', 'lesson_num', 'go_to']
    search_fields = ['name', 'course_image', 'desc', 'detail', 'degree',
                     'learn_time', 'students', 'fav_num', 'click_num', 'lesson_num']
    list_filter = ['name', 'course_image', 'desc', 'detail', 'degree',
                   'learn_time', 'students', 'fav_num', 'click_num', 'add_time']
    model_icon = 'fa fa-book'
    ordering = ['-fav_num']
    readonly_fields = ['fav_num', 'click_num', 'students']
    # 指定添加数据时候，可以同时添加外键关联表数据
    inlines = [LessonInline]
    # 设置选择刷新时间
    refresh_times = [3, 5]

    def save_models(self):
        # 可以在保存课程实例的时候，做些任务，像触发器.新增和修改都会走这个流程
        # 如以下保存机构中course_num课程数量统计
        # obj = self.new_obj
        # odj.save()
        # if obj:
        #   course_org = obj.course_org
        #   course_org.course_num = Course.objects.filter(course_org=course_org).count()
        #   course_org.save()
        pass

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']
    model_icon = 'fa fa-th-list'


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fa fa-video-camera'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']
    model_icon = 'fa fa-cloud-download'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
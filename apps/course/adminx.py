__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/8 22:03'


from .models import Course, Lesson, Video, CourseResource


import xadmin


class CourseAdmin(object):
    list_display = ['name', 'course_image', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_num', 'click_num', 'add_time']
    search_fields = ['name', 'course_image', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_num', 'click_num']
    list_filter = ['name', 'course_image', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_num', 'click_num', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
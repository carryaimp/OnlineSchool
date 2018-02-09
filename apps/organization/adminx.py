__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/8 22:03'


import xadmin


from .models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'org_image', 'desc', 'address', 'click_num', 'fav_num', 'add_time']
    search_fields = ['city', 'name', 'org_image', 'desc', 'address', 'click_num', 'fav_num']
    list_filter = ['city', 'name', 'org_image', 'desc', 'address', 'click_num', 'fav_num', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
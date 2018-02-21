__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/8 22:03'


import xadmin


from .models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-map-marker'


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'org_image', 'desc', 'address', 'click_num', 'fav_num', 'add_time']
    search_fields = ['city', 'name', 'org_image', 'desc', 'address', 'click_num', 'fav_num']
    list_filter = ['city', 'name', 'org_image', 'desc', 'address', 'click_num', 'fav_num', 'add_time']
    model_icon = 'fa fa-graduation-cap'
    ordering = ['-click_num']
    readonly_fields = ['fav_num', 'click_num']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']
    model_icon = 'fa fa-black-tie'
    ordering = ['-click_num']
    readonly_fields = ['fav_num', 'click_num']


# 注册顺序也是后台显示顺序
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(City, CityAdmin)
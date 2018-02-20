__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/15 8:23'

from django.urls import path

from .views import OrgListView, AddAskView, OrgHome,\
    OrgDescView, OrgCourseView, OrgTeacherView, OrgTeacherListView, OrgTeacherDetailView

urlpatterns = [
    path('list/', OrgListView.as_view(), name='org_list'),
    path('add_ask/', AddAskView.as_view(), name='add_ask'),
    path('home/<int:org_id>/', OrgHome.as_view(), name='org_home'),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    path('teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),
    path('teacher/list', OrgTeacherListView.as_view(), name='teacher'),
    path('teacher/detail/<int:teacher_id>', OrgTeacherDetailView.as_view(), name='teacher_detail'),
]
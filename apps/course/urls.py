__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/18 7:59'

from django.urls import path
from .views import CourseListView, CourseDetailView, LessonView, CommentView, VideoPlayView

urlpatterns = [
    path('list', CourseListView.as_view(), name='course_list'),
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='course_detail'),
    path('lesson/<int:course_id>', LessonView.as_view(), name='course_lesson'),
    path('comment/<int:course_id>', CommentView.as_view(), name='course_comment'),
    path('video/<int:course_id>/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),
]
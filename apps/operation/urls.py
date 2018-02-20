__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/17 21:46'


from django.urls import path

from .views import AddFavView, UserInfoView, UserCourseView, \
    UserFavView, UserMessageView, ImageUploadView, UpdatePwdView, \
    EmailCodeView, UpdateEmailView

urlpatterns = [
    path('add-fav/', AddFavView.as_view(), name='add_fav'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
    path('user-course/', UserCourseView.as_view(), name='user_course'),
    path('user-fav/', UserFavView.as_view(), name='user_fav'),
    path('user-message/', UserMessageView.as_view(), name='user_message'),
    path('image/upload/', ImageUploadView.as_view(), name='image_upload'),
    path('update-pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path('email-code/', EmailCodeView.as_view(), name='email_code'),
    path('update-email/', UpdateEmailView.as_view(), name='update_email')
]
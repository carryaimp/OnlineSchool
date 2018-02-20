import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from users.models import UserProfile, EmailVerifyRecord
from .forms import ImageUploadForm, UpdatePwdForm, UpdateEmailForm, UpdateUserInfoForm
from .models import UserFavorite, UserMessage
from course.models import Course
from organization.models import CourseOrg, Teacher
from operation.models import UserCourse
from tools.send_email import send_email
from tools.need_login import NeedLoginViewMinx

from pure_pagination import Paginator, PageNotAnInteger


class AddFavView(View):
    """
    用户添加收藏，包括课程，课程机构，讲师三类收藏
    首先要判断用户是否登录，获得用户ID，再判断收藏的数据是否存在（判断用户是否非法提交）
    如果用户点击收藏，查看是否有记录，有则删除，没有则添加
    """
    def post(self, request):
        rep_data = dict()
        # 判断用户是否登录
        if not request.user.is_authenticated:
            rep_data['status'] = 'fail'
            rep_data['msg'] = '用户未登录'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')

        # 判断用户提交数据是否合法
        try:
            fav_id = int(request.POST.get('fav_id', 0))
            fav_type = int(request.POST.get('fav_type', 0))
        except:
            rep_data['status'] = 'fail'
            rep_data['msg'] = '收藏出错'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')
        if fav_id <= 0 or fav_type not in [1, 2, 3]:
            rep_data['status'] = 'fail'
            rep_data['msg'] = '收藏出错'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')

        # 检查对应的id是否在数据库中存在？闯关模式
        if fav_type == 1:
            try:
                record = Course.objects.get(id=fav_id)
            except:
                rep_data['status'] = 'fail'
                rep_data['msg'] = '收藏出错'
                return HttpResponse(json.dumps(rep_data), content_type='application/json')
        if fav_type == 2:
            try:
                record = CourseOrg.objects.get(id=fav_id)
            except:
                rep_data['status'] = 'fail'
                rep_data['msg'] = '收藏出错'
                return HttpResponse(json.dumps(rep_data), content_type='application/json')
        if fav_type == 3:
            try:
                record = Teacher.objects.filter(id=fav_id)
            except:
                rep_data['status'] = 'fail'
                rep_data['msg'] = '收藏出错'
                return HttpResponse(json.dumps(rep_data), content_type='application/json')

        # 查看记录是否存在，存在则删除，不存在则添加
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_record:
            exist_record.delete()
            rep_data['status'] = 'success'
            rep_data['msg'] = '收藏'
            # 统计收藏， 无论fav_type是哪个，上面三个record总会有个生效
            record.fav_num += 1
            record.save()
            return HttpResponse(json.dumps(rep_data), content_type='application/json')
        else:
            user_fav = UserFavorite()
            user_fav.user = request.user
            user_fav.fav_type = fav_type
            user_fav.fav_id = fav_id
            user_fav.save()

            # 统计
            record.fav_num -= 1
            record.save()
            rep_data['status'] = 'success'
            rep_data['msg'] = '已收藏'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')


class UserInfoView(NeedLoginViewMinx, View):
    """用户中心，包括修改头像、修改密码、修改邮箱、个人相关信息"""
    def get(self, request):
        #  用户信息保存在session中，封装在request中
        render_data = dict()
        return render(request, 'center/usercenter-info.html', render_data)

    def post(self, request):
        """
        用户提交个人信息修改， ajax方式提交
        :param request:
        :return:
        """
        render_data = dict()
        if request.user.is_authenticated:
            # 通过 instance 指明修改哪些实例，本质上指明修改那几行数据
            update_user_info = UpdateUserInfoForm(request.POST, instance=request.user)
            if update_user_info.is_valid():
                update_user_info.save()
                render_data['status'] = 'success'
                return HttpResponse(json.dumps(render_data), content_type='application/json')
            else:
                render_data['status'] = 'fail'
                render_data['msg'] = update_user_info.errors
                return HttpResponse(json.dumps(render_data), content_type='application/json')
        else:
            render_data['status'] = 'fail'
            render_data['msg'] = "没有登录哦"
            return HttpResponse(json.dumps(render_data), content_type='application/json')


class UserCourseView(NeedLoginViewMinx, View):
    """用户学习课程中心"""
    def get(self, request):
        render_data = dict()
        all_course = UserCourse.objects.filter(user=request.user)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, per_page=8, request=request)
        # 进行分页
        all_course = p.page(page)

        render_data['all_course'] = all_course
        return render(request, 'center/usercenter-mycourse.html', render_data)


class UserFavView(NeedLoginViewMinx, View):
    """用户收藏课程中心"""
    def get(self, request):
        course, org, teacher = 1, 2, 3
        render_data = dict()
        all_fav = UserFavorite.objects.all()
        menu_key = request.GET.get('menu-key', None)
        # 依据不同的menu_key返回不同的页面
        # 课程收藏
        if menu_key == 'course':
            # page_label用于导航栏激活状态使用
            page_label = 'course'
            render_data['page_label'] = page_label
            # 找出所有收藏课程ID
            fav_course_id = [course.fav_id for course in all_fav.filter(user=request.user, fav_type=course)]
            # 通过收藏课程ID找到所有的课程
            fav_course = Course.objects.filter(id__in=fav_course_id)
            render_data['page_label'] = page_label
            render_data['fav_course'] = fav_course
            return render(request, 'center/usercenter-fav-course.html', render_data)

        # 教师收藏
        elif menu_key == 'teacher':
            fav_teacher_id = [teacher.fav_id for teacher in all_fav.filter(user=request.user, fav_type=teacher)]
            fav_teacher = Teacher.objects.filter(id__in=fav_teacher_id)
            page_label = 'teacher'
            render_data['page_label'] = page_label
            render_data['fav_teacher'] = fav_teacher
            return render(request, 'center/usercenter-fav-teacher.html', render_data)

        else:
            # 默认显示收藏的机构页面
            page_label = ''
            fav_org_id = [org.fav_id for org in all_fav.filter(user=request.user, fav_type=org)]
            fav_org = CourseOrg.objects.filter(id__in=fav_org_id)
            render_data['page_label'] = page_label
            render_data['fav_org'] = fav_org
            return render(request, 'center/usercenter-fav-org.html', render_data)


class UserMessageView(NeedLoginViewMinx, View):
    """用户消息通知中心"""
    def get(self, request):
        render_data = dict()
        public_message = UserMessage.objects.filter(user=0).order_by('-add_time')[:5]
        person_message = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')
        # 统一把消息修改为全读
        UserMessage.objects.filter(user=request.user.id, has_read=False).update(has_read=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(person_message, per_page=8, request=request)
        # 进行分页
        person_message = p.page(page)

        render_data['public_message'] = public_message
        render_data['person_message'] = person_message
        return render(request, 'center/usercenter-message.html', render_data)


class ImageUploadView(NeedLoginViewMinx, View):
    """
    用户修改头像
    django总用户上传文件放在request.FILES中，和post方式提交的分开
    上传url > post方式接收数据，FILES字段中存放上传的文件 > 定义一个form表单 > 通过form表单中clean_data获得验证后的数据 > 更改保存
    """
    def post(self, request):
        render_data = dict()
        """
        通过 instance 参数指定修改的对象，因为有了model和修改的对象，就可以直接更改了
        :param request:
        :return:
        """
        image_upload_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_upload_form.is_valid():
            image_upload_form.save()
            # image = image_upload_form.cleaned_data['head_image']
            # request.user.head_image = image
            # request.user.save()

            # 写入消息
            message = UserMessage()
            message.user = request.user.id
            message.message = '修改头像成功了哦'
            message.save()

            render_data['status'] = 'success'
            return HttpResponse(json.dumps(render_data), content_type='application/json')
        else:
            render_data['status'] = 'fail'
            return HttpResponse(json.dumps(render_data), content_type='application/json')


class UpdatePwdView(NeedLoginViewMinx, View):
    """用户登录状态下修改密码"""
    def post(self, request):
        render_data = dict()
        update_pwd_form = UpdatePwdForm(request.POST)
        if update_pwd_form.is_valid():
            first_password = request.POST.get('first_password', None)
            sure_password = request.POST.get('sure_password', None)
            # 验证两次密码输入是否都一样
            if first_password == sure_password:
                request.user.password = make_password(first_password)
                request.user.save()

                # 写入消息
                message = UserMessage()
                message.user = request.user.id
                message.message = '修改密码成功了哦'
                message.save()

                render_data['status'] = 'success'
                return HttpResponse(json.dumps(render_data), content_type='application/json')
            else:
                render_data['status'] = 'fail'
                render_data['msg'] = '密码不一致'
                return HttpResponse(json.dumps(render_data), content_type='application/json')
        else:
            return HttpResponse(json.dumps(update_pwd_form.errors), content_type='application/json')


class EmailCodeView(NeedLoginViewMinx, View):
    """用户修改邮箱发送验证码"""

    def get(self, request):
        render_data = dict()
        email = request.GET.get('email', '')
        if email:
            # 检查邮箱是否注册过
            if UserProfile.objects.filter(email=email):
                render_data['email'] = '邮箱已经注册'
                return HttpResponse(json.dumps(render_data), content_type='application/json')
            # 发邮件
            send_status = send_email(email_address=email, email_type='update')
            if send_status:
                # 写入消息
                message = UserMessage()
                message.user = request.user.id
                message.message = '哇，人家已经把你验证邮件发送出去了哦'
                message.save()
                render_data['email'] = '已发送邮箱验证码'
                return HttpResponse(json.dumps(render_data), content_type='application/json')
        else:
            render_data['email'] = '邮箱输入错误'
            return HttpResponse(json.dumps(render_data), content_type='application/json')


class UpdateEmailView(NeedLoginViewMinx, View):
    """
    用户修改邮箱
    """
    def post(self, request):
        """ajax方式提交数据"""
        update_email_form = UpdateEmailForm(request.POST)
        render_data = dict()
        if update_email_form.is_valid():
            email = request.POST.get('email', '')
            code = request.POST.get('code', '')
            # 排序找出最新的验证码
            last_record = EmailVerifyRecord.objects.filter(email=email, send_type='update',
                                                           has_used=False).order_by('-send_time')
            # 判断最新的验证码使用一致
            if last_record.first().code == code:
                try:
                    email_record = last_record.get(code=code)
                except:
                    render_data['email'] = '邮箱验证出错'
                    return HttpResponse(json.dumps(render_data), content_type='application/json')
                if email_record:
                    # 更改邮箱
                    request.user.email = email
                    request.user.save()
                    # 验证码置为已经使用
                    email_record.has_used = True
                    email_record.save()

                    # 写入消息
                    message = UserMessage()
                    message.user = request.user.id
                    message.message = '人家已经帮你把邮件修改好了'
                    message.save()

                    render_data['status'] = 'success'
                    render_data['email'] = '邮箱修改成功'
                    return HttpResponse(json.dumps(render_data), content_type='application/json')
                else:
                    render_data['email'] = '邮箱验证出错'
                    return HttpResponse(json.dumps(render_data), content_type='application/json')
            else:
                render_data['email'] = '邮箱验证出错'
                return HttpResponse(json.dumps(render_data), content_type='application/json')
        else:
            render_data['email'] = '邮箱验证出错'
            return HttpResponse(json.dumps(render_data), content_type='application/json')


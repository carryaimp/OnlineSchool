import json

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import View

from .models import Course, Lesson, CourseResource, Video
from operation.models import UserFavorite, UserCourse, CourseComment
from operation.forms import CourseCommentForm

from pure_pagination import Paginator, PageNotAnInteger
from tools.need_login import NeedLoginViewMinx


class CourseListView(View):
    """
    公开课列表展示页面，包含分页功能
    """
    def get(self, request):
        render_data = dict()
        all_course = Course.objects.all().order_by('-add_time')
        order_key = request.GET.get('sort', '')
        hot_course = all_course.order_by('-fav_num')[:3]
        # 排序
        if order_key:
            if order_key == 'hot':
                all_course = all_course.order_by('-fav_num')
            if order_key == 'students':
                all_course = all_course.order_by('-students')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, per_page=9, request=request)
        all_course = p.page(page)

        render_data['order_key'] = order_key
        render_data['all_course'] = all_course
        render_data['hot_course'] = hot_course
        return render(request, 'course/course-list.html', render_data)


class CourseDetailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        render_data = dict()
        if course_id:
            course = Course.objects.get(id=course_id)
            if course:
                render_data['course'] = course
                course.click_num += 1
                course.save()
                # 判断是否收藏
                has_fav_course = False
                has_fav_org = False
                # 判断用户是否登录
                if request.user.is_authenticated:
                    if UserFavorite.objects.filter(fav_id=course.id, fav_type=1):
                        has_fav_course = True
                    if UserFavorite.objects.filter(fav_id=course.org.id, fav_type=2):
                        has_fav_org = True
                    render_data['has_fav_course'] = has_fav_course
                    render_data['has_fav_org'] = has_fav_org
                else:
                    render_data['has_fav_course'] = has_fav_course
                    render_data['has_fav_org'] = has_fav_org
                category = course.category
                if category:
                    relate_course = Course.objects.filter(category__icontains=category)[:1]
                    render_data['relate_course'] = relate_course
                else:
                    render_data['relate_course'] = ''
                return render(request, 'course/course-detail.html', render_data)
            else:
                return redirect(to='index')
        else:
            return redirect(to='index')


class LessonView(NeedLoginViewMinx, View):
    """课程章节视频页面"""
    def get(self, request, course_id):
        page_label = 'lesson'
        if course_id:
            course = Course.objects.get(id=course_id)
            if course:
                # 保存用户学习学习课程
                if not UserCourse.objects.filter(user=request.user, course=course):
                    user_course = UserCourse(user=request.user, course=course)
                    user_course.save()

                # 找出学习了该课程的所有的用户
                user_id_list = [user.user.id for user in UserCourse.objects.filter(course=course)]
                # 找出这些用户ID对应的课程
                user_course = UserCourse.objects.filter(user__in=user_id_list)
                # 找出所有的课程ID
                course_id_list = [i.course.id for i in user_course]
                course_id_list.remove(course.id)
                # 获得推进课程
                relate_course = Course.objects.filter(id__in=course_id_list).order_by('-students')[:3]

                all_lesson = Lesson.objects.filter(course=course)
                all_course_resource = CourseResource.objects.filter(course=course)
                render_data = dict()
                render_data['course'] = course
                render_data['all_lesson'] = all_lesson
                render_data['all_course_resource'] = all_course_resource
                render_data['relate_course'] = relate_course
                render_data['page_label'] = page_label
                return render(request, 'course/course-video.html', render_data)
            else:
                return redirect(to='index')
        else:
            return redirect(to='index')


class CommentView(NeedLoginViewMinx, View):
    """
    课程评论页面
    """
    def get(self, request, course_id):
        page_label = 'comment'
        if course_id:
            course = Course.objects.get(id=course_id)
            if course:
                all_lesson = Lesson.objects.filter(course=course)
                # 所有章节信息
                all_course_resource = CourseResource.objects.filter(course=course)

                # 找出学习了该课程的所有的用户
                user_id_list = [user.user.id for user in UserCourse.objects.filter(course=course)]
                # 找出这些用户ID对应的课程
                user_course = UserCourse.objects.filter(user__in=user_id_list)
                # 找出所有的课程ID
                course_id_list = [i.course.id for i in user_course]
                course_id_list.remove(course.id)
                # 获得推进课程
                relate_course = Course.objects.filter(id__in=course_id_list).order_by('-students')[:3]

                # 课程评论
                all_commit = CourseComment.objects.filter(course=course).order_by('-add_time')
                render_data = dict()
                render_data['course'] = course
                render_data['all_lesson'] = all_lesson
                render_data['all_course_resource'] = all_course_resource
                render_data['relate_course'] = relate_course
                render_data['all_commit'] = all_commit
                render_data['page_label'] = page_label
                return render(request, 'course/course-comment.html', render_data)
            else:
                return redirect(to='index')
        else:
            return redirect(to='index')

    def post(self, request, course_id):
        """
        提交评论， ajax请求方式提交，需要返回json数据
        :param request:
        :param course_id:
        :return:
        """
        response_data = dict()
        # 验证用户是否登录
        if request.user.is_authenticated:
            course_comment_form = CourseCommentForm(request.POST)
            # 通过form类验证提交字段是否合法
            if course_comment_form.is_valid():
                course_comment_form.save()
                response_data['status'] = 'success'
                response_data['msg'] = '提交成功'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                response_data['status'] = 'fail'
                response_data['msg'] = '数据出错'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data['status'] = 'fail'
            response_data['msg'] = '用户未登录'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        
    
class VideoPlayView(NeedLoginViewMinx, View):
    def get(self, request, course_id, video_id):
        page_label = 'lesson'
        if video_id and course_id:
            course = Course.objects.get(id=course_id)
            if course:
                all_lesson = Lesson.objects.filter(course=course)
                # 所有章节信息
                all_course_resource = CourseResource.objects.filter(course=course)

                # 找出学习了该课程的所有的用户
                user_id_list = [user.user.id for user in UserCourse.objects.filter(course=course)]
                # 找出这些用户ID对应的课程
                user_course = UserCourse.objects.filter(user__in=user_id_list)
                # 找出所有的课程ID
                course_id_list = [i.course.id for i in user_course]
                course_id_list.remove(course.id)
                # 获得推进课程
                relate_course = Course.objects.filter(id__in=course_id_list).order_by('-students')[:3]

                # 课程评论
                all_commit = CourseComment.objects.filter(course=course).order_by('-add_time')
                # 视频相关
                video = Video.objects.get(id=video_id)

                render_data = dict()
                render_data['course'] = course
                render_data['all_lesson'] = all_lesson
                render_data['all_course_resource'] = all_course_resource
                render_data['relate_course'] = relate_course
                render_data['all_commit'] = all_commit
                render_data['video'] = video
                render_data['page_label'] = page_label
                return render(request, 'course/video-play.html', render_data)
            else:
                return redirect(to='index')


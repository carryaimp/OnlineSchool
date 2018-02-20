import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.db.models import Q

from .models import CourseOrg, City, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite

from pure_pagination import Paginator, PageNotAnInteger


class OrgListView(View):
    """课程机构列表页面"""
    def get(self, request):
        city_id = request.GET.get('city', '')
        category = request.GET.get('category', '')
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by('-click_num')[:3]
        sort_key = request.GET.get('sort', '')
        print(sort_key)
        # 前端对结果进行赛选
        keywords = request.GET.get('keywords', None)
        if keywords:
            all_org = all_org.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) |
                                     Q(category__icontains=keywords) | Q(address__icontains=keywords))
        # 按城市赛选
        if city_id:
            all_org = all_org.filter(city=city_id)
        # 按机构类型赛选
        if category:
            all_org = all_org.filter(category=category)
        # 按sort_key排序
        if sort_key == 'student':
            all_org = all_org.order_by('-student_num')
        if sort_key == 'course':
            all_org = all_org.order_by('-course_num')
        all_city = City.objects.all()
        org_num = all_org.count()

        # 获得页码, 并对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, per_page=5, request=request)
        # 进行分页
        all_org = p.page(page)

        return render(request, 'org/org-list.html', {
            'all_org': all_org,
            'all_city': all_city,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort_key': sort_key
        })


class AddAskView(View):
    """
    用户添加咨询，通过 form 中ModelForm实现验证完成后自动保存
    """
    def post(self, request):
        rep_data = dict()
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            # 通过form进行自动保存
            user_ask_form.save(commit=True)
            rep_data['status'] = 'success'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')
        else:
            rep_data['status'] = 'fail'
            rep_data['msg'] = '添加出错'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')


class OrgHome(View):
    """课程机构首页，需要通过org_id传递关联机构的课程和教师信息，并通过传递当前页面的标记实现选中状态"""
    def get(self, request, org_id):
        page_label = 'home'
        render_data = dict()
        if org_id > 0:
            try:
                org = CourseOrg.objects.get(id=org_id)
            except:
                return redirect(to='index')

            # 统计
            org.click_num += 1
            org.save()

            # 通过外键反查
            all_course = org.course_set.all()[:3]
            all_teacher = org.teacher_set.all()[:1]
            has_fav = False
            if UserFavorite.objects.filter(fav_id=org.id, fav_type=2):
                has_fav = True
            render_data['all_course'] = all_course
            render_data['all_teacher'] = all_teacher
            render_data['org'] = org
            render_data['page_label'] = page_label
            render_data['has_fav'] = has_fav
            return render(request, 'org/org-detail-homepage.html', render_data)
        else:
            return redirect(to='index')


class OrgDescView(View):
    """
    课程机构描叙页面
    """
    def get(self, request, org_id):
        page_label = 'desc'
        render_data = dict()
        if org_id > 0:
            try:
                org = CourseOrg.objects.get(id=org_id)
            except:
                return redirect(to='index')
            # 通过外键反查
            render_data['org'] = org
            render_data['page_label'] = page_label
            has_fav = False
            if UserFavorite.objects.filter(fav_id=org.id, fav_type=2):
                has_fav = True
            render_data['has_fav'] = has_fav
            return render(request, 'org/org-detail-desc.html', render_data)
        else:
            return redirect(to='index')


class OrgCourseView(View):
    """
    机构课程页面
    """
    def get(self, request, org_id):
        page_label = 'course'
        render_data = dict()
        if org_id:
            try:
                org = CourseOrg.objects.get(id=org_id)
            except:
                return redirect(to='index')
            # 通过外键反查
            all_course = org.course_set.all()
            has_fav = False
            if UserFavorite.objects.filter(fav_id=org.id, fav_type=2):
                has_fav = True
            render_data['all_course'] = all_course
            render_data['org'] = org
            render_data['page_label'] = page_label
            render_data['has_fav'] = has_fav
            return render(request, 'org/org-detail-course.html', render_data)
        else:
            return redirect(to='index')


class OrgTeacherView(View):
    def get(self, request, org_id):
        if org_id:
            try:
                org = CourseOrg.objects.get(id=org_id)
            except:
                return redirect(to='index')
            has_fav = True if UserFavorite.objects.filter(fav_id=org.id, fav_type=2) else False
            render_data = dict()
            all_teacher = Teacher.objects.filter(org=org)
            render_data['all_teacher'] = all_teacher
            render_data['org'] = org
            render_data['has_fav'] = has_fav
            return render(request, 'org/org-detail-teachers.html', render_data)
        else:
            return redirect(to='index')


class OrgTeacherListView(View):
    """机构教师页面"""
    def get(self, request):
        page_label = 'list'
        all_teacher = Teacher.objects.all()
        teacher_num = all_teacher.count()
        hot_teacher = all_teacher.order_by('-click_num')[:3]
        keywords = request.GET.get('keywords', None)
        # 搜索
        if keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=keywords) | Q(work_company__icontains=keywords) |
                                     Q(work_position__icontains=keywords) | Q(points__icontains=keywords))

        # 排序
        if request.GET.get('sort', None) == 'hot':
            page_label = 'hot'
            all_teacher = all_teacher.order_by('-click_num')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, per_page=5, request=request)
        # 进行分页
        all_teacher = p.page(page)

        render_data = dict()
        render_data['all_teacher'] = all_teacher
        render_data['teacher_num'] = teacher_num
        render_data['hot_teacher'] = hot_teacher
        render_data['page_label'] = page_label
        return render(request, 'teacher/teachers-list.html', render_data)


class OrgTeacherDetailView(View):
    """
    教师详情页面
    """
    def get(self, request, teacher_id):
        if teacher_id <= 0 or not teacher_id:
            return redirect(to='teacher')
        # 是否能查到此记录
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except:
            return redirect(to='teacher')
        # 统计
        teacher.click_num += 1
        teacher.save()

        render_data = dict()
        # 是否收藏判断
        has_teacher_fav = True if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3) else False
        has_org_fav = True if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2) else False
        all_course = teacher.get_all_course()
        hot_teacher = Teacher.objects.all().order_by('-fav_num')[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, per_page=8, request=request)
        # 进行分页
        all_course = p.page(page)

        render_data['teacher'] = teacher
        render_data['all_course'] = all_course
        render_data['hot_teacher'] = hot_teacher
        render_data['has_teacher_fav'] = has_teacher_fav
        render_data['has_org_fav'] = has_org_fav
        return render(request, 'teacher/teacher-detail.html', render_data)
import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View

from .models import CourseOrg, City
from .forms import UserAskForm

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
    def get(self, request, org_id):
        page_label = 'home'
        render_data = dict()
        if org_id:
            org = CourseOrg.objects.get(id=org_id)
            # 通过外键反查
            all_course = org.course_set.all()[:3]
            all_teacher = org.teacher_set.all()[:1]
            render_data['all_course'] = all_course
            render_data['all_teacher'] = all_teacher
            render_data['org'] = org
            render_data['page_label'] = page_label
            return render(request, 'org/org-detail-homepage.html', render_data)
        else:
            return redirect(to='index')


class OrgDescView(View):
    def get(self, request, org_id):
        page_label = 'desc'
        render_data = dict()
        if org_id:
            org = CourseOrg.objects.get(id=org_id)
            # 通过外键反查
            render_data['org'] = org
            render_data['page_label'] = page_label
            return render(request, 'org/org-detail-desc.html', render_data)
        else:
            return redirect(to='index')


class OrgCourseView(View):
    def get(self, request, org_id):
        page_label = 'course'
        render_data = dict()
        if org_id:
            org = CourseOrg.objects.get(id=org_id)
            # 通过外键反查
            all_course = org.course_set.all()
            render_data['all_course'] = all_course
            render_data['org'] = org
            render_data['page_label'] = page_label
            return render(request, 'org/org-detail-course.html', render_data)
        else:
            return redirect(to='index')


class OrgTeacherView(View):
    def get(self, request, org_id):
        page_label = 'teacher'
        if org_id:
            render_data = dict()
            org = CourseOrg.objects.get(id=org_id)
            # 通过外键反查
            all_teacher = org.teacher_set.all()
            render_data['all_teacher'] = all_teacher
            render_data['org'] = org
            render_data['page_label'] = page_label
            return render(request, 'org/org-detail-teachers.html', render_data)
        else:
            return redirect(to='index')
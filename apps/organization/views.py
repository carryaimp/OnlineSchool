from django.shortcuts import render
from django.views.generic.base import View

from .models import CourseOrg, City

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


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
        return render(request, 'org-list.html', {
            'all_org': all_org,
            'all_city': all_city,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort_key': sort_key
        })

import json

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View

from .forms import UserFavoriteForm
from .models import UserFavorite
from course.models import Course
from organization.models import CourseOrg, Teacher


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
            record = Course.objects.filter(id=fav_id)
            if not record:
                rep_data['status'] = 'fail'
                rep_data['msg'] = '收藏出错'
                return HttpResponse(json.dumps(rep_data), content_type='application/json')
        if fav_type == 2:
            record = CourseOrg.objects.filter(id=fav_id)
            if not record:
                rep_data['status'] = 'fail'
                rep_data['msg'] = '收藏出错'
                return HttpResponse(json.dumps(rep_data), content_type='application/json')
        if fav_type == 3:
            record = Teacher.objects.filter(id=fav_id)
            if not record:
                rep_data['status'] = 'fail'
                rep_data['msg'] = '收藏出错'
                return HttpResponse(json.dumps(rep_data), content_type='application/json')

        # 查看记录是否存在，存在则删除，不存在则添加
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_record:
            exist_record.delete()
            rep_data['status'] = 'success'
            rep_data['msg'] = '收藏'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')
        else:
            user_fav = UserFavorite()
            user_fav.user = request.user
            user_fav.fav_type = fav_type
            user_fav.fav_id = fav_id
            user_fav.save()

            rep_data['status'] = 'success'
            rep_data['msg'] = '已收藏'
            return HttpResponse(json.dumps(rep_data), content_type='application/json')

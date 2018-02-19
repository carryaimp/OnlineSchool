__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/19 9:56'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class NeedLoginViewMinx(object):
    """
    验证用户是否登录，如果没有登录跳转到登录页面
    """
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(NeedLoginViewMinx, self).dispatch(request, *args, **kwargs)
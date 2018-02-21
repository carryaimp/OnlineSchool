__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/20 23:08'

from django.shortcuts import render_to_response


def handler_404_error(request):
    """
    访问的url在站点不存在返回的错误，资源找不到
    :param request:
    :return:
    """
    response = render_to_response('handler_error/404.html', {})
    response.status_code = 404
    return response


def handler_500_error(request):
    """
    访问的url在站点不存在返回的错误，资源找不到
    :param request:
    :return:
    """
    response = render_to_response('handler_error/500.html', {})
    response.status_code = 500
    return response


def handler_403_error(request):
    """
    访问的url在站点不存在返回的错误，资源找不到
    :param request:
    :return:
    """
    response = render_to_response('handler_error/403.html', {})
    response.status_code = 403
    return response
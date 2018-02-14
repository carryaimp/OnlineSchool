__author__ = 'beimenchuixue'
__blog__ = 'http://www.cnblogs.com/2bjiujiu/'
__date__ = '2018/2/14 11:00'

import hashlib
import re

from random import sample
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from OnlineSchool.settings import EMAIL_FROM


def send_email(email_address=None, email_type='register'):
    # 用于发送邮件验证码，用于激活和忘记密码逻辑验证
    random_str = get_random_str(12)
    email_record = EmailVerifyRecord()
    email_record.code = random_str
    email_record.email = email_address
    email_record.send_type = email_type
    email_record.save()
    # 注册类型邮件
    if email_type == 'register':
        email_title = '云学在线账号激活'
        email_content = '请点击以下链接完成账号激活，如果不是本人忽略。http://127.0.0.1:8000/user/active/{code}'.format(code=random_str)
        send_status = send_mail(subject=email_title, message=email_content, from_email=EMAIL_FROM, recipient_list=[email_address])
        return send_status
    # 忘记密码重置密码邮件
    if email_type == 'forget':
        email_title = '云学在线账号修改密码'
        email_content = '请点击以下链接完成账号密码修改，如果不是本人忽略。http://127.0.0.1:8000/user/reset/{code}'.format(code=random_str)
        send_status = send_mail(subject=email_title, message=email_content, from_email=EMAIL_FROM,
                                recipient_list=[email_address])
        return send_status


def get_random_str(length=12):
    """获取随机码的哈希值"""
    choice_str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    m = hashlib.md5()
    m.update(''.join(sample(choice_str, length)).encode('utf-8'))
    return m.hexdigest()


def get_mail_url(email=None):
    """
    获取各自邮箱对应的url地址
    :param email:
    :return:
    """
    if email:
        label = re.split('[@.]', email)[1]
        tem_url = 'https://mail.{label}.com'.format(label=label)
        return tem_url
    else:
        return None


if __name__ == '__main__':
    # import os
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'OnlineSchool.settings'
    # import django
    # django.setup()
    # send_email(email_address='422083556@qq.com')
    # print(get_random_str())
    # import re
    # print(re.split('[.@]', '222@163.com')[1])
    print(get_mail_url('422@qq.com'))
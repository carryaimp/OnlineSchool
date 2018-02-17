#from django.test import TestCase

# Create your tests here.

import re


def re_match(mobile):
    REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
    p = re.compile(REGEX_MOBILE)
    return mobile if p.match(mobile) else None


if __name__ == '__main__':
    rep = re_match('15579811036')
    print(rep)

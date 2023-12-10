from django.http import HttpResponse

# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/10 17:13

def hello(request):
    return HttpResponse("Hello world ! ")

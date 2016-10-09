#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def index(request):
	context_dict={}
	context_dict['hi']='hi'
	return render(request,'dashboard/index.html',context_dict)
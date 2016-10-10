#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings

from dashboard.models import Messages

def index(request):
	context_dict = {}
	context_dict['hi'] = 'hi'
	context_dict['data'] = Messages.objects.all()[::-1]
	return render(request, 'dashboard/index.html', context_dict)

@csrf_exempt
def log_in(request):
	c={}
	# if request.method == 'POST':
	# 	email=request.POST.get('email')
	# 	batch=request.POST.get('batch')
	# 	c['email']=email
	# 	c['batch']=batch
	# 	return render(request,'dashboard/logged_in.html',c)
	c.update(csrf(request))
	return render(request,'login.html',c)

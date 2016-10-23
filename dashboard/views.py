#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from datetime import datetime
from dashboard.models import Messages,User
fb_id='hello'
def index(request):
	context_dict = {}
	context_dict['hi'] = 'hi'
	context_dict['data'] = Messages.objects.all()[::-1]
	response=render(request, 'dashboard/index.html', context_dict)
	#response.set_cookie("my_cookie","hello world")
	#print request.COOKIES.get('my_cookie','N/A')

	visits =  int(request.COOKIES.get('visits','1'))

	if 'last_visit' in request.COOKIES:
		last_visit = request.COOKIES['last_visit']
		last_visit_time= datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")

		if(datetime.now() - last_visit_time).seconds > 5:
			response.set_cookie('visits',visits+1)
			response.set_cookie('last_visit',datetime.now())
		else:
			pass
	else:
		response.set_cookie('last_visit',datetime.now())
	return response

def login(request):
	context_dict = {}
	if(request.method == 'GET'):
		fb_id=str(request.GET.get('fb_id'))
		print "fb id ***",fb_id,type(fb_id)
		context_dict['fb_id']=fb_id

	if(request.method == 'POST'):
		email=request.POST.get('email')
		batch=request.POST.get('batch')
		fb_id=request.POST.get('fb_id')
		context_dict['email']=email
		context_dict['batch']=batch
		context_dict['fb_id']=fb_id
		p=User.objects.get_or_create(fb_id=fb_id,
			email=email,
			batch=batch)[0]
		p.save()
		return render(request,'dashboard/logged_in.html',context_dict)


	return render(request, 'dashboard/login.html', context_dict)	

def web(request):
	return render(request,'dashboard/site.html')
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings

from dashboard.models import Messages,User

def index(request):
	context_dict = {}
	context_dict['hi'] = 'hi'
	context_dict['data'] = Messages.objects.all()[::-1]
	return render(request, 'dashboard/index.html', context_dict)
fb_id=''
def login(request):
	context_dict = {}
	if(request.method == 'GET'):
		fb_id=request.GET.get('fb_id')
	# context_dict['fb_id']=fb_id
	if(request.method == 'POST'):
		email=request.POST.get('email')
		batch=request.POST.get('batch')
		context_dict['email']=email
		context_dict['batch']=batch
		p=User.objects.get_or_create(fb_id=fb_id,
			email=email,
			batch=batch)[0]
		p.save()
		return render(request,'dashboard/logged_in.html',context_dict)


	return render(request, 'dashboard/login.html', context_dict)	

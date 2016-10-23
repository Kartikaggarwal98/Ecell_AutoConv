from django import template
import random,datetime
register= template.Library()

@register.simple_tag
def random_color_1():
	'''
		usage: background -color: {%% foo %%} !important
	'''
	r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
	return "rgb(%s,%s,%s)"%(r,g,b)

@register.simple_tag
def random_color_2():
	'''
		usage: background -color: {%% foo %%} !important
	'''
	r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
	return "rgb(%s,%s,%s)"%(r,g,b)

@register.simple_tag
def current_time(format_string):
	return datetime.datetime.now().strftime(format_string)

#TEMPLATE FILTERS
@register.filter(name='lower')
def lower(value):
	return value.lower()

@register.assignment_tag
def concat(a,b,c):
	return a+b+c


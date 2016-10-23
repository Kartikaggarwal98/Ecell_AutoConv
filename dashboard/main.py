
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from datetime import datetime
from dashboard.models import Messages,User
import sys
import time
import telepot
TOKEN='264775797:AAGFhQemU7tO6HlAPoD1mfYBdmo40IkBZts'

"""
$ python2.7 skeleton.py <token>
A skeleton for your telepot programs.
"""

def handle(msg):
    flavor = telepot.flavor(msg)

    summary = telepot.glance(msg, flavor=flavor)
    print flavor, summary


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)
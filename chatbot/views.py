#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import re
import random
import pprint
import apiai
# Create your views here.

from dashboard.models import Messages
APIAI_CLIENT_ACCESS_TOKEN= '0e76c8cfd8c44710aab2224c72d3aac7'
VERIFY_TOKEN = '7thseptember2016'
PAGE_ACCESS_TOKEN = 'EAAZAB0AYNpNkBADHRjDJ3ED9AcDjZC6r7m71bbWGXadBZCnHH0NHe77ZCEIV5neqZB7VohNHrzmHZALaIYvsVLcZBqWYX2RTxU3YmnaTXWvFqGzHVMbMCkVZC9o7RBeftXj6QIZC7plWs8GGzZAV5sGfQGhpZBrPAZCjrzSnvCQgUNwH3jtrJYNy57ZAA'

def domain_whitelist(domain='https://codingblocksdjango.herokuapp.com'):
    post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s"%(PAGE_ACCESS_TOKEN)
    response_object =     {
                "setting_type" : "domain_whitelisting",
                "whitelisted_domains" : [domain],
                "domain_action_type": "add"
              }
    response_msg = json.dumps(response_object)

    status = requests.post(post_message_url, 
                headers={"Content-Type": "application/json"},
                data=response_msg)

    logg(status.text,symbol='--WHT--')              

def domain_whitelist_2(domain='https://petersfancybrownhats.com'):
    post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s"%(PAGE_ACCESS_TOKEN)
    response_object =     {
                "setting_type" : "domain_whitelisting",
                "whitelisted_domains" : [domain],
                "domain_action_type": "add"
              }
    response_msg = json.dumps(response_object)

    status = requests.post(post_message_url, 
                headers={"Content-Type": "application/json"},
                data=response_msg)

    logg(status.text,symbol='--DOMHT--')   


def save_message(fbid='1129928563722136',message_text='hi'):
    url = 'https://graph.facebook.com/v2.6/%s?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=%s'%(fbid,PAGE_ACCESS_TOKEN)
    print url
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    name = '%s %s'%(data['first_name'],data['last_name'])
    p = Messages.objects.get_or_create(name=name,
      profile_url = data['profile_pic'],
      fb_id = fbid,
      gender = data['gender'],
      locale = data['locale'],
      message = message_text
      )[0]
    p.save()

    return json.dumps(data)

def scrape_spreadsheet():

  with open('sheet3.json') as data_file:
      data = json.loads(data_file.read())
  arr =[]

  for entry in data['feed']['entry']:
      d = {}
      for k,v in entry.iteritems():
          if k.startswith('gsx'):
              key_name = k.split('$')[-1]
              d[key_name] = entry[k]['$t']

      arr.append(d)

  return arr

def scrape_spreadsheet_2():
    sheet_id='1oHgUnqmGZs_C0oqTwQIUPN0gm54lImC7nA7Vfa7jkjM'
    #sheet_id = '1EXwvmdQV4WaMXtL4Ucn3kwwhS1GOMFu0Nh9ByVCfrxk'
    url = 'https://spreadsheets.google.com/feeds/list/%s/od6/public/values?alt=json'%(sheet_id)

    resp = requests.get(url=url)
    data = json.loads(resp.text)
    arr =[]

    for entry in data['feed']['entry']:
        d = {}
        for k,v in entry.iteritems():
            if k.startswith('gsx'):
                key_name = k.split('$')[-1]
                d[key_name] = entry[k]['$t']

        arr.append(d)

    return arr


def set_greeting_text():
    post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s"%(PAGE_ACCESS_TOKEN)
    
    request_msg = {
        "setting_type":"greeting",
          "greeting":{
            "text":"Hello {{user_first_name}}! Greetings from IEEE NSIT. \n See menu for options"
          }
    }
    response_msg = json.dumps(request_msg)

    status = requests.post(post_message_url, 
                headers={"Content-Type": "application/json"},
                data=response_msg)

    logg(status.text,symbol='--GR--')


def index(request):
    fbid= '1129928563722136'
    #status= set_menu()
    print "set menu!!!!"
    # response_msg= gen_response_object('1129928563722136','members')

    #set_greeting_text()
    #get_started_button()
    # gen_answer_object('1129928563722136',keyword='index error')
    #domain_whitelist()
    #domain_whitelist_2()
    status= handle_postback('1129928563722136','MENU_CHAPTER')

    # post_facebook_message('1129928563722136','members')
    # search_string = request.GET.get('text') or 'foo'
    # output_text = gen_response_object('fbid',item_type='members')

    # response_msg= {
    #     "recipient":{
    #         "id":fbid
    #       },
    #       "message":{
    #         "attachment":{
    #           "type":"template",
    #           "payload":{
    #             "template_type":"generic",
    #             "elements":[
    #                {
    #                 "title":"Welcome to Peter\'s Hats",
    #                 "image_url":"https://petersfancybrownhats.com/company_image.png",
    #                 "subtitle":"We\'ve got the right hat for everyone.",
    #                 "default_action": {
    #                   "type": "web_url",
    #                   "url": "https://petersfancybrownhats.com",
    #                   "messenger_extensions": True,
    #                   "webview_height_ratio": "tall",
    #                   "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
    #                 },
    #                 "buttons":[
    #                   {
    #                     "type":"web_url",
    #                     "url":"https://petersfancybrownhats.com",
    #                     "title":"View Website"
    #                   },{
    #                     "type":"postback",
    #                     "title":"Start Chatting",
    #                     "payload":"DEVELOPER_DEFINED_PAYLOAD"
    #                   }              
    #                 ]      
    #               }
    #             ]
    #           }
    #         }
    #       }
    # }
    # response_msg=json.dumps({"recipient":{"id":'1129928563722136'}, "message":{"text":"output_text"}})
    # response_msg= json.dumps(response_msg)
    # status = requests.post(post_message_url, 
    #                 headers={"Content-Type": "application/json"},
    #                 data=response_msg)
    return HttpResponse(status, content_type='application/json')

def get_started_button():
  post_message_url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s'%PAGE_ACCESS_TOKEN
  response_object= {
                    'get_started':{
                        'payload':'GET_STARTED_PAYLOAD'
                      }
  }
  start_object = json.dumps(response_object)
  status = requests.post(post_message_url,
          headers = {"Content-Type": "application/json"},
          data = start_object)

  logg(status.text,'-START-OBJECT-')

def set_menu():
    post_message_url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s'%PAGE_ACCESS_TOKEN
    
    response_object =   {
                          "setting_type" : "call_to_actions",
                          "thread_state" : "existing_thread",
                          "call_to_actions":[
                            {
                              "type":"postback",
                              "title":"About",
                              "payload":"MENU_HELP"
                            },
                            {
                              "type":"postback",
                              "title":"Members",
                              "payload":"MENU_MEMBER"
                            },
                            {
                              "type":"postback",
                              "title":"Events",
                              "payload":"MENU_EVENTS"
                            },
                            {
                              "type":"postback",
                              "title":"Chapters",
                              "payload":"MENU_CHAPTER"
                            },
                            {
                              "type":"postback",
                              "title":"Visit our Website",
                              "payload":"MENU_CALL"
                            }
                          ]
                        }

    menu_object = json.dumps(response_object)
    status = requests.post(post_message_url,
          headers = {"Content-Type": "application/json"},
          data = menu_object)

    logg(status.text,'-MENU-OBJECT-')
    return status

def gen_response_object(fbid,item_type='members'):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN

    spreadsheet_object = scrape_spreadsheet()
    item_arr = [i for i in spreadsheet_object if i['itemtype'] == item_type]
    elements_arr = []

    for i in item_arr:
        #print i
        sub_item = {
                        "title":i['itemname'],
                        "item_url":i['itemlink'],
                        "image_url":i['itempicture'],
                        "subtitle":i['itemdescription'],
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":i['itemlink'],
                            "title":"Open"
                          },
                          {
                            "type":"element_share"
                          }              
                        ]
                      }
        elements_arr.append(sub_item)


    response_object = {
              "recipient":{
                "id":fbid
              },
              "message":{
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":elements_arr
                  }
                }
              }
            }
    print response_object
    
    return response_object

def gen_response_object_1(fbid,item_type='members'):
    spreadsheet_object = scrape_spreadsheet()
    item_arr = [i for i in spreadsheet_object if i['etype'] == item_type]
    elements_arr = []

    for i in item_arr:
        sub_item = {
                        "title":i['ename'],
                        "item_url":i['elink'],
                        "image_url":i['epicture'],
                        "subtitle":i['ename'],
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":i['elink'],
                            "title":"Open"
                          },
                          {
                            "type":"element_share"
                          }              
                        ]
                      }
        elements_arr.append(sub_item)


    response_object = {
              "recipient":{
                "id":fbid
              },
              "message":{
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":elements_arr
                  }
                }
              }
            }
    print "-------------response object-----------------"
    return json.dumps(response_object)

def gen_answer_object(fbid,keyword='index error'):
      api_url = 'http://soapidjango.herokuapp.com/api/?q=%s'%(keyword)
      resp = requests.get(url=api_url)
      item_arr = json.loads(resp.text)

      elements_arr=[]
      for i in item_arr[:2]:
          sub_item = {
                          "title":"Question #%s"%(item_arr.index(i)),
                          "item_url": "http://stackoverflow.com/q/%s"%(i['id']),
                          "image_url":i['image'],
                          "subtitle":i['title'],
                          "buttons":[
                            {
                              "type":"web_url",
                              "url":i['answers'][0],
                              "title":"Answer 1",
                              "webview_height_ratio": "compact"
                            },
                            {
                              "type":"web_url",
                              "url":i['answers'][1],
                              "title":"Answer 2",
                              "webview_height_ratio": "compact"
                            },
                            {
                              "type":"element_share"
                            }              
                          ]
                        }
          elements_arr.append(sub_item)


      response_object = {
                "recipient":{
                  "id":fbid
                },
                "message":{
                  "attachment":{
                    "type":"template",
                    "payload":{
                      "template_type":"generic",
                      "elements":elements_arr
                    }
                  }
                }
              }

      return json.dumps(response_object)




      for i in item_arr:
          sub_item = {
                          "title":i['itemname'],
                          "item_url":i['itemlink'],
                          "image_url":i['itempicture'],
                          "subtitle":i['itemdescription'],
                          "buttons":[
                            {
                              "type":"web_url",
                              "url":i['itemlink'],
                              "title":"Open",
                              "webview_height_ratio": "compact"

                            },
                            {
                              "type":"element_share"
                            }              
                          ]
                        }
          elements_arr.append(sub_item)


      response_object = {
                "recipient":{
                  "id":fbid
                },
                "message":{
                  "attachment":{
                    "type":"template",
                    "payload":{
                      "template_type":"generic",
                      "elements":elements_arr
                    }
                  }
                }
              }

      return json.dumps(response_object)

def post_facebook_message(fbid,message_text):
    print message_text,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    message_text = message_text.lower()
    # save_message(fbid,message_text)
    if message_text in 'members,event,chapter'.split(','):
        output_text = gen_response_object(fbid,item_type=message_text)
        response_msg= json.dumps(output_text)
    elif message_text == 'about':
        output_text= 'Started back in 2001, IEEE-DIT has now grown into a multi-faceted chapter, empowering young engineers to enhance their skills and set up milestones in the history of IEEE NSIT. Our foremost objective is to create an environment which promotes students to learn technical knowledge, inculcate managerial skills and develop their overall personalities. We achieve this by sponsoring technical projects, providing opportunities to manage and organize events and to participate in various events and conferences at state as well as national level.'
        response_msg=json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
    elif message_text == 'call':
        output_text= 'http://ieeensit.org'
    elif message_text=="get_started":
      output_text="Welcome to IEEE NSIT Bot! \n Send us your query or see Menu for Help"
      response_msg=json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})

    elif message_text.startswith('/ask'):
        query = message_text.replace('/ask','')
        output_text = gen_answer_object(fbid,query)
    else:
      ai = apiai.ApiAI(APIAI_CLIENT_ACCESS_TOKEN)
        
      request = ai.text_request()
      request.query = message_text

      response = json.loads(request.getresponse().read())

      result = response['result']
      print result

      output_text= response['result']['fulfillment']['speech']
      print(u"< %s" % output_text) 
      response_msg=json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
    
    # response_msg_1={"message": {"attachment": {"type": "template", "payload": {"template_type": "generic", "elements": [{"buttons": [{"url": "http://codingblocks.com/", "type": "web_url", "title": "Open"}, {"type": "element_share"}], "subtitle": "...", "item_url": "http://codingblocks.com/", "image_url": "http://codingblocks.com/wp-content/uploads/2015/12/Team_manmohan-150x150.png", "title": "Manhoman Gupta"}, {"buttons": [{"url": "http://codingblocks.com/", "type": "web_url", "title": "Open"}, {"type": "element_share"}], "subtitle": "...", "item_url": "http://codingblocks.com/", "image_url": "http://codingblocks.com/wp-content/uploads/2015/12/Team_anushray-150x150.png", "title": "Anushray Gupta"}]}}}, "recipient": {"id": "1129928563722136"}}  
    # print response_msg
 
    status = requests.post(post_message_url, 
                    headers={"Content-Type": "application/json"},
                    data=response_msg)
    return status


def handle_postback(fbid,payload):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    output_text = 'Payload Recieved: ' + payload
    logg(payload,symbol='*')
    if payload == "GET_STARTED_PAYLOAD":
      print "get started"
      return post_facebook_message(fbid,'get_started')
    if payload == 'MENU_ABOUT':
        return post_facebook_message(fbid,'about')
    elif payload == 'MENU_MEMBER':
        return post_facebook_message(fbid,'members')
    elif payload == 'MENU_CHAPTER':
        return post_facebook_message(fbid,'chapter')
    elif payload=='MENU_EVENTS':
        return post_facebook_message(fbid,'event')
    elif payload == 'MENU_WHY':
        response_object = {
                        "recipient":{
                          "id":fbid
                        },
                        "message":{
                          "attachment":{
                            "type":"template",
                            "payload":{
                              "template_type":"button",
                              "text":"What do you want to do next?",
                              "buttons":[
                                  {
                                                  "type":"web_url",
                                                  "url":"http://codingblocksdjango.herokuapp.com/login?fb_id=%s"%(fbid),
                                                  "title":"Select Criteria",
                                                  "webview_height_ratio": "compact"
                                                }
                              ]
                            }
                          }
                        }
                      }
        response_msg = json.dumps(response_object)
        requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        
    elif payload == "MENU_HELP":
        output_text = 'This is IEEE NSIT. Started back in 2001, IEEE-DIT has now grown into a multi-faceted chapter, empowering young engineers to enhance their skills and set up milestones in the history of IEEE NSIT. Our foremost objective is to create an environment which promotes students to learn technical knowledge, inculcate managerial skills and develop their overall personalities.'
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    
    elif payload == 'MENU_CALL':
        return post_facebook_message(fbid,'call')    

    #return

def logg(message,symbol='-'):
    print '%s\n %s \n%s'%(symbol*10,message,symbol*10)


def handle_quickreply(fbid,payload):
    if not payload:
        return
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    logg(payload,symbol='-QR-')
    if payload.split(':')[0] == payload.split(':')[-1]:
         logg("COrrect Answer",symbol='-YES-')
         output_text = 'Correct Answer'
         giphy_image_url = giphysearch(keyword='Yes,right,correct')
    else:
        logg("Wrong Answer",symbol='-NO-')
        output_text = 'Wrong answer'
        giphy_image_url =giphysearch(keyword='NO,wrong,bad')
    response_msg = json.dumps({"recipient":{"id":fbid}, 
        "message":{"text":output_text}})
    response_msg_image = {

            "recipient":{
                "id":fbid
              },
              "message":{
                "attachment":{
                  "type":"image",
                  "payload":{
                    "url": giphy_image_url
                  }
                }
              }

    } 
    response_msg_image = json.dumps(response_msg_image)
    status = requests.post(post_message_url, 
        headers={"Content-Type": "application/json"},
        data=response_msg)
    status = requests.post(post_message_url, 
        headers={"Content-Type": "application/json"},
        data=response_msg_image)
    return

class MyChatBotView(generic.View):
    def get (self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Oops invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message= json.loads(self.request.body.decode('utf-8'))
        
        logg(incoming_message)

        for entry in incoming_message['entry']:
            for message in entry['messaging']:

                try:
                    if 'postback' in message:
                        handle_postback(message['sender']['id'],message['postback']['payload'])
                        return HttpResponse()
                    else:
                        pass
                except Exception as e:
                    logg(e,symbol='-315-')

                try:
                    if 'quick_reply' in message['message']:
                        handle_quickreply(message['sender']['id'],
                            message['message']['quick_reply']['payload'])
                        return HttpResponse()
                    else:
                        pass
                except Exception as e:
                    logg(e,symbol='-325-')
                
                try:
                    sender_id = message['sender']['id']
                    message_text = message['message']['text']
                    post_facebook_message(sender_id,message_text) 
                except Exception as e:
                    logg(e,symbol='-332-')

        return HttpResponse()  


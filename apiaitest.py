import apiai
import os
import sys
import json




# demo agent acess token: e5dc21cab6df451c866bf5efacb40178

CLIENT_ACCESS_TOKEN = '0e76c8cfd8c44710aab2224c72d3aac7'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
user_message = 'hi'

        
request = ai.text_request()
request.query = user_message

response = json.loads(request.getresponse().read())

result = response['result']
print result


print(u"< %s" % response['result']['fulfillment']['speech'])

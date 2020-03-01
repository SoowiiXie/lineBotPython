from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage

import http.client, json
from PythyAPI.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

host = 'runnableqna.azurewebsites.net'  #主機
endpoint_key = "21191be3-17c2-4433-a13f-b80cd2597ec2"  #授權碼
kb = "bb0bd10e-1088-4e9e-9aed-661efdcded39"  #GUID碼
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

def sendQnA(event, mtext, userid):  #QnA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    if 'No good match' in result1:
        text1 = '很抱歉，資料庫中無適當解答！\n請再輸入問題。'
        #將沒有解答的問題寫入資料庫
        #userid = event.source.user_id
        #unit = users.objects.create(uid=userid, question=mtext)
        #unit.save()
        unit = users.objects.get(uid=userid)
        unit.question = mtext
        unit.save()
    else:
        result2 = result1[2:]  #移除「A：」
        text1 = result2  
    message = TextSendMessage(text = text1)
    line_bot_api.reply_message(event.reply_token,message)

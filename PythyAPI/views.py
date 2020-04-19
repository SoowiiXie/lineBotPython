from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from PythyAPI.models import users
from module import func51location
from module import func63button
from module import func64dateTime
from module import func75liff
#from module import func8QnA
from module import func9LUIS
from module import func10login
from module import func11translate
from module import func12liff

import variable_settings as varset
from urllib.parse import parse_qsl
#Postback裡的action使用

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                userid = event.source.user_id
                userPictureUrl = event.source.pictureUrl
                userid, lang, sound = readData(event)
                if not users.objects.filter(uid=userid).exists():
                    unit = users.objects.create(uid=userid, state='no')#10
                    unit.save()
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext in ['?','？','選單','menu',"目錄","help",\
                                 "你好","hi","hello","."]:
                        func63button.sendButton(event)
                        
                    elif mtext == '本期':
                        func10login.showCurrent(event)
                        
                    elif mtext == '前期':
                        func10login.showOld(event)
                        
                    elif len(mtext) == 3 and mtext.isdigit():
                        func10login.show3digit(event, mtext, userid)
    
                    elif len(mtext) == 5 and mtext.isdigit():
                        func10login.show5digit(event, mtext, userid)

                    elif mtext[:3] == 'ttt' and len(mtext) > 3:
                        mtext = mtext[3:]
                        func11translate.sendTranslate(event, lang, sound, mtext)
                        
                    elif mtext == '@取消':
                        func12liff.sendCancel(event, userid)
                        
                    elif mtext[:3] == '###' and len(mtext) > 3:  #處理LIFF傳回的FORM資料
                        func12liff.manageForm(event, mtext, userid)
                        
                    elif mtext[:9] == 'soowiiSay' and len(mtext) > 9:  #推播給所有顧客
                        func12liff.pushMessage(event, mtext)
                        
                    else:  #一般性輸入
                        func9LUIS.sendLUIS(event, mtext, userid)
                        
            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                userPictureUrl, userid, lang, sound = readData(event)
                #第一種id取得法
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback的data資料
                if backdata.get('action') == 'sellDate':
                    func64dateTime.sendData_sell(event, backdata)
                elif backdata.get('action') == 'func51':
                    func51location.sendPosition(event, backdata)
                elif backdata.get('action') == 'func64':
                    func64dateTime.sendDatetime(event, backdata)
                elif backdata.get('action') == 'func75':
                    func75liff.sendFlex(event, backdata, userid, userPictureUrl)
                elif backdata.get('action') == 'func9':
                    func9LUIS.sendUse(event, backdata)
                elif backdata.get('action') == 'func11':
                    func11translate.setElselang(event)
                elif backdata.get('action') == 'yes':
                    func12liff.sendYes(event, userid)
                elif backdata.get('action') == 'no':
                    func12liff.sendNo(event)
                else:
                    func11translate.sendData(event, backdata, sound, userid)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def readData(event):  #讀取使用者id,語言及發音設定
    userid = event.source.user_id  #第二種id取得法
    try:  
        data = varset.get(userid)  #讀取語言及發音設定
        datalist = data.split('/')
        lang = datalist[0]
        sound = datalist[1]
    except:  #第一次使用時做使用者初始設定
        varset.set(userid, 'en/yes')
        lang = 'en'
        sound = 'yes'
    return userid, lang, sound
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import func51location
from module import func63button
from module import func64dateTime
from module import func75liff
# =============================================================================
# from module import func8QnA
# =============================================================================
from module import func9LUIS
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
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext in ['?','？','選單','menu',"目錄","help",\
                                 "你好","hi","hello","."]:
                        func63button.sendButton(event)
                        
                    elif mtext[:3] == '###' and len(mtext) > 3:
                        func75liff.manageForm(event, mtext)
                        
                    else:  #一般性輸入
                        func9LUIS.sendLUIS(event, mtext)
                        
            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
                if backdata.get('action') == 'sellDate':
                    func64dateTime.sendData_sell(event, backdata)
                elif backdata.get('action') == 'func51':
                    func51location.sendPosition(event, backdata)
                elif backdata.get('action') == 'func64':
                    func64dateTime.sendDatetime(event, backdata)
                elif backdata.get('action') == 'func75':
                    func75liff.sendFlex(event, backdata)
                elif backdata.get('action') == 'func9':
                    func9LUIS.sendUse(event, backdata)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

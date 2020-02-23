from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage,\
PostbackTemplateAction, ButtonsTemplate

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                                     #顯示的圖片
                thumbnail_image_url='https://upload.cc/i1/2020/02/23/CrfWMt.png',
                title='可以跑就是Runnable',  #主標題
                text='請選擇服務：',  #副標題
                actions=[
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='傳送位置',
                        #text='@購買披薩'
                        data='action=func51'  #Postback資料
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='傳送時間',
                        #text='@購買披薩'
                        data='action=func64'  #Postback資料
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='傳送Flex',
                        #text='@購買披薩'
                        data='action=func75'  #Postback資料
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='其他使用說明',  #按鈕文字
                        #text='@購買披薩',  #顯示文字計息
                        data='action=func9'  #Postback資料
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='sendButton發生錯誤！'))
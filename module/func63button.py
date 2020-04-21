from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage,\
PostbackTemplateAction, ButtonsTemplate
import json
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendButton(event, user_profile_json):  #按鈕樣版
    user_profile_loads = json.loads(user_profile_json)
    if (user_profile_loads["picture_url"] is None):
        mb_line_pic = 'https://upload.cc/i1/2020/02/23/CrfWMt.png'
    else :
        mb_line_pic = user_profile_loads["picture_url"]
    if (user_profile_loads["status_message"] == "" or user_profile_loads["status_message"] is None):
        mb_line_status = "I Runn Able"
    else :
        mb_line_status = user_profile_loads["status_message"]
    try:
        message = TemplateSendMessage(
            alt_text='所有功能',
            template=ButtonsTemplate(
                #顯示的圖片
                thumbnail_image_url = mb_line_pic,
                title="你知道嗎？",  #主標題
                #title='可以跑就是Runnable',  #主標題
                text='偉大的'+user_profile_loads["display_name"]+'曾說過：'+mb_line_status,  #副標題
                actions=[
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='傳送位置',
#                        text='"'+user_profile_loads["user_id"]+"'我'"+\
#                                 mb_line_pic+"'我'"+\
#                                 user_profile_loads["display_name"]+"'我'"+\
#                                 mb_line_status+"'",
                        data='action=func51'  #Postback資料
                    ),
# =============================================================================
#                     PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
#                         label='傳送時間',
#                         #text='@購買披薩'
#                         data='action=func64'  #Postback資料
#                     ),
# =============================================================================
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='ttt翻譯',
                        #text='@購買披薩'
                        data='action=func11'  #Postback資料
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='Runn-able就是可以跑',
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
from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,LocationSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendPosition(event, backdata):  #傳送位置
    try:
        message = LocationSendMessage(
            title='資策會',
            address='320桃園市中壢區中大路300號',
            latitude=24.9664599,  #緯度
            longitude=121.1889883  #經度
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
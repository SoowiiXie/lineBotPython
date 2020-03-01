from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, AudioSendMessage

import variable_settings as varset
from translate import Translator
from urllib.parse import quote

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def setLang(event, lang, sound, userid):  #設定翻譯語言
    try:
        varset.set(userid, lang + '/' + sound)
        message = TextSendMessage(alt_text="語言設定",text = '語言設定為：' +\
                                  langtoword(lang))
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
def setElselang(event):  #設定其他語言
    try:
        message = TextSendMessage(
            alt_text="其他語言",
            text = '請選擇語言：',
            quick_reply = QuickReply(  #使用快速選單
                items = [
                    QuickReplyButton(
                        action = PostbackAction(label='英文', data='item=en')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='日文', data='item=ja')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='韓文', data='item=ko')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='泰文', data='item=th')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='越南文', data='item=vi')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='法文', data='item=fr')
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
def sendTranslate(event, lang, sound, mtext):  #翻譯及朗讀
    try:
        translator = Translator(from_lang="zh-Hant", to_lang=lang)  
        #來源是中文,翻譯後語言為lang
        translation = translator.translate(mtext)  #進行翻譯
        text = quote(translation)
        stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query='\
        + text + '&language=' + lang  #使用google語音API
        message = [  #若要發音需傳送文字及語音,必須使用陣列
            TextSendMessage(alt_text="文字翻譯",text = translation),#傳送翻譯後文字
            AudioSendMessage(alt_text="語音翻譯",\
                             original_content_url = stream_url,duration=20000),#傳送語音
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
def sendData(event, backdata, sound, userid):  #設定其他語言
    lang = backdata.get('item')  #取得快速選單的選取值
    setLang(event, lang, sound, userid)  #設定翻譯語言
    
def langtoword(lang):  #將語言代碼轉為中文字
    if lang == 'en':  word = '英文'
    elif lang == 'ja':  word = '日文'
    elif lang == 'ko':  word = '韓文'
    elif lang == 'th':  word = '泰文'
    elif lang == 'vi':  word = '越南文'
    elif lang == 'fr':  word = '法文'
    return word


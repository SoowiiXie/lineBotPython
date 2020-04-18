from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,\
ConfirmTemplate,PostbackTemplateAction

from PythyAPI.models import teamUp, users

import peewee #20200418
from datetime import date #20200418

db = peewee.PostgresqlDatabase('daqfqhdshludoq',
                          user='tlnlkxrtnbepdl',
                          password='2a372ee7bedb7e93309cb56336a42fe8824885adb6a6509d27d86cdba914c5d3',
                          host='ec2-52-86-73-86.compute-1.amazonaws.com',
                          port=5432)

db.connect() #20200418

print("VO---------------------------------#20200418")
#table
class GROUPER(peewee.Model):
    #col
    GRP_NO = peewee.CharField()
    MB_ID = peewee.CharField()
    LOC_NO = peewee.CharField()
    GRP_APPLYSTART = peewee.DateField()
    GRP_APPLYEND = peewee.DateField()
    GRP_START = peewee.DateField()
    GRP_END = peewee.DateField()
    GRP_NAME = peewee.CharField()
    GRP_CONTENT = peewee.CharField()
    GRP_PERSONMAX = peewee.IntegerField
    GRP_PERSONMIN = peewee.IntegerField
    GRP_PERSONCOUNT = peewee.IntegerField
    GRP_STATUS = peewee.IntegerField
    GRP_FOLLOW = peewee.IntegerField
    
    #db
    class Meta:
        database = db

#table
class GRP_DETAIL(peewee.Model):
    #col
    participants = peewee.ForeignKeyField(GROUPER, backref='participatingGroups')
    GRP_NO = peewee.CharField()
    MB_ID = peewee.CharField()
    GRP_REGISTER = peewee.IntegerField

    #db
    class Meta:
        database = db


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendCancel(event, user_id):  #取消訂房
    try:
        if teamUp.objects.filter(bid=user_id).exists():  #已有訂房記錄
            teamUpdata = teamUp.objects.get(bid=user_id)  #讀取訂房資料
            place = teamUpdata.place
            amount = teamUpdata.amount
            timein = teamUpdata.timein
            text1 = "您的揪團資料如下："
            text1 += "\n場地：" + place
            text1 += "\n人數：" + amount + " 人"
            text1 += "\n日期：" + timein.replace("T","\n時間：")
            message = [
                TextSendMessage(  #顯示訂房資料
                    text = text1
                ),
                TemplateSendMessage(  #顯示確認視窗
                    alt_text='取消揪團確認',
                    template=ConfirmTemplate(
                        text='你確定要取消揪團嗎？',
                        actions=[
                            PostbackTemplateAction(  #按鈕選項
                                label='是',
                                data='action=yes'
                            ),
                            PostbackTemplateAction(
                                label='否',
                                data='action=no'
                           )
                        ]
                    )
                )
            ]
        else:  #沒有訂房記錄
            message = TextSendMessage(
                text = '您目前沒有揪團！'
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='sendCancel發生錯誤！'))

def manageForm(event, mtext, user_id):  #處理LIFF傳回的FORM資料
    try:
        if not (teamUp.objects.filter(bid=user_id).exists()):  #沒有訂房記錄
            flist = mtext[3:].split('/')  #去除前三個「#」字元再分解字串
            place = flist[0]  #取得輸入資料
            amount = flist[1]
            timein = flist[2]
            unit = teamUp.objects.create(bid=user_id, place=place, amount=amount,\
                                          timein=timein)  #寫入資料庫
            
            print(timein)
            participant = GROUPER.create(name=user_id, LOC_NO=place,\
                                         GRP_PERSONMAX=amount,GRP_START=timein)
            
            unit.save()
            text1 = "您的揪團資料如下："
            text1 += "\n場地：" + place
            text1 += "\n人數：" + amount + " 人"
            text1 += "\n日期：" + timein.replace("T","\n時間：")
            message = TextSendMessage(  #顯示訂房資料
                text = text1
            )
        else:  #已有訂房記錄
            message = TextSendMessage(
                text = '您目前已有揪團，不能再揪團。'
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text=timein,'manageForm發生錯誤！'))

def sendYes(event, user_id):  #處理取消訂房
    try:
        datadel = teamUp.objects.get(bid=user_id)  #從資料庫移除資料記錄
        datadel.delete()
        message = TextSendMessage(
            text = "您的揪團已成功刪除。\n謝謝！"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='sendYes發生錯誤！'))
        
def sendNo(event):  #處理取消訂房
    try:
        message = TextSendMessage(
            text = "您的揪團沒被刪除。"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='sendNo發生錯誤！'))

def pushMessage(event, mtext):  ##推播訊息給所有顧客
    try:
        msg = mtext[6:]  #取得訊息
        userall = users.objects.all()
        for user in userall:  #逐一推播
            message = TextSendMessage(
                text = msg
            )
            line_bot_api.push_message(to=user.uid, messages=[message])  #推播訊息
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='pushMessage發生錯誤！'))

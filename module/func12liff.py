from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,\
ConfirmTemplate,PostbackTemplateAction

from PythyAPI.models import teamUp, users
from PythyAPI.modelsPG import GROUPER, ORDERS

import datetime #20200418
import peewee #20200419
import json #20200420
db = peewee.PostgresqlDatabase('d5o37ss0mrmndl',
                          user='rcccchvvxjnxbw',
                          password='42bc0d8ef563d2f91b1b2bfb222fdcc3900f9368f2ed287c30b06fbbcf7e6469',
                          host='ec2-3-231-16-122.compute-1.amazonaws.com',
                          port=5432)

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
            db.connect()                                       #2020-04-18T13:02
            date_time_obj = datetime.datetime.strptime(timein, '%Y-%m-%dT%H:%M')
            participant = GROUPER.create(MB_ID=user_id, LOC_NO=place,\
                                         GRP_PERSONMAX=int(amount),\
                                         GRP_START=date_time_obj)
            
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
        db.close()
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='manageForm發生錯誤！'))

def manageOrders(event, mtext, user_id, user_profile_json):  #處理LIFF傳回的FORM資料
    user_profile_loads = json.loads(user_profile_json)
    try:
        flist = mtext[3:].split('/')  #去除前三個「#」字元再分解字串
        mb_id = flist[0]  #取得輸入資料
        gender = flist[1]
        phone = flist[2]
        
        db.connect()
        LineUpdate = ORDERS.select().where(ORDERS.MB_ID == mb_id).get()
        LineUpdate.MB_LINE_ID = user_id
        LineUpdate.MB_LINE_DISPLAY = user_profile_loads["display_name"]
        if (user_profile_loads["picture_url"] is not None):
            LineUpdate.MB_LINE_PIC = user_profile_loads["picture_url"]
        if not (user_profile_loads["status_message"] == "" or user_profile_loads["status_message"] is None):
            LineUpdate.MB_LINE_STATUS = user_profile_loads["status_message"]
        LineUpdate.save(),'#returns:1'
        query = ORDERS.select().where(ORDERS.MB_ID == mb_id)
        count = 0
        text1 = "您的\n"
        for order in query:
            OS=order.OD_STATUS
            if(OS==1):OSinCH="發貨中"
            if(OS==2):OSinCH="已發貨"
            if(OS==3):OSinCH="已到達"
            if(OS==4):OSinCH="已取貨"
            if(OS==5):OSinCH="退貨"
            count+=1
            text1 += "第"+str(count)+"筆訂單資料如下："
            text1 += "\n帳號：" + order.MB_ID
            text1 += "\n訂單編號：" + order.OD_NO
            text1 += "\n狀態：" + OSinCH + "\n"
        message = TextSendMessage(  #顯示訂房資料
            text = text1
        )
        db.close()
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='manageOrders發生錯誤！'))

def sendYes(event, user_id):  #處理取消訂房
    try:
        datadel = teamUp.objects.get(bid=user_id)  #從資料庫移除資料記錄
        datadel.delete()
        db.connect()
        query = GROUPER.delete().where(GROUPER.MB_ID==user_id)
        query.execute()
        message = TextSendMessage(
            text = "您的揪團已成功刪除。\n謝謝！"
        )
        db.close()
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
        msg = mtext[9:]  #取得訊息
        userall = users.objects.all()
        for user in userall:  #逐一推播
            message = TextSendMessage(
                text = msg
            )
            line_bot_api.push_message(to=user.uid, messages=[message])  #推播訊息
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='pushMessage發生錯誤！'))

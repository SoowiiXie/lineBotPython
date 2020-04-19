from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction
from PythyAPI.models import teamUp

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendFlex(event, backdata, user_id):  #彈性配置
    try:
        if not (teamUp.objects.filter(bid=user_id).exists()):  #沒有訂房記錄
            bubble = BubbleContainer(
                direction='ltr',  #項目由左向右排列
                header=BoxComponent(  #標題
                    layout='vertical',
                    contents=[
                        TextComponent(text='可以跑就是Runn-able', weight='bold', size='xl'),
                    ]
                ),
                hero=ImageComponent(  #主圖片
                    url='https://upload.cc/i1/2020/02/23/CrfWMt.png',
                    size='full',
                    aspect_ratio='792:555',  #長寬比例
                    aspect_mode='cover',
                ),
                body=BoxComponent(  #主要內容
                    layout='vertical',
                    contents=[
                        TextComponent(text='按讚、留言，加meToo', size='md'),
                        BoxComponent(
                            layout='baseline',  #水平排列
                            margin='md',
                            contents=[
                                TextComponent(text='按', size='md', color='#999999',flex=0),
                                IconComponent(size='lg',\
                                              url='https://upload.cc/i1/2020/04/19/NLBGdU.png'),
                                TextComponent(text='、 ', size='md', color='#999999',flex=0),
                                IconComponent(size='md',\
                                              url='https://upload.cc/i1/2020/04/19/D7mc9a.png'),
                                TextComponent(text='  ，加me ', size='md', color='#999999', flex=0),
                                IconComponent(size='lg',\
                                              url='https://upload.cc/i1/2020/04/19/DlaV4C.png'),
                            ]
                        ),
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    contents=[
                                        TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                        TextComponent(text='320桃園市中壢區中大路300號', color='#666666', size='sm', flex=5)
                                    ],
                                ),
                                SeparatorComponent(color='#0000FF'),
                                BoxComponent(
                                    layout='baseline',
                                    contents=[
                                        TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                        TextComponent(text="08:30 - 22:30", color='#666666', size='sm', flex=5),
                                    ],
                                ),
                            ],
                        ),
                        BoxComponent(  
                            layout='horizontal',
                            margin='xxl',
                            contents=[
                                ButtonComponent(
                                    style='link',
                                    height='sm',
                                    action=URIAction(label='點我查看商城訂單目前狀態',\
                                                     uri="https://liff.line.me/1653880251-yZpK05QY"),                                    
                                )
                            ]
                        ),
                        BoxComponent(  
                            layout='horizontal',
                            margin='xxl',
                            contents=[
                                ButtonComponent(
                                    style='secondary',
                                    height='sm',
                                    action=URIAction(label='電話', uri='tel:034257387'),
                                ),
                                ButtonComponent(
                                    style='primary',
                                    height='sm',
                                    action=URIAction(label='揪團',\
                                                     uri="line://app/1653880251-4b2aDNMl")
                                )
                            ]
                        )
                    ],
                ),
                footer=BoxComponent(  #底部版權宣告
                    layout='vertical',
                    contents=[
                        TextComponent(text='Copyright@III DA106 Group5', color='#888888', size='sm', align='center'),
                    ]
                ),
            )
            message = FlexSendMessage(alt_text="準備揪團", contents=bubble)
        else:  #已有訂房記錄
            message = TextSendMessage(
                text = '您目前已有揪團，不能再揪團。'
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='sendFlex發生錯誤！'))

def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        text1 = '姓名：' + flist[0] + '\n'
        text1 += '日期：' + flist[1] + '\n'
        text1 += '場地：' + flist[2]
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='manageForm發生錯誤！'))

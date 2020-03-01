from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage
from module import func8QnA

import requests
import twder  #匯率套件
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

user_key = "CWB-77235BD2-2020-4346-A37E-DEE22EB1D2D8"
doc_name = "F-C0032-001"

cities = ["臺北","新北","桃園","臺中","臺南","高雄","基隆","新竹","嘉義"]  #市
counties = ["苗栗","彰化","南投","雲林","嘉義","屏東","宜蘭","花蓮","臺東","澎湖",\
            "金門","連江"]  #縣
currencies = {'美金':'USD','美元':'USD','港幣':'HKD','英鎊':'GBP','澳幣':'AUD',\
              '加拿大幣':'CAD','加幣':'CAD','新加坡幣':'SGD','新幣':'SGD',\
              '瑞士法郎':'CHF','瑞郎':'CHF','日圓':'JPY','日元':'JPY','日幣':'JPY',\
              '南非幣':'ZAR','瑞典幣':'SEK','紐元':'NZD','紐幣':'NZD','泰幣':'THB',\
              '泰銖':'THB','菲國比索':'PHP','菲律賓幣':'PHP','印尼幣':'IDR',\
              '歐元':'EUR','韓元':'KRW','馬幣':'MYR','韓幣':'KRW','越南盾':'VND',\
              '越南幣':'VND','馬來幣':'MYR','人民幣':'CNY' }  #幣別字典
keys = currencies.keys()

def sendUse(event, backdata):  #使用說明
    try:
        text1 ='''0.若要取消揪團
請輸入「@取消」

1.查詢縣或直轄市的天氣：
輸入「XX天氣如何?」
或輸入類似「XX有下雨嗎?」
例如「台中有起霧嗎?」

2.查詢現在台銀的匯率：
輸入「XX匯率為多少?」
或輸入類似
「XX一元換新台幣多少元?」
例如「日幣等於多少元台幣」

3.發票對獎:
輸入發票末三碼
例如「168」
或輸入「本期」或「前期」

4.翻譯(預設翻成英文):
點「ttt翻譯」並選擇好語言後
輸入「ttt」在要翻譯的中/英文前面
例如「tttAngela好聰明!」

若是其他問題
請直接輸入
Angela會幫您搜尋資料庫回答'''
        message = TextSendMessage(alt_text="其他功能說明",text = text1)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,\
                                   TextSendMessage(text='sendUse發生錯誤！'))

def sendLUIS(event, mtext, userid):  #LUIS
    try:
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/'+\
                         'apps/bb948c03-e76d-4568-b50b-3c6945e94ebb'+\
                         '?staging=true&verbose=true&timezoneOffset=-480&'+\
                         'subscription-key=a6961e76af7a4698bf84b79b0ce3c5f7&q='+\
                         mtext)  #終結點
        result = r.json()

        city = ''
        money = ''
        if result['topScoringIntent']['intent'] == '縣市天氣':
            for en in result['entities']:
                if en['type'] == '地點':  #由LUIS天氣類取得地點
                    city = en['entity']
                    break
        elif result['topScoringIntent']['intent'] == '匯率查詢':
            for en in result['entities']:
                if en['type'] == '幣別':  #由LUIS匯率類取得幣別
                    money = en['entity']
                    break
        if not city == '':  #天氣類地點存在
            flagcity = False  #檢查是否為縣市名稱
            city = city.replace('台', '臺')  #氣象局資料使用「臺」
            city = city.replace('中壢', '桃園')
            if city in cities:  #加上「市」
                city += '市'
                flagcity = True
            elif city in counties:  #加上「縣」
                city += '縣'
                flagcity = True
            if flagcity:  #是縣市名稱
                weather = city + '天氣資料：\n'
                #由氣象局API取得氣象資料
                api_link = "http://opendata.cwb.gov.tw/opendataapi?dataid"\
                           +"=%s&authorizationkey=%s" % (doc_name,user_key)
                report = requests.get(api_link).text
                xml_namespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
                root = et.fromstring(report)
                dataset = root.find(xml_namespace + 'dataset')
                locations_info = dataset.findall(xml_namespace + 'location')
                target_idx = -1
                # 取得 <location> Elements,每個 location 就表示一個縣市資料
                for idx,ele in enumerate(locations_info):
                    locationName = ele[0].text # 取得縣市名
                    if locationName == city:
                        target_idx = idx
                        break  
                # 挑選出目前想要 location 的氣象資料
                tlist = ['天氣狀況', '最高溫', '最低溫', '舒適度', '降雨機率']
                for i in range(5):
                    element = locations_info[target_idx][i+1] # 取出 Wx (氣象描述)
                    timeblock = element[1] # 取出目前時間點的資料
                    data = timeblock[2][0].text
                    weather = weather + tlist[i] + '：' + data + '\n'
                weather = weather[:-1]  #移除最後一個換行
                line_bot_api.reply_message(event.reply_token,\
                                           TextSendMessage(text=weather))
            else:
                line_bot_api.reply_message(event.reply_token,\
                                           TextSendMessage(text='無此地點天氣資料！'))
        elif not money == '':  #匯率類幣別存在
            tlist = ['現金買入', '現金賣出', '即期買入', '即期賣出']
            message = '台灣銀行' + currencies[money] +'='+ money + '的匯率：\n'
            if money in keys:
                for i in range(4):
                    exchange = twder.now(currencies[money])[i+1]
                    message = message + tlist[i] + '= ' + str(exchange)
                    if i != 3:
                        message = message + '\n'
                line_bot_api.reply_message(event.reply_token,\
                                           TextSendMessage(text=message))
            else:
                line_bot_api.reply_message(event.reply_token,\
                                           TextSendMessage(text='無此幣別匯率資料！'))
        else:  #其他未知輸入
            func8QnA.sendQnA(event, mtext, userid)
# =============================================================================
#             text = '無法了解你的意思，請重新輸入！'
#             line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
# =============================================================================
            
    except:
       line_bot_api.reply_message(event.reply_token,\
                                  TextSendMessage(text='sendLUIS執行時產生錯誤！'))

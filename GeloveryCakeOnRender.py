from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationSendMessage, VideoSendMessage, TemplateSendMessage, MessageTemplateAction, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageSendMessage, StickerSendMessage, PostbackEvent, MessageAction, QuickReply, QuickReplyButton

import os

line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
handler = WebhookHandler(os.environ.get('Channel_Secret'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

baseurl = 'https://8d18-119-77-180-85.ngrok-free.app/static/'  #靜態檔案網址

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@更多訊息':
        try:
            message = [   #串列
                StickerSendMessage(   #傳送貼圖
                    package_id='1',
                    sticker_id='2' 
                ),
                TextSendMessage(    #傳送文字
                    text = "歡迎加入Gelovery cake好友!\n✨ Gelovery Gift 新年特價 ✨\n法式提拉米蘇優惠價NT$888！\n限時特惠，經典甜點，迎接甜蜜新年。\n立即訂購，讓幸福從這一口開始！"
                ),
                ImageSendMessage(   #傳送圖片
                    original_content_url = "https://i.imgur.com/m1ze1FR.png",  #截圖提拉米蘇的圖片
                    preview_image_url = "https://i.imgur.com/m1ze1FR.png"
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
            
    elif mtext == '@相關影片':
        try:
            message = VideoSendMessage(
                original_content_url=baseurl + 'cake_video.mp4',  #影片檔置於static資料夾
                preview_image_url=baseurl + "cake_photo.png"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
            
    elif mtext == '@位置訊息':
        try:
            message = LocationSendMessage(
                title='Gelovery Cake',
                address='台北市大安區大安路一段51巷27號',
                latitude=25.043203, #緯度
                longitude=121.54743 #經度
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
            
    elif mtext == '@快速選單':
        try:
            # 第一層選單：選擇程式語言
            message = TextSendMessage(
                text="蛋糕宅配有一定風險，為了確保蛋糕的新鮮及配送安全，蛋糕全程皆使用「宅配低溫冷凍」配送，因保存期限及衛生考量。",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="關於鑑賞期", text="依據消保法規定為食用商品不適用於七天鑑賞期")),
                        QuickReplyButton(action=MessageAction(label="退換貨資訊", text="一經拆封或非運送過程失溫導致商品變質者，恕不退換貨，下單前請謹慎思考，敬請見諒！")),
                        QuickReplyButton(action=MessageAction(label="節日期間", text="重大節日或天災造成的不可抗因素,皆無法指定到貨日期以及到貨時段,建議指定提前一天到貨。")),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤'))
            
    elif mtext == '@推薦品項':
        sendCarousel(event)
        
@handler.add(PostbackEvent)
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))

    if backdata.get('action') == 'buy':
        sendBack_buy(event, backdata)
    elif backdata.get('action') == 'sell':
        sendBack_sell(event, backdata)
        
def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/RlEw56f.png',
                        title='小山園濃重抹茶生巧克力生乳捲',
                        text='NT$580',
                        actions=[
                            MessageTemplateAction(
                                label='產品介紹',
                                text='採用麵粉界的天花板「金寶笠麵粉」,入口一抿就化，吃在嘴裡蛋糕體與奶油分不出邊界融合在一起！'
                            ),
                            URITemplateAction(
                                label='購買連結',
                                uri='https://liff.line.me/2006620228-jKo5n6WP'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/cQztNxm.png',
                        title='艾美黛巧克力奶霜蛋糕六入組',
                        text='NT$2,499',
                        actions=[
                            MessageTemplateAction(
                                label='產品介紹',
                                text='搭配日本北海道中澤奶霜，清爽中帶點濃郁，巧克力與細緻奶油的完美結合，每吃一口都會忍不住捧著臉頰享受，再一口接一口！'
                            ),
                            URITemplateAction(
                                label='購買連結',
                                uri='https://liff.line.me/2006620228-A3R04q6y'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/XpSo6wD.png',
                        title='北海道草莓起司蛋糕',
                        text='NT$1,480',
                        actions=[
                            MessageTemplateAction(
                                label='產品介紹',
                                text='少女心噴發！濃郁起司加上草莓，香味Double！\n搭配特製法式餅乾底，口感綿密層次豐富，絕對是午茶時光必備甜點。'
                            ),
                            URITemplateAction(
                                label='購買連結',
                                uri='https://liff.line.me/2006620228-Jw9MXqon'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
        
if __name__ == '__main__':
    app.run()
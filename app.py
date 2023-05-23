#載入LineBot所需要的模組 
from flask import Flask, request, abort  
from linebot import (LineBotApi, WebhookHandler) 
from linebot.exceptions import (InvalidSignatureError) 
from linebot.models import *

app = Flask(__name__)  
# 必須放上自己的Channel Access Token 
line_bot_api = LineBotApi('Hhy9PWK0R49sz4HLsuG4NNcyQi5ZgvQf8KvfGdRBIGPKRHFPaj2ptFakk9naXJjr7eSMKh+n8YZ8QAY3pHOc1jhST8mN27Wy3wQ/8OECwdG39ekwVzEI/jZ/sxmuKWBRwibRO9OpReJ4BcCF1hIhPwdB04t89/1O/w1cDnyilFU=')  
# 必須放上自己的Channel Secret
handler = WebhookHandler('0de9cdba20c0b3dd52562dcfa8a88600')

line_bot_api.push_message('U98d45abf2b2460105e18bca31faf5084', TextSendMessage(text='你可以開始了'))

#訊息傳遞區塊 
##### 基本上程式編輯都在這個function ##### 
@handler.add(MessageEvent, message=TextMessage) 
def handle_message(event):
    message = event.message.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

# 監聽所有來自 /callback 的 Post Request 
@app.route("/callback", methods=['POST']) 
def callback():
    # get X-Line-Signature header value     
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)# get request body as text
    app.logger.info("Request body: " + body)      
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#主程式 
import os if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
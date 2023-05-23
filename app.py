
from __future__ import unicode_literals
from config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET

import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


line_bot_api.push_message('U98d45abf2b2460105e18bca31faf5084', TextSendMessage(text='你可以開始了COPY'))


@app.route("/", methods=['GET'])
def hello():
    return "Hello World! by LeoS"

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
       abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    msg = msg.encode('utf-8')
    # Echo the user's message back to the chat
    reply = 'You said: ' + msg

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    line_bot_api.push_message('U98d45abf2b2460105e18bca31faf5084', TextSendMessage(text='我結束了'))


if __name__ == "__main__":
    app.run(debug=True,port=80)
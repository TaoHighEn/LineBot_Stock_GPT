from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
import os
from src.logger import logger
from src.utils import get_role_and_content
from src.mongodb import mongodb
import src.stock_util as stock_util
from src.stock_util import get_stock_data, get_KD, calculate_indicators
from datetime import datetime, timedelta
import openai
import pandas as pd

load_dotenv('.env.example')

app = Flask(__name__)
print(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
model_management = {}

# 問GPT這樣會漲還是跌
def ask(ticker,df):
    # 從環境變量中讀取 API 密鑰
    openai.api_key = os.getenv('OPENAI_API')
    # openai.api_key = ''
    # 定義要發送給 ChatGPT 的消息
    # 調用 ChatGPT API
    print(map_msg(ticker,df))
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "你是個財經專家"
        }, {
            "role": "user",
            "content": map_msg(ticker,df)
        }])
    
    # 取得 ChatGPT 的回應
    reply = response.choices[0].message.content
    print(response.choices)
    print(reply)
    return reply

def map_msg(ticker,df):
    columns = list(df.columns)
    ticker_name = stock_util.get_stock_name(ticker)
    df0 = df.tail(1)
    index = df0.index
    msg='請問' + ticker + ' ' + ticker_name + '的股票各項指標如下：'
    for x in columns:
        result = df0.at[index[0],x]
        msg +=('\n' + x + ':' +str(result))
    
    msg += '\n請協助分析目前漲跌情況。'
    return msg

@app.route("/callback", methods=['POST'])
def callback():
    # LineBot必要資訊
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    logger.info(f'{user_id}: {text}')

    try:
        # end = datetime.today()
        # start = end - timedelta(days=30)  # 最近3個月
        # stock_info = get_stock_data('2330', start, end)
        # # df = stock_util.get_rsi_func(stock_info)
        # df = stock_util.get_rsi_func(stock_info)
        # # df = pd.concat([df,stock_util.get_macd_func(stock_info)])
        # df = pd.merge(left=df,right=stock_util.get_macd_func(stock_info),how='outer',on='Date')
        # df = pd.merge(left=df,right=stock_util.get_kd_func(stock_info),how='outer',on='Date')
        # stock = stock_util.get_stock_info('8039.TW',30)
        # msg = TextMessage(text=ask('8039.TW',stock))
        if text.startswith('/查詢'):
            ticker = text[3:].strip() + '.TW'
            stock = stock_util.get_stock_info(ticker,30)
            msg = TextMessage(text=ask(ticker,stock))
        elif text.startswith('/選股'):
            None

    except Exception as repli:
        print(repli.args)
        msg = TextSendMessage(text='發生錯誤，請稍後再試。')

    line_bot_api.reply_message(event.reply_token, msg)


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

import os
import json
import logging
import random
import cv2
from pathlib import Path
from flask import Flask, abort, request
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent,
                            TextMessage, TextSendMessage, FollowEvent, FlexSendMessage)
#hagih




app = Flask(__name__)


face_cascade_path = "haarcascade_frontalface_default.xml"
eye_cascade_path = "haarcascade_eye.xml"

YOUR_CHANNEL_ACCESS_TOKEN = "21MB2pzMrEs0JNqAdPTPyxFJmnaljipr9bLiUuMJrPWaLeCPHmK1tnqK23FoVL9kjqnpmyaJ0jFu3/KBCKl+O0WKIYzZ6lqfNEcAGaw3ag8aOwVlNzFsgmgVjiyewGsJOjnlogELVfGGTqz/PRJimwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "b392c7fd703eba783a31c2c6cb80a890"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]     #lineしか受け付けない

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(FollowEvent)
def handle_follow(event):
    with open('./saisyohaguu_message.json') as f:
        saisyohaguu_message = json.load(f)
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message)
    )
@handler.default()
def default(event):
    with open('./saisyohaguu_message.json') as f:
        saisyohaguu_message = json.load(f)
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message)
    )



   
    

def handle_textmessage(event):
    print("ログ成功！！！！！！！！！")
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text="目を検知できませんでした。"),
            TextSendMessage(text="他の画像を送信してください。"),
        ]
    )




@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id

    # 画像を保存

    message_content = line_bot_api.get_message_content(message_id)

    with open("static/"+ message_id + ".jpg", "wb") as f:
        f.write(message_content.content)

    result = change_image(event)
    if result:
        print("ログ成功！！！！！！！！！")
        line_bot_api.reply_message(
            event.reply_token, ImageSendMessage(
                original_content_url="https://team-hagi-project.herokuapp.com/static/mosaic.jpg",
                preview_image_url="https://team-hagi-project.herokuapp.com/static/mosaic.jpg",
            )
        )
    else:
        handle_textmessage(event)

def change_image(event):
    message_id = event.message.id
    fname = "static/" + message_id + ".jpg"  # 画像ファイル名



    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

    src = cv2.imread(fname)
    src_mosaic = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(src_mosaic)

    ratio = 0.05     #縮小処理時の縮小率(小さいほどモザイクが大きくなる)


# 検出した場合
    #if len(facerect) > 0:
#
    #    # 検出した顔を囲む矩形の作成
    #    for rect in facerect:
    #        cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=2)
    #else:
    #    return False
#
    #cv2.imwrite(output_path, image)
    ## 認識結果の保存

    if len(eyes) > 0:
        for x, y, w, h in eyes:  # 引数でeyesで取得した数分forループ
            # y:はHEIGHT、x:はWEIGHT  fxはxの縮小率、fyはyの縮小率
            small = cv2.resize(src[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
            src[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    else:
        return False

    cv2.imwrite("static/mosaic.jpg", src)

    return True
#def save_image(message_id: str, save_path: str) -> None:
    #"""保存"""
    #message_content = line_bot_api.get_message_content(message_id)
    #with open(save_path, "wb") as f:
       # for chunk in message_content.iter_content():
        #    f.write(chunk)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
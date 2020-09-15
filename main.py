from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import os
import cv2
import template.message_ymst as ymst
#hagih

app = Flask(__name__)

# face_cascade_path = "haarcascade_frontalface_default.xml"
# eye_cascade_path = "haarcascade_eye.xml"
YOUR_CHANNEL_ACCESS_TOKEN=os.environ["21MB2pzMrEs0JNqAdPTPyxFJmnaljipr9bLiUuMJrPWaLeCPHmK1tnqK23FoVL9kjqnpmyaJ0jFu3/KBCKl+O0WKIYzZ6lqfNEcAGaw3ag8aOwVlNzFsgmgVjiyewGsJOjnlogELVfGGTqz/PRJimwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET=os.environ["b392c7fd703eba783a31c2c6cb80a890"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    print("Request body: {}".format(body))

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    contents = []
    flex_ymst = FlexSendMessage.new_from_json_dict(ymst.get_ymst_message())
    contents.append(flex_ymst)
    line_bot_api.reply_message(event.reply_token, messages=contents)

if __name__=="__main__":
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)


# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image(event):
#     message_id = event.message.id

#     # 画像を保存

#     message_content = line_bot_api.get_message_content(message_id)

#     with open("static/"+ message_id + ".jpg", "wb") as f:
#         f.write(message_content.content)

#     result = change_image(event)
#     if result:
#         print("ログ成功！！！！！！！！！")
#         line_bot_api.reply_message(
#             event.reply_token, ImageSendMessage(
#                 original_content_url="https://team-hagi-project.herokuapp.com/static/mosaic.jpg",
#                 preview_image_url="https://team-hagi-project.herokuapp.com/static/mosaic.jpg",
#             )
#         )

# def change_image(event):
#     message_id = event.message.id
#     fname = "static/" + message_id + ".jpg"  # 画像ファイル名



#     eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

#     src = cv2.imread(fname)
#     src_mosaic = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

#     eyes = eye_cascade.detectMultiScale(src_mosaic)

#     ratio = 0.05     #縮小処理時の縮小率(小さいほどモザイクが大きくなる)

#     if len(eyes) > 0:
#         for x, y, w, h in eyes:  # 引数でeyesで取得した数分forループ
#             # y:はHEIGHT、x:はWEIGHT  fxはxの縮小率、fyはyの縮小率
#             small = cv2.resize(src[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
#             src[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
#     else:
#         return False

#     cv2.imwrite("static/mosaic.jpg", src)

#     return True

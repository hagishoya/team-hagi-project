from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
from image_change import mosic_change, art_change, dot_change, illust_change, hair_change
import main
import shutil
import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

################################################################
###------------------//画像送信処理//------------------------###

def handle_textmessage(event):
    main.line_bot_api.reply_message(event.reply_token,
    [
        #TextSendMessage(text=event.message.text),
        TextSendMessage(text="目を検知できませんでした。"),
        #TextSendMessage(text=event.message.id),
    ]
    )

#モザイク送信
def handle_send_message(event,reply,userid):
    result = mosic_change.mosic_image(event,userid)
    reply = str(reply)
    print("通過チェック画像：{}".format(main.FQDN + "/static/" + userid + "/" + event + "_face.jpg"))
    
    if result:
        message = []
        message.append(TextSendMessage(text = "画像を加工中です..."))
        message.append(ImageSendMessage(
            original_content_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",
            preview_image_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",))
        message.append(TextSendMessage(text = "加工が終了しました。"))
        main.line_bot_api.reply_message(reply,message)
        #shutil.rmtree("static/" + userid)
    else:
        handle_textmessage(event)



# 線画送信
def handle_send_message2(event,reply,userid):
    plt.set_cmap("gray")
    result = art_change.art_image(event,userid)
    reply = str(reply)
    print("通過チェック画像：{}".format(main.FQDN + "/static/" + userid + "/" + event + "_face.jpg"))
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
    #shutil.rmtree("static/" + userid)
    
# イラスト送信
def handle_send_message3(event,reply,userid):
    result = illust_change.illust_image(event,userid)
    reply = str(reply)
    print("通過チェック画像：{}".format(main.FQDN + "/static/" + userid + "/" + event + "_face.jpg"))
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
    #shutil.rmtree("static/" + userid)

# ドット絵送信
def handle_send_message4(event,reply,userid):
    result = dot_change.dot_image(event,userid)
    reply = str(reply)
    print("通過チェック画像：{}".format(main.FQDN + "/static/" + userid + "/" + event + "_face.jpg"))
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
    #shutil.rmtree("static/" + userid)

# # 髪の毛変更test
def handle_send_message5(event,reply,userid):
    result = hair_change.hair_image(event,userid)
    reply = str(reply)
    print("通過チェック画像：{}".format(main.FQDN + "/static/" + userid + "/" + event + "_face.jpg"))
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + userid + "/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
    #shutil.rmtree("static/" + userid)
################################################################
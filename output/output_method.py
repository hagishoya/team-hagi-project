from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
from image_change import mosic_change, art_change, dot_change, illust_change, hair_change
import main
import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

################################################################
###------------------//画像送信処理//------------------------###

#モザイク送信
def handle_send_message(event,relpy):
    #mozaiku(event)
    result = mosic_change.mosic_image(event)
    reply = str(relpy)
    print("ここも通過したじょ")
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
    # else:
    #     handle_textmessage(event)

# 線画送信
def handle_send_message2(event,reply):
    plt.set_cmap("gray")
    result = art_change.art_image(event)
    reply = str(reply)
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
    
# イラスト送信
def handle_send_message3(event,relpy):
    result = illust_change.illust_image(event)
    reply = str(relpy)
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)

# ドット絵送信
def handle_send_message4(event,relpy):
    result = dot_change.dot_image(event)
    reply = str(relpy)
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)

# 髪の毛変更test
def handle_send_message(event,relpy):
    result = hair_change.hair_image(event)
    reply = str(relpy)
    message = []
    message.append(TextSendMessage(text = "画像を加工中です..."))
    message.append(ImageSendMessage(
        original_content_url=main.FQDN + "/static/" + event + "_face.jpg",
        preview_image_url=main.FQDN + "/static/" + event + "_face.jpg",))
    message.append(TextSendMessage(text = "加工が終了しました。"))
    main.line_bot_api.reply_message(reply,message)
################################################################
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import main
import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import path_data
import random


def skin_image(event,userid,color):
    image_path, output_path = path_data.get_image_path(event,userid)


    img = cv2.imread(image_path)     # Load image
 

 
    #height = img.shape[0]
    #width = img.shape[1]
    #img2 = cv2.resize(img , (int(width*0.5), int(height*0.5)))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # BGR->HSV変換
    hsv_2 = np.copy(hsv)
    hsv_3 = np.copy(hsv_2)
    hsv_4 = np.copy(hsv_3)

    #hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>5) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 150,hsv[:, :, 0])
    #hsv_2[:, :, 2] = np.where((hsv[:, :, 2]>5) )
    #hsv_2[:, :, 2] = np.where((hsv[:, :, 0]>5) & (hsv[:, :, 0]<30) ,hsv[:, :, 2] *0.5,hsv[:, :, 2])#金髪から黒髪
    #hsv_2[:, :, 2] = np.where((hsv[:, :, 0]>5) & (hsv[:, :, 0]<30) ,hsv[:, :, 2] *0.5,hsv[:, :, 2])
    #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] +110 ,hsv[:, :, 0])#黒(茶色)から青
    #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] +50 ,hsv[:, :, 0])#黒(茶色)から緑
    #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] +160 ,hsv[:, :, 0])#黒(茶色)から赤
    #bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    #cv2.imwrite(output_path,bgr)
    #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] +50 ,hsv[:, :, 0])
    if color == 1:
        hsv_2[:, :, 1] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<100) ,hsv[:, :, 1] + 255 ,hsv[:, :, 1])
        #hsv_3[:, :, 2] = np.where((hsv_2[:, :, 2]>0) & (hsv_2[:, :, 2]<128) ,hsv_2[:, :, 2] + 120 ,hsv_2[:, :, 2])#白
        #hsv_4[:, :, 0] = np.where((hsv_3[:, :, 2]>120) & (hsv_3[:, :, 2]<248) ,hsv_3[:, :, 0] + 60 ,hsv_3[:, :, 0])
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 50,hsv[:, :, 0]) #緑
    elif color == 2:
        hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>6) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 110,hsv[:, :, 0]) #青
    elif color == 3:
        hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>6) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 20,hsv[:, :, 0]) #黄色
    elif color == 4:
        hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 176,hsv[:, :, 0]) #ピンク
        hsv_2[:, :, 1] = np.where((hsv[:, :, 0]>=176) ,hsv[:, :, 1] + 96 ,hsv[:, :, 1])
    elif color == 5:
        hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>6) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] *0.001,hsv[:, :, 0]) #赤色
    elif color == 6:
        hsv_2[:, :, 2] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 2] *0.4,hsv[:, :, 2]) #黒色




    #茶色から指定色-----------------------------------------------------------------------------------------------------------
    #if color == 1:
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<255) ,hsv[:, :, 0] +50 ,hsv[:, :, 0])#黒(茶色)から緑
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 50,hsv[:, :, 0]) #緑
    #elif color == 2:
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>6) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 110,hsv[:, :, 0]) #青
    #elif color == 3:
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>6) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 20,hsv[:, :, 0]) #黄色
    #elif color == 4:
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 176,hsv[:, :, 0]) #ピンク
        #hsv_2[:, :, 1] = np.where((hsv[:, :, 0]>=176) ,hsv[:, :, 1] + 96 ,hsv[:, :, 1])
    #elif color == 5:
        #hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>6) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] *0.001,hsv[:, :, 0]) #赤色
    #elif color == 6:
        #hsv_2[:, :, 2] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 2] *0.4,hsv[:, :, 2]) #黒色
    #hsv_2[:, :, 2] = np.where((hsv_2[:, :, 0]>6) & (hsv_2[:, :, 0]<30) ,hsv_2[:, :, 1] *0.7,hsv_2[:, :, 2]) #黒色
    #0.001 赤
    #0.3 緑
    #bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    #----------------------------------------------------------------------------------------------------------------------

    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path, bgr)

#hsv_2[:, :, 0] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 0] + 176,hsv[:, :, 0]) #濃い茶色
#hsv_2[:, :, 1] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 1] + 96 ,hsv[:, :, 1])


#白
#hsv_2[:, :, 1] = np.where((hsv[:, :, 2]>0) & (hsv[:, :, 2]<128) ,hsv[:, :, 1] + 180 ,hsv[:, :, 1])
#hsv_3[:, :, 2] = np.where((hsv_2[:, :, 2]>0) & (hsv_2[:, :, 2]<128) ,hsv_2[:, :, 2] + 180 ,hsv_2[:, :, 2])
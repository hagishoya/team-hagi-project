from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import main
import json
import os
import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np
import path_data


def get_head_mask(img):
 

    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    """
    The algorithm works best when a person is on a background that does not merge with his hair. Also, the hair should not merge with the complexion.
    """
    """
    Get the mask of the head
    Cuting  BG
    :param img: source image
    :return:   Returns the mask with the cut out BG
    """
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))    # Find faces
    if len(faces) != 0:
        x, y, w, h = faces[0]
        (x, y, w, h) = (x - 40, y - 100, w + 80, h + 200)
        rect1 = (x, y, w, h)
        cv2.grabCut(img, mask, rect1, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)     #Crop BG around the head
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # Take the mask from BG

    return mask2

def is_bold(pnt, hair_mask):
    """
    Check band or not
    :param pnt: The upper point of the head
    :param hair_mask: Mask with hair
    :return: True if Bald, else False
    """
    roi = hair_mask[pnt[1]:pnt[1] + 40, pnt[0] - 40:pnt[0] + 40]    # Select the rectangle under the top dot
    cnt = cv2.countNonZero(roi) # Count the number of non-zero points in this rectangle
    # If the number of points is less than 25%, then we think that the head is bald
    if cnt < 800:
        print("Bald human on phoro")
        return True
    else:
        print("Not Bold")
        return False

#def hsv_to_rgb(h,s,v):
##    h = 0 ~ 360
##    s = 0 ~ 255
##    v = 0 ~ 255
#    i = int(h / 60.0)
#    mx = v
#    mn = v - ((s / 255.0) * v)
#    if h is None:
#        return(0,0,0)
#    if i == 0:
#        (r1,g1,b1) = (mx,(h/60.0)*(mx-mn)+mn,mn)
#    elif i == 1:
#        (r1,g1,b1) = (((120.0-h)/60.0)*(mx-mn)+mn,mx,mn)
#    elif i == 2:
#        (r1,g1,b1) = (mn,mx,((h-120.0)/60.0)*(mx-mn)+mn)
#    elif i == 3:
#        (r1,g1,b1) = (mn,((240.0-h)/60.0)*(mx-mn)+mn,mx)
#    elif i == 4:
#        (r1,g1,b1) = (((h-240.0)/60.0)*(mx-mn)+mn,mn,mx)
#    elif 5 <= i:
#        (r1,g1,b1) = (mx,mn,((360.0-h)/60.0)*(mx-mn)+mn)
#    return (int(r1), int(g1), int(b1))

def hair_image(event,userid):
    image_path, output_path = path_data.get_image_path(event,userid)

    image = cv2.imread(image_path)     # Load image
    image = imutils.resize(image, height=500)     # We result in 500px in height
    mask = get_head_mask(image)      # We get the mask of the head (without BG))

    # Find the contours, take the largest one and memorize its upper point as the top of the head
    cnts = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnt=cnts[0]
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])


    # We remove the face by the color of the skin
    lower = np.array([0, 0, 100], dtype="uint8")  # Lower limit of skin color
    upper = np.array([255, 255, 255], dtype="uint8")  # Upper skin color limit
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   # We translate into HSV color format
    skinMask = cv2.inRange(converted, lower, upper)     # Write a mask from places where the color is between the outside
    mask[skinMask == 255] = 0   # We remove the face mask from the mask of the head

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mask, kernel1, iterations=1)
    i1 = cv2.bitwise_and(image, image, mask=mask)


    # 髪の毛なし
    if is_bold(topmost,mask):
        cv2.rectangle(image,topmost,topmost,(0,0,255),5)
        print(topmost)



    # 髪の毛あり
    else:
        #輪郭取得
        cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        cv2.drawContours(image,[cnts[0]],-1,(0,0,255),2)
       # green = np.uint8([[[0,255,0 ]]])
        #bgr = cv2.cvtColor(np.array([[[0,255,0]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
        #ポリゴンの領域を塗りつぶす
        
        #test_color = hsv_to_rgb(300, 200 , 200)
        # 色基準で2値化する。
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 色の範囲を指定する
        lower_color = np.array([0, 0, 0])
        upper_color = np.array([255, 255, 255])

        # 指定した色に基づいたマスク画像の生成
        mask = cv2.inRange(hsv, lower_color, upper_color)
        output = cv2.bitwise_and(hsv, hsv, mask = mask)
        print(output)
        print("\n\n\n\n\n\n\n\n\n")
        bgr_output = colorsys.hsv_to_rgb(output)
        bgr_color = bgr_output + (0,0,80)
        cv2.fillPoly(image, pts =[cnts[0]], color= bgr_color)
        #cv2.fillPoly(image, pts =[cnts[0]], color= (255,0,0))
        #green = np.uint8([[[0,255,0 ]]])
        #hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
        #image[:] = hsv_green
        for c in cnts[0]:
            print(c)


    if bool:
        # 認識結果の保存
        cv2.imwrite(output_path, image)
        #cv2.imwrite(output_path2, image)
        return True
    else:
        return False
    # # Display the image in a loop
    # while True:
    #     cv2.imwrite(output_path, image)
    #     #cv2.imshow("image1", image)
    #     # Exit to Esc
    #     if cv2.waitKey(5) == 27:
    #         break
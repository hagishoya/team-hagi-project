from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import json
import os
import cv2
import imutils
import numpy as np
import colorsys
import scipy.ndimage as snd
from PIL import Image, ImageDraw

work = {}
path_w1 = 'saveid.txt'
path_w2 = 'savereply.txt'
app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
FQDN = os.environ["FQDN"]


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    print("Request body" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
       [
           TextSendMessage(text=event.message.text),
           #TextSendMessage(text="おはよ------"),
           #TextSendMessage(text="顔、目を検知できませんでした。"),
           #TextSendMessage(text=event.message.id),
       ]
       )
    print("取得イヴェント:{}".format(event))
    print("取得イヴェントメッセージID:{}".format(event.message.id))
    print("リプライトークン：{}".format(event.reply_token))
    print("------リプライ型------")
    print(type(event.reply_token))
    if event.message.text == "1":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        handle_send_message2(work,work1)
    if event.message.text == "2":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        handle_send_message3(work,work1)



def text_save_id(work):
    s = work
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD_text_saveID:{}".format(work))
    with open(path_w1, mode='w') as f:
        f.write(s)

def text_save_reply(work):
    s = work
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD_text_saveReply:{}".format(work))
    with open(path_w2, mode='w') as f:
        f.write(s)


def flex(event):
    work = event.message.id
    reply_work = event.reply_token
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD:{}".format(work))
    text_save_id(work)
    text_save_reply(reply_work)
    json_open = open('test.json', 'r')
    json_data = json.load(json_open)
    user_id = os.environ["USER_ID"]
    #print("json_data: {}".format(json_data.get("hero").get("url")))
    #print(json_data.get("hero").get("url"))
    #json_data["hero"]
    #message = line_bot_api.reply_message(
    #    event.reply_token,
    #    [
    #        FlexSendMessage(
    #        alt_text="flex",
    #        contents=BubbleContainer.new_from_json_dict(json_data)
    #        )
    #    ]
    #)

    messages = FlexSendMessage(alt_text="test", contents=json_data)
    print("フレックスメッセージ中身: {}".format(messages))
    if event.reply_token == "00000000000000000000000000000000":
        return
    if event.reply_token == "ffffffffffffffffffffffffffffffff":
        return
        
    line_bot_api.push_message(user_id, messages=messages)


def handle_textmessage(event):
    line_bot_api.reply_message(event.reply_token,
        [
            #TextSendMessage(text=event.message.text),
            TextSendMessage(text="顔、目を検知できませんでした。"),
            #TextSendMessage(text=event.message.id),
        ]
        )

#画像受信後処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print("メッセージID")
    print(event.message.id)
    message_content = line_bot_api.get_message_content(event.message.id)
    if not os.path.exists('static'):
        os.mkdir('static/')
    with open("static/" + event.message.id + ".jpg", "wb") as f:
        f.write(message_content.content)
    
    
    flex(event)

    

    
# #画像送信処理
# def handle_send_message(event):
#     #mozaiku(event)
#     result = change_image(event)

#     if result:
#         line_bot_api.reply_message(
#             event.reply_token, ImageSendMessage(
#                 original_content_url=FQDN + "/static/" + event.message.id + "_face.jpg",
#                 preview_image_url=FQDN + "/static/" + event.message.id + "_face.jpg",
#             )
#             )

#     else:
#         handle_textmessage(event)


#画像送信処理
def handle_send_message2(event,relpy):
    #mozaiku(event)
    result = change_image(event)
    reply = str(relpy)
    if result:
        line_bot_api.reply_message(
            reply, ImageSendMessage(
                original_content_url=FQDN + "/static/" + event + "_face.jpg",
                preview_image_url=FQDN + "/static/" + event + "_face.jpg",
            )
        )

    else:
        handle_textmessage(event)

#画像送信処理
def handle_send_message3(event,relpy):
    #mozaiku(event)
    result = change_image2(event)
    reply = str(relpy)

    if result:
        line_bot_api.reply_message(
            reply, ImageSendMessage(
                original_content_url=FQDN + "/static/" + event + "_face.jpg",
                preview_image_url=FQDN + "/static/" + event + "_face.jpg",
            )
        )

    else:
        handle_textmessage(event)

#囲う処理
def change_image(event):
    bool = True
    cascade_path = "haarcascade_frontalface_default.xml"
    cascade_eye_path = "haarcascade_eye.xml"

    image_file = event + ".jpg"
    save_file = event + "_face.jpg"
    #save_file2 = event.message.id + "_face2.jpg"
    print("イメージファイル: {} // {}".format(image_file, save_file))
    image_path = "static/" + image_file
    print("イメージパス: {}".format(image_path))
    output_path = "static/" + save_file
    #output_path2 = "static/" + save_file2
    print("アウトプットパス: {}".format(output_path))
    # ファイル読み込みo
    image = cv2.imread(image_path)

    # グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    cascade_eye = cv2.CascadeClassifier(cascade_eye_path)
    # 物体認識（顔認識）の実行
    # image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    # objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    # scaleFactor – 各画像スケールにおける縮小量を表します
    # minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    # flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    # minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    eyerect = cascade_eye.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(20, 20))
    print("レクト:{} // {}".format(facerect, eyerect))
    print("ぎっとぽっど")

    color = (255, 0, 0)  # 青

    ## 検出した場合
    #if len(facerect) > 0:
    #    # 検出した顔を囲む矩形の作成
    #    for rect in facerect:
    #        cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=1)
    #        print(facerect)
    #        print(rect)
    #else:
    #    bool = False

    ratio = 0.05  # 縮小処理時の縮小率(小さいほどモザイクが大きくなる)
    if len(eyerect) > 0:
        # for rect in eyerect:
        #     cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=1)
        #     print(eyerect)
        #     print(rect)
           

        for x, y, w, h in eyerect:  # 引数でeyesで取得した数分forループ
           # y:はHEIGHT、x:はWEIGHT  fxはxの縮小率、fyはyの縮小率
           small = cv2.resize(image[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
           image[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
           
    else:
        bool = False

    if bool:
        # 認識結果の保存
        cv2.imwrite(output_path, image)
        #cv2.imwrite(output_path2, image)
        return True
    else:
        return False




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
    print("mask{}".format(mask))
    bgdModel = np.zeros((1, 65), np.float64)
    print("bgdModel{}".format(bgdModel))
    fgdModel = np.zeros((1, 65), np.float64)
    print("fgdModel{}".format(fgdModel))
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))    # Find faces
    print(faces)
    if len(faces) != 0:
        x, y, w, h = faces[0]
        (x, y, w, h) = (x - 40, y - 100, w + 80, h + 200)
        rect1 = (x, y, w, h)
        print("rect1{}".format(rect1))
        cv2.grabCut(img, mask, rect1, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)     #Crop BG around the head
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # Take the mask from BG
    print("mask2{}".format(mask2))
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

def hsv2rgb(h,s,v):
    return (round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


#def draw_contours_B(output_path, img):
    # 2値化
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite(now + '_1_' + file_name + '_gray_B.jpg', gray)
    
#    ret,th1 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    #cv2.imwrite(now + '_2_' + file_name + '_th1_B.jpg', gray)
    # 輪郭抽出
#    contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#    areas = []
#    for cnt in contours:
#        area = cv2.contourArea(cnt)
#        if area > 10000:
#            epsilon = 0.1*cv2.arcLength(cnt,True)
#            approx = cv2.approxPolyDP(cnt,epsilon,True)
#            areas.append(approx)
    #cv2.drawContours(img, areas, -1, (0,255,0), 3)
#    cv2.imwrite(output_path, img)


def change_image2(event):
    image_file = event + ".jpg"
    save_file = event + "_face.jpg"
    #save_file2 = event.message.id + "_face2.jpg"
    print("イメージファイル: {} // {}".format(image_file, save_file))
    image_path = "static/" + image_file
    print("イメージパス: {}".format(image_path))
    output_path = "static/" + save_file
    #output_path2 = "static/" + save_file2
    print("アウトプットパス: {}".format(output_path))
    img = cv2.imread(image_path)
    #draw_contours_B(output_path, img)

    # load image, change color spaces, and smoothing
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_HSV = cv2.GaussianBlur(img_HSV, (9, 9), 3)

    # detect tulips
    img_H, img_S, img_V = cv2.split(img_HSV)
    thre, img_flowers = cv2.threshold(img_H, 140, 255, cv2.THRESH_BINARY)
    # find tulips
    contours, hierarchy = cv2.findContours(img_flowers, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for i in range(0, len(contours)):
        if len(contours[i]) > 0:

            # remove small objects
            if cv2.contourArea(contours[i]) < 500:
                continue

            cv2.polylines(img, contours[i], True, (255, 255, 255), 5)

    # save
    cv2.imwrite(output_path, img)
    return True


    img = cv2.imread(output_path)     # Load image
    height = img.shape[0]
    width = img.shape[1]
    img2 = cv2.resize(img , (int(width*0.5), int(height*0.5)))
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV) # BGR->HSV変換
    hsv_2 = np.copy(hsv)
    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>16) & (hsv[:, :, 0]<25) ,hsv[:, :,(2)]*0.2,hsv[:, :, 0])
    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path,bgr)
    return True

    #if bool:
    #    # 認識結果の保存
    #    cv2.imwrite(output_path, image)
    #    #cv2.imwrite(output_path2, image)
    #    return True
    #else:
    #    return False
    #



def image_resize(image1, width = None, height = None, inter = 
cv2.INTER_AREA):

    #サイズ変更する画像のサイズを初期化し、
    #画像サイズを取得します
    dim = None
    (h, w) = image1.shape[:2]

    # 幅と高さの両方がNoneの場合、
    #元の画像
    if width is None and height is None:
        return image1

    # 幅がなしかどうかを確認します
    if width is None:
        # 高さの比率を計算し、
        # 寸法
        r = height / float(h)
        dim = (int(w * r), height)

    # それ以外の場合、高さはなし
    else:
        # 幅の比率を計算し、
        # 寸法
        r = width / float(w)
        dim = (width, int(h * r))

    # 画像のサイズを変更する
    resized = cv2.resize(image1, dim, interpolation = inter)

    # サイズ変更された画像を返す
    return resized


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    #12/31
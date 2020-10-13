def get_image_path(event):

    image_file = event + ".jpg"
    save_file = event + "_face.jpg"
    print("イメージファイル: {} // {}".format(image_file, save_file))

    # 元画像の保存場所をパスとして保管
    image_path = "static/" + image_file
    print("イメージパス: {}".format(image_path))

    # 加工済みの画像の保存場所をパスとして保管
    output_path = "static/" + save_file
    print("アウトプットパス: {}".format(output_path))

    return image_path, output_path
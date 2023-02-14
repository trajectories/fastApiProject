import os, io
import requests
# import pandas as pd
import time, json, cv2, base64
img_list = []
for x in range(3, 4):
    folder_number = str(x)
    # path = "C:/Users/Administrator/Desktop/Real Photo/Vertical/"
    path = "C:/Users/admin/Desktop/Real Photo/Vertical/"
    path += folder_number
    dir_list = os.listdir(path)
    all_item = len(dir_list)

    for i in range(all_item):
        img_file = dir_list[i]
        image = open(path + '/' + img_file, 'rb')  # open binary file in read mode
        image_read = image.read()
        imagebase64 = base64.b64encode(image_read).decode('ascii')
        img_list.append(imagebase64)

print(img_list[0])
import threading, queue
import os, io
import requests
# import pandas as pd
import time, json, base64
# import pytest
# from pandas.core.frame import DataFrame
# import numpy as np

from PIL import Image

headers = {
    'apikey': 'YXBpc2VjcmV0a2V5',
    'Content-Type': 'application/json'
}
base_url = 'http://115.31.144.250:5001/v2/detect_atk/capture'

results_negative = []
results_positive = []
failed_requests = []
not_detects = []
results_invalid = []
start_time = time.time()
img_list = []
results_cant_read = []

for x in range(1, 6):
    folder_number = str(x)
    # path = "C:/Users/Administrator/Desktop/Real Photo/Vertical/"
    path = "C:/Users/admin/Desktop/Real Photo/Positive/positive"
    path += folder_number
    dir_list = os.listdir(path)
    all_item = len(dir_list)

    for i in range(all_item):
        img_file = dir_list[i]
        image = open(path + '/' + img_file, 'rb')  # open binary file in read mode
        image_read = image.read()
        imagebase64 = base64.b64encode(image_read).decode('ascii')
        img_list.append(imagebase64)


def worker():
    with requests.Session() as session:
        # a = 0
        # b = 10
        # while b <= 100:
        for j in range(len(img_list)):
        # j = 2
        #     print(img_list[j])

            payload = json.dumps({
                "imageBase64": img_list[j]
            })
            response = session.post(url=base_url, headers=headers, data=payload)
            if response.ok:
                data = response.json()
                print(f'round{j}')
                print(data)

                if data["msg"] == 'ATK not detected!':
                    not_detects.append(j)
                elif data["msg"] == 'Cannot read image file':
                    results_cant_read.append(j)
                elif data["result"] == "Positive":
                    results_positive.append((data['result']))
                elif data["result"] == "Negative":
                    results_negative.append((data['result']))
                elif data["result"] == "Invalid":
                    results_invalid.append((data['result']))
            else:
                failed_requests.append(j)
            time.sleep(0.00001)
                # a += 10
                # b += 10
                # print(a)
                # print(b)


    print(f'Image have {len(img_list)}.')
    print(f'ATK Negative have {len(results_negative)}.')
    print(f'ATK Positive have {len(results_positive)}.')
    print(f'ATK Invalid have {len(results_invalid)}.')
    print(f'ATK Can not read image file have {len(results_cant_read)}.')
    print(f'ATK cant detect have {len(not_detects)}.')
    print(f'Status 422 have {len(failed_requests)}.')

    print("\n--- %s seconds ---" % (time.time() - start_time))


worker()




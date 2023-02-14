import threading, queue
import os, io
import requests
# import pandas as pd
import time, json, cv2, base64
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
start_time = time.time()
img_list = []
for x in range(1, 3):
    folder_number = str(x)
    # path = "C:/Users/Administrator/Desktop/Real Photo/Vertical/"
    path = "C:/Users/admin/Desktop/Real Photo/Invalid/invalid"
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
        for j in range(len(img_list)):
            imagebase64str = img_list[j]
            payload = json.dumps({
                "imageBase64": imagebase64str
            })
            response = session.post(url=base_url, headers=headers, data=payload)
            if response.ok:
                data = response.json()
                if data['msg'] == 'ATK not detected!':
                    not_detects.append(j)
                elif data['result'] == ['Positive']:
                    results_positive.append(data['result'])
                else:
                    results_negative.append(data['result'])
            else:
                failed_requests.append(j)
    print(f'Image have {len(img_list)}.')
    print(f'ATK Negative have {len(results_negative)}.')
    print(f'ATK Positive have {len(results_positive)}.')
    print(f'ATK cant detect have {len(not_detects)}.')
    print(f'Status 422 have {len(failed_requests)}.')

    print("\n--- %s seconds ---" % (time.time() - start_time))


worker()




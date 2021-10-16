# -*- coding: utf-8 -*-
"""extract_frame.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IAhLwKVOEY2Js9M0pRQyVuDlCVcKaJQl
"""

import io
import os
import numpy as np
import base64
from IPython.display import HTML
import cv2
#from google.colab.patches import cv2_imshow
from tensorflow.keras.models import model_from_json
from PIL import Image
#import glob
#import shutil

from google.colab import drive
drive.mount('/content/gdrive')

#!cp -r "/content/gdrive/MyDrive/antispoofing.zip" "/content"

import zipfile
archive = zipfile.ZipFile('/content/gdrive/MyDrive/antispoofing.zip')
archive.extractall('/content')

root_dir =  '/content/antispoofing'

#!ls antispoofing

face_cascade = cv2.CascadeClassifier("/content/antispoofing/model/haarcascade_frontalface_default.xml")

json_file = open("/content/antispoofing/model/finalyearproject_antispoofing_model_mobilenet.json",'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('/content/antispoofing/model/┘Çantispoofing_model.h5')

def playvideo(filename):
    video = io.open(filename, 'r+b').read()
    encoded = base64.b64encode(video)
    return HTML(data='''<video alt="test" controls>
                    <source src="data:video/mp4;base64,{0}" type="video/mp4"/>
                 </video>'''.format(encoded.decode('ascii')))

video = 'WhatsApp Video 2021-10-13 at 9.36.54 PM.mp4'
playvideo(video)

cap = cv2.VideoCapture(video)

save_path = os.mkdir('/content/save')

i=0 
gap =10

while True:
    try:
      ret,frame = cap.read()
      if i==0:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
      if i%gap==0:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)

      print(" Found {0} Faces.".format(len(faces)))

      for (x,y,w,h) in faces:
        face = frame[y-5:y+h+5,x-5:x+w+5] 
        resized_face = cv2.resize(face,(160,160))
        resized_face = resized_face.astype("float") / 255.0
        resized_face = np.expand_dims(resized_face, axis=0)


        preds = model.predict(resized_face)[0]
        print(preds)
        if preds> 0.5:
          label = 'spoof'
          cv2.putText(frame, label, (x,y - 10),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)   
          cv2.rectangle(frame, (x, y), (x+w,y+h),(0, 0, 255), 2)
        else:
          label = 'real'
          cv2.putText(frame, label, (x,y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
          cv2.rectangle(frame, (x, y), (x+w,y+h),(0, 255, 0), 2)
        
        print("[INFO] Object found. Saving locally.")
        print(label)
        cv2.imwrite(str(w) + str(h) +label+ '_faces.jpg', frame)
        cv2.imwrite(f"{save_path}/{i}.png", frame)
        
        status = cv2.imwrite(str(predect)+'faces_detected.jpg', frame)
        print("[INFO] Image faces_detected.jpg written to filesystem: ", status) 

        key = cv2.waitKey(1)
        if key == ord('q'):
          break
    except Exception as e:
        pass
video.release()        
cv2.destroyAllWindows()
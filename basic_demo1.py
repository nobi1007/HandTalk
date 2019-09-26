import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
import time

mappings = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"G",8:"H",9:"I",10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",}
cap = cv2.VideoCapture(0)
myModel = keras.models.load_model("first_handTalk.h5")
# print(myModel.summary())

while(True):
    ret, frame = cap.read()
    image = cv2.flip(frame,1)
    start_point = (250,150)
    end_point = (500,400)
    color = (0,255,0)
    thickness = 2    
    image = cv2.rectangle(image, start_point, end_point, color, thickness)
    y2 = image[150:401,250:501]
    y = cv2.resize(y2,(28,28))
    y2 = cv2.resize(y,(250,250))
    y2 = cv2.cvtColor(y2,cv2.COLOR_BGR2GRAY)
    y = cv2.cvtColor(y,cv2.COLOR_BGR2GRAY)

    img1 = "Original"
    cv2.namedWindow(img1)        
    cv2.moveWindow(img1, 140,130) 
    
    img2 = "Cropped and Sized"
    cv2.namedWindow(img2)        
    cv2.moveWindow(img2, 1040,130)  
    
    
    newImg = np.reshape(y,[1,28,28,1])
    prediction = myModel.predict(newImg)
    index = 0
    prediction
    for i in range(len(prediction[0])):
        if prediction[0][i]==1:
            index = i
            break

    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (50, 50) 
    fontScale = 2
    color = (255, 0, 0) 
    thickness = 2
    image = cv2.putText(image, mappings[index], org, font,  
                    fontScale, color, thickness, cv2.LINE_AA) 
    cv2.imshow(img1, image)
    cv2.imshow(img2, y2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()

import tensorflow as tf
import numpy as np
import cv2
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
import time
import math
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

myModel = keras.models.load_model("handTalk_ver2.h5")
mappings = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:'J',10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",25:'Z',26:' DEL ',27:'',28:'  '}

app = Flask(__name__)
app.config['SECRET_KEY'] = "vnkdjnfjknfl1232#"
socketio = SocketIO(app)

@app.route("/")
def sessions():
    return render_template("landing.html")

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

# @app.route("/camera")
# def camera_access():
#     return render_template("camera_acc.html")

@app.route("/main")
def main_page():
    return render_template("main_app.html")

@app.route("/main/aim")
def aim_section():
    return render_template("aim.html")

@app.route("/main/abouts")
def abouts_section():
    return render_template("abouts.html")

@app.route("/main/help")
def help_section():
    return render_template("help.html")

@socketio.on("my event")
def handle_my_custom_event(json,methods=["GET","POST"]):

    global myModel

    print("Received my image : ")
    if len(json) == 1:
        print(json)
    else:
        height = 64
        width = 64
        arr=[[[0 for k in range(3)] for j in range(width)] for i in range(height)]
        bw_data = []
        dic = json["image_data"]
        print(len(dic))
        for i in range(0,len(dic),4):
            temp = []
            temp.append(dic[str(i)])
            temp.append(dic[str(i+1)])
            temp.append(dic[str(i+2)])
            bw_data.append(temp)
            # +dic[str(i+1)]+dic[str(i+2)])/3))
        # print(np.shape(bw_data))
        bw_data = np.array(bw_data)

        for i in range(height):
            for j in range(width):
                arr[i][j][0] = bw_data[i*height + j][0]
                arr[i][j][1] = bw_data[i*height + j][1]
                arr[i][j][2] = bw_data[i*height + j][2]
        
        arr = np.array(arr)
        print(np.shape(arr),arr)
        new_arr = np.reshape(arr,[1,height,width,3])

        # prediction = myModel.predict(new_arr)
        # val = max(prediction[0])
        # pos = np.where(prediction[0]==val)
        
        print(np.shape(new_arr))
        json["response"] = mappings[0]

        # new_image_array = np.reshape(bw_data,[1,height,width,1])
        # print(bw_data)
        # print(len(bw_data),len(new_image_array))
    # print(json["image_data"])

    socketio.emit("my response",json,callback = messageReceived)

if __name__ == "__main__":
    socketio.run(app,port=2000,debug=True)
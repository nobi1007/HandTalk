from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import math
import numpy as np
 
app = Flask(__name__)
app.config['SECRET_KEY'] = "vnkdjnfjknfl1232#"
socketio = SocketIO(app)

@app.route("/")
def sessions():
    return render_template("basic_template.html")

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@app.route("/camera")
def camera_access():
    return render_template("camera_acc.html")

@socketio.on("my event")
def handle_my_custom_event(json,methods=["GET","POST"]):
    print("Received my image : ")
    if len(json) == 1:
        print(json)
    else:
        height = 20
        width = 20
        arr=[[0 for j in range(width)] for i in range(height)]
        bw_data = []
        dic = json["image_data"]
        print(len(dic))
        for i in range(0,len(dic),4):
            bw_data.append(math.floor((dic[str(i)]+dic[str(i+1)]+dic[str(i+2)])/3))
        # print(np.shape(bw_data))
        bw_data = np.array(bw_data)

        for i in range(height):
            for j in range(width):
                arr[i][j] = bw_data[i*height + j]
        arr = np.array(arr)
        print(np.shape(arr),arr)
        new_arr = np.reshape(arr,[1,height,width,1])
        print(np.shape(new_arr))
        # new_image_array = np.reshape(bw_data,[1,height,width,1])
        # print(bw_data)
        # print(len(bw_data),len(new_image_array))
    # print(json["image_data"])
    json["response"] = "hello there !"
    socketio.emit("my response",json,callback = messageReceived)

if __name__ == "__main__":
    socketio.run(app,port=2000,debug=True)
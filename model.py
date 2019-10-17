from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from flask import Flask,render_template, request, flash, url_for,Response, redirect
from werkzeug import secure_filename
import os
from picamera import PiCamera
import cv2
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
import json
#import socket

app = Flask(__name__)
vc = cv2.VideoCapture(0)

item_list = {
	"401":{
			"Name":"horlicks-Medium",
			"Cost":"300"
			},

	"402":{
			"Name":"colgate-toothpaste-small",
			"Cost":"20"
		},
	"403":{
			"Name":"colgate-toothpaste-medium",
			"Cost":"60"
		},
	"404":{
			"Name":"Peanut Butter",
			"Cost":"350"
		}
}



rootCAPath = "./AmazonRootCA1.pem"
certificatePath = "./8a48f1bc6a.cert.pem"
privateKeyPath = "./8a48f1bc6a.private.key"
host = "a1s5ihhuzh4ik5-ats.iot.us-east-1.amazonaws.com"
port = 8883
clientId = "cam1"
topic = "camera/info"

global count
count = 401

@app.route('/')
def hello_world(name=None):
    return render_template('index.html', name=name)

def gen(): 
   """Video streaming generator function.""" 
   while True: 
       rval, frame = vc.read() 
       cv2.imwrite('pic.jpg', frame) 
       yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')



@app.route('/video_feed')
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(), 
         mimetype='multipart/x-mixed-replace; boundary=frame') 



@app.route('/capture', methods = ['GET', 'POST'])
def capture():
    ret,frame = vc.read()
    print(ret)
    print(frame)
    PATH = '/home/pi/flaskappv2/static/img/image.jpg'

    cv2.imwrite(PATH, frame)
    cv2.waitKey(0)
    return redirect('/train')

@app.route('/train', methods = ['GET', 'POST'])
def train():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    PATH = '/home/pi/flaskappv2/static/img/image.jpg'
    img = image.load_img(PATH, target_size=(300, 300))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = loaded_model.predict(images, batch_size=10)
    print(classes[0])
    if classes[0]>0.5:
        p_id = "101"
        p_name = "horlicks-Medium"
        p_cost = "300"
    elif (classes[0]>0.5):
        p_id = "104"
        p_name = "peanut-butter"
        p_cost = "60"
    elif (classes[0]>0.5):
        p_id = "102"
        p_name = "colgate-toothpaste-small"
        p_cost = "60"
    else:
        p_id = "103"
        p_name = "colgate-toothpaste-medium"
        p_cost = "60"
    

    message = {}
    message['productID'] = p_id
    message['productName'] = p_name
    message['productCost'] = p_cost
    messageJson = json.dumps(message)

    camMQTTClient = AWSIoTMQTTClient(clientId)
    camMQTTClient.configureEndpoint(host, port)
    camMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    camMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    camMQTTClient.configureOfflinePublishQueueing(-1)
    camMQTTClient.configureDrainingFrequency(2)  
    camMQTTClient.configureConnectDisconnectTimeout(10)  
    camMQTTClient.configureMQTTOperationTimeout(5)  

    camMQTTClient.connect()	
    camMQTTClient.publish(topic,messageJson,1)
   

    return messageJson;

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
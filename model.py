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
#import socket

app = Flask(__name__)
vc = cv2.VideoCapture(0)


# UPLOAD_FOLDER = '/upload/'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    #camera = PiCamera() 
    #camera.start_preview()
    #camera.capture('/home/pi/flaskappv2/static/img/image.jpg')
    #camera.stop_preview()
    #return render_template('index.html')
    
    #cap = cv2.VideoCapture(1)
    ret,frame = vc.read()
    print(ret)
    print(frame)
    PATH = '/home/pi/flaskappv2/static/img/image.jpg'
    grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  
    #cv2.imgshow("capturing", grey)
    cv2.imwrite(PATH, frame)
    cv2.waitKey(0)

    #img1=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #plt.imgshow(img1)
    #plt.title('color Image RGB')
    #plt.xticks([])
    #plt.yticks([])
    #plt.show()
    #cap.release()
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
       print(" is a Colgate")
       status = "Colgate"
    else:
       print(" is a Horlicks")
       status = "Horlicks"

    return render_template('index.html',stats=status)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
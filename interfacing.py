from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os


json_file = open('model.json', 'r')
loaded_model = json_file.read()

json_file.close()
model = tf.keras.models.model_from_json(loaded_model_json)
model.load_weights("model.h5")

path = '/content/image.jpg'

img = image.load_img(path, target_size(300,300))
x =  image.img_to_array(img)
x =  np.expand_dims(x, axis=0)

images = np.vstack([x])
classes = loaded_model.predict(images, batch_size=10)
if classes[0] > 0.5:
	print(fn + "is a colgate")
else:
	print(fn + "is a Horlicks")




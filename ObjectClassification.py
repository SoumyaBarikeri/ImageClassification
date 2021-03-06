#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:40:27 2019

@author: soumya
"""

from keras.preprocessing.image import ImageDataGenerator,image
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = '/Users/soumya/Documents/Mannheim-Data-Science/Sem 2/Computer vision/dogs-vs-cats/train'
validation_data_dir = '/Users/soumya/Documents/Mannheim-Data-Science/Sem 2/Computer vision/dogs-vs-cats/validation'
nb_train_samples = 3000
nb_validation_samples = 1200
epochs = 20
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)
    
    
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#model.add(Conv2D(32, (3, 3)))
#model.add(Activation('relu'))
#model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(3))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)


train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')


model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

model.save_weights('first_try2.h5')

model.save('first_try2.h5')

from keras.preprocessing.image import img_to_array, load_img
import numpy as np

for i in range(30):
    test_model = load_model('first_try2.h5')
    
    img = load_img('/Users/soumya/Documents/Mannheim-Data-Science/Sem 2/Computer vision/dogs-vs-cats/train/cats/cat.{}.jpg'.format(i),False,target_size=(img_width,img_height))
    
    x = img_to_array(img)
    
    x = np.expand_dims(x, axis=0)
    x = np.reshape(x,[1,150,150,3])
    preds = test_model.predict_classes(x)
    
    probs = test_model.predict_proba(x)
    
    print("Class predicted {}".format(preds))
    print("Class predicted probability {}".format(probs))

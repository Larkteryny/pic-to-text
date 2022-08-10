import tensorflow as tf
import numpy as np
from PIL import Image

# Read dataset
data_dir = ""
batch_size = 50
img_dims = (28, 28)  # 28x28 to conform with MNIST

normalize = tf.keras.layers.Rescaling(1. / 255)  # Dataset is not normalized for diagnostic purposes

ds_train = tf.keras.utils.image_dataset_from_directory(
	data_dir,
	validation_split=0.2,
	subset="training",
	seed=420,
	image_size=img_dims)\
	.map(lambda X, y: (normalize(X), y))\
	.cache().prefetch(buffer_size=tf.data.AUTOTUNE)  # Optimize data loading

ds_valid = tf.keras.utils.image_dataset_from_directory(
	data_dir,
	validation_split=0.2,
	subset="validation",
	seed=420,
	image_size=img_dims)\
	.map(lambda X, y: (normalize(X), y))\
	.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

ds_train = ds_train
ds_valid = ds_valid.cache()

# Create model
model = tf.keras.models.Sequential([
	tf.keras.layers.Flatten(input_shape=img_dims),
	tf.keras.layers.Dense(units=128, activation=tf.nn.relu),
	tf.keras.layers.Dense(units=128, activation=tf.nn.relu),
	tf.keras.layers.Dense(units=62, activation=tf.nn.softmax)
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(ds_train, validation_data=ds_valid, epochs=5)
model.save("ocr_0.model")

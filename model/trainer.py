from PIL import Image
import tensorflow as tf

# Read dataset
X_train = None
y_train = None

# Create model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(25, 25)))
model.add(tf.keras.layers.Dense(units=256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=5)
model.save("ocr_0.model")

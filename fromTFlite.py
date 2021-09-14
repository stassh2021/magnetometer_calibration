# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 17:57:53 2021

@author: 6degt
"""


# The conversion from a TensorFlow SaveModel or tf.keras H5 model to .tflite is an irreversible process. Specifically, the original model topology is optimized during the compilation by the TFLite converter, which leads to some loss of information. Also, the original tf.keras model's loss and optimizer configurations are discarded, because those aren't required for inference.

# However, the .tflite file still contains some information that can help you restore the original trained model. Most importantly, the weight values are available, although they might be quantized, which could lead to some loss in precision.

# The code example below shows you how to read weight values from a .tflite file after it's created from a simple trained tf.keras.Model.

import numpy as np
import tensorflow as tf

# First, create and train a dummy model for demonstration purposes.
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, input_shape=[5], activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")])
model.compile(loss="binary_crossentropy", optimizer="sgd")

xs = np.ones([8, 5])
ys = np.zeros([8, 1])
model.fit(xs, ys, epochs=1)

# Convert it to a TFLite model file.
converter = tf.lite.TFLiteConverter.from_keras_model_file(model)
tflite_model = converter.convert()
# open("converted.tflite", "wb").write(tflite_model)

# # Use `tf.lite.Interpreter` to load the written .tflite back from the file system.
# interpreter = tf.lite.Interpreter(model_path="converted.tflite")
# all_tensor_details = interpreter.get_tensor_details()
# interpreter.allocate_tensors()

# for tensor_item in all_tensor_details:
#   print("Weight %s:" % tensor_item["name"])
#   print(interpreter.tensor(tensor_item["index"])())
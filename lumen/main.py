import json

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB4
import numpy as np
import matplotlib.pyplot as plt

model_path = "./model/region_guessr_reg_eff_net_mdl_wts.hdf5"
IMAGE_SIZE = 128
BATCH_SIZE = 128
json_x_path = "./gdrive/MyDrive/lumen/transforms/x.json"
json_y_path = "./gdrive/MyDrive/lumen/transforms/y.json"

def build_model():
  inputs = layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
  model = EfficientNetB4(include_top=False, input_tensor=inputs, weights="imagenet")
  x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
  x = layers.BatchNormalization()(x)
  top_dropout_rate = 0.1
  x = layers.Dropout(top_dropout_rate, name="top_dropout")(x)
  outputs = layers.Dense(2, activation="sigmoid", name="pred")(x)
  model = tf.keras.Model(inputs, outputs, name="EfficientNet")
  optimizer = tf.keras.optimizers.Adam(learning_rate=1e-2)
  model.compile(optimizer=optimizer, loss="mean_squared_error", metrics=["mean_squared_error"])
  return model


def dummy_fun():
    result = {"state": {"coordinates": (70, 50)}}
    return result

def transform(json_x_path, json_y_path, data):
  with open(json_x_path, 'r') as file:
    transformation_x = json.load(file)
  with open(json_y_path, 'r') as file:
    transformation_y = json.load(file)
  transformed_data = []
  for coords in data:
    transformed = []
    for trans in transformation_x:
      if coords[1] <= trans["target_range_end"]:
        range_perc = (coords[1] - trans["target_range_start"])/(trans["target_range_end"] - trans["target_range_start"])
        transformed.append(range_perc * (trans["original_range_end"] - trans["original_range_start"]) + trans["original_range_start"])
        if range_perc * (trans["original_range_end"] - trans["original_range_start"]) + trans["original_range_start"] > 1:
          print("Error: x is bigger then 1")
        break
    for trans in transformation_y:
      if coords[0] <= trans["target_range_end"]:
        range_perc = (coords[0] - trans["target_range_start"])/(trans["target_range_end"] - trans["target_range_start"])
        transformed.append(range_perc * (trans["original_range_end"] - trans["original_range_start"]) + trans["original_range_start"])
        if range_perc * (trans["original_range_end"] - trans["original_range_start"]) + trans["original_range_start"] > 1:
          print("Error: y is bigger then 1")
        break
    transformed_data.append(transformed)
  return transformed_data

def predict_coords(images):
    model = build_model()
    model.load_weights(model_path)
    predictions = model(images)
    predictions = transform(json_x_path=json_x_path, json_y_path=json_y_path, data=predictions)
    return predictions

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB4
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import json
model_path = "./model/region_guessr_reg_eff_net_mdl_wts.hdf5"
IMAGE_SIZE = 128
BATCH_SIZE = 128
json_x_path = "./transforms/x.json"
json_y_path = "./transforms/y.json"

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

images_path = "path"
results_path = "results.csv"
results_file = open(results_path, "w", newline="")
csv_writer = csv.writer(results_file)
csv_writer.writerow(["uuid", "latitude", "longitude"])
model = build_model()
model.load_weights(model_path)
for folder in os.listdir(images_path)[:10]:
    images = []
    for image_name in os.listdir(images_path + "/" + folder):
        image = cv2.imread(images_path + "/" + folder + "/" + image_name)
        image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
        images.append(image)
    predictions = model(np.array(images))
    predictions = transform(json_x_path=json_x_path, json_y_path=json_y_path, data=predictions)
    result = {"x": 0, "y": 0}
    for prediction in predictions:
        result["x"] += np.array(prediction[0])
        result["y"] += np.array(prediction[1])
    result["x"] = result["x"] / len(predictions)
    result["y"] = result["y"] / len(predictions)
    if result["x"] > 1:
        result["x"] = 1
    if result["y"] > 1:
        result["y"] = 1
    result["x"] = result["x"] * (19.45 - 13.5) + 13.5
    result["y"] = result["y"] * (46.55 - 42.4) + 42.4
    csv_writer.writerow([folder, result["y"], result["x"]])
results_file.close()

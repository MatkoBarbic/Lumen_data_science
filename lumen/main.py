import json
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB4
import cv2
import numpy as np

model_path = "./model/region_guessr_reg_eff_net_mdl_wts.hdf5"
IMAGE_SIZE = 128
BATCH_SIZE = 128
json_x_path = "./transforms/x.json"
json_y_path = "./transforms/y.json"
map_path = "../lil/src/images/croatia-satellite-map.jpg"

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

def visualize_results(pred, map_path):
  map = cv2.imread(map_path)
  x0 = int(pred[0] * map.shape[0])
  y0 = map.shape[1] - int(pred[1] * map.shape[1])

  cv2.circle(map, (x0, y0), 15, (0, 0, 255), -1)
  cv2.imwrite("../lil/src/images/result_visualization.jpg", map)

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

def predict_coords(request):
  images = []
  try:
    for i in request.FILES:
      image = cv2.imread(request.FILES[i].temporary_file_path())
      image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
      images.append(image)
  except:
    for i in request.FILES:
      image = cv2.imdecode(np.frombuffer(request.FILES[i].read(), np.uint8), 1)
      image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
      images.append(image)
  model = build_model()
  model.load_weights(model_path)
  predictions = model(np.array(images))
  predictions = transform(json_x_path=json_x_path, json_y_path=json_y_path, data=predictions)
  result = {"x": 0, "y": 0, "image": None}
  for prediction in predictions:
    result["x"] += np.array(prediction[0])
    result["y"] += np.array(prediction[1])
  result["x"] = result["x"] / len(predictions)
  result["y"] = result["y"] / len(predictions)
  visualize_results((result["x"], result["y"]), map_path)
  result["image"] = "../images/result_visualization.jpg"
  return result
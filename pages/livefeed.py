import streamlit as st
from streamlit_autorefresh import st_autorefresh
import cv2
import numpy as np
import tensorflow as tf
from streamlit_extras.switch_page import switch_page
import requests

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

# Load TFLite models
dog_model = tf.lite.Interpreter(model_path="dog_saved_model/dog_float16.tflite")
dog_model.allocate_tensors()
behavior_model = tf.lite.Interpreter(model_path="best1_saved_model/best1_float16.tflite")
behavior_model.allocate_tensors()

def run_inference(model, image):
    input_details = model.get_input_details()
    output_details = model.get_output_details()
    model.set_tensor(input_details[0]['index'], image)
    model.invoke()
    return model.get_tensor(output_details[0]['index'])

def process_frame(frame):
    input_image = cv2.resize(frame, (224, 224))
    input_image = np.expand_dims(input_image.astype(np.float32) / 255.0, axis=0)
    dog_results = run_inference(dog_model, input_image)
    boxes = []
    for result in dog_results[0]:
        if len(result) >= 6 and result[4] > 0.5:  # Confidence threshold
            x_min, y_min, x_max, y_max = map(int, result[:4])
            boxes.append((x_min, y_min, x_max, y_max))
    if boxes:
        largest_box = max(boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
        x1, y1, x2, y2 = largest_box
        dog_crop = frame[y1:y2, x1:x2]
        if dog_crop.size > 0:
            dog_resized = cv2.resize(dog_crop, (224, 224))
            dog_resized = np.expand_dims(dog_resized.astype(np.float32) / 255.0, axis=0)
            behavior_results = run_inference(behavior_model, dog_resized)
            behavior = ["Sitting", "Standing", "Lying"][int(np.argmax(behavior_results[0]))]  # Example labels
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, behavior, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            requests.post("http://127.0.0.1:8000/save-behavior-log/", json={
                "behavior": behavior, "timestamp": st.session_state.get('timestamp', '')
            })
    return frame

st_autorefresh(interval=1000)  # Refresh every second
cap = cv2.VideoCapture("rtsp://admin:L2A51CBA@192.168.0.102:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif")
ret, frame = cap.read()
cap.release()
if ret:
    frame = process_frame(frame)
    st.image(frame, channels="BGR")
else:
    st.write("Failed to capture frame.")

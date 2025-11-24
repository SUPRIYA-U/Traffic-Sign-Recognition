from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

class_names = {
    0: "Speed Limit 20",
    1: "Speed Limit 30",
    2: "Speed Limit 50",
    3: "Speed Limit 60",
    4: "Speed Limit 70",
    5: "Speed Limit 80",
    6: "End of Speed Limit 80",
    7: "Speed Limit 100",
    8: "Speed Limit 120",
    9: "No passing",
    10: "No passing for vehicles over 3.5 metric tons",
    11: "Right-of-way at the next intersection",
    12: "Priority road",
    13: "Yield",
    14: "Stop",
    15: "No vehicles",
    16: "Vehicles over 3.5 metric tons prohibited",
    17: "No entry",
    18: "General caution",
    19: "Dangerous curve to the left",
    20: "Dangerous curve to the right",
    21: "Double curve",
    22: "Bumpy road",
    23: "Slippery road",
    24: "Road narrows on the right",
    25: "Road work",
    26: "Traffic signals",
    27: "Pedestrians",
    28: "Children crossing",
    29: "Bicycles crossing",
    30: "Beware of ice/snow",
    31: "Wild animals crossing",
    32: "End of all restrictions",
    33: "Turn right ahead",
    34: "Turn left ahead",
    35: "Ahead only",
    36: "Go straight or right",
    37: "Go straight or left",
    38: "Keep right",
    39: "Keep left",
    40: "Roundabout mandatory",
    41: "End of no passing",
    42: "End of no passing by vehicles over 3.5 metric tons"
}

model = tf.keras.models.load_model("models/cnn_model.h5")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    sign_name = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', prediction=None, sign_name=None)
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', prediction=None, sign_name=None)
        img = Image.open(file.stream).resize((32, 32))
        img_array = np.array(img) / 255.0
        if img_array.shape[-1] != 3:
            img_array = np.stack([img_array]*3, axis=-1)
        img_array = np.expand_dims(img_array, axis=0)
        pred = model.predict(img_array)
        predicted_class = int(np.argmax(pred, axis=1)[0])
        sign_name = class_names.get(predicted_class, f"Class {predicted_class}")
        prediction = f"Predicted class: {predicted_class}"
    return render_template('index.html', prediction=prediction, sign_name=sign_name)

if __name__ == '__main__':
    app.run(debug=True)

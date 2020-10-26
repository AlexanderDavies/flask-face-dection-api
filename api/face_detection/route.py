from flask import Blueprint, render_template, jsonify, make_response, request, send_file
from flasgger import swag_from
import cv2
import numpy as np
import os

face_detection = Blueprint('/api/vi', __name__, template_folder='templates',
                           static_folder='static', static_url_path='/face_detection/static')


@face_detection.route('/', methods=['GET'])
@swag_from({
    'responses': {
        '200': {
            'description': "html page for loading images",
            "content": {
                "text/html": {
                    "example":  "<html><body>index.html page</body></html>"
                }
            }
        }
    }
})
def get_ui():
    response = make_response(render_template('index.html'))
    response.headers.set('Cache-Control', 'no-cache')
    return response


@face_detection.route('/', methods=['POST'])
@swag_from({
    'requestBody': {
        'description': "image to detect faces ",
        "required": "true",
        "content": {
            "image/png": {
                "schema": {
                    "type": "string",
                    "format": "binary"
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': "result image with detected faces boxed",
            "content": {
                "image/png": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            }
        }
    }
})
def detect_faces():
    unint8 = np.fromstring(request.data, np.uint8)

    image = cv2.imdecode(unint8, cv2.IMREAD_COLOR)

    dir = os.path.dirname(__file__)

    path = os.path.join(dir, "haarcascade_frontalface_default.xml")

    faceCascade = cv2.CascadeClassifier(path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    retval, buffer = cv2.imencode('.jpg', image)

    response = make_response(buffer.tobytes())

    return response, 200

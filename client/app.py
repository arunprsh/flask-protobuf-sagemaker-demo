import json
import logging

import requests
from flask import Flask, render_template, request

from deserialize import deserialize_response
from serialize import serialize_image
import traceback

app = Flask(__name__)
proxy_endpoint = 'http://10.10.0.3:8081/proxy/predict'
logging.basicConfig(level=logging.ERROR)

# DO NOT set content-type since the post call to proxy is using proto-buf encoded data
# headers = {'content-type': 'image/jpeg'}


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/client/predict', methods=['POST'])
def predict():
    try:
        images_bytes: bytes = request.data
        serialized_image = serialize_image(images_bytes)
        response = requests.post(proxy_endpoint, data=serialized_image)
        deserialized_response = deserialize_response(response.content)
        return json.dumps(deserialized_response)
    except Exception as e:
        logging.error(e)
        traceback.print_exc()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

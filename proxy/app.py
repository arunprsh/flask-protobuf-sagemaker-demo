from flask import Flask, render_template, request

from invoke import invoke_sagemaker_endpoint_by_data
from serialize import serialize_response

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/proxy/predict', methods=['POST'])
def predict():
    response = invoke_sagemaker_endpoint_by_data(request.data)
    serialized_response = serialize_response(response)
    return serialized_response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

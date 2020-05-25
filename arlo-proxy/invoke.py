from io import BytesIO

from PIL.JpegImagePlugin import JpegImageFile
from deserialize import deserialize_image
from numpy import ndarray
from PIL import Image
import numpy as np
import traceback
import logging
import boto3
import json

logging.basicConfig(level=logging.ERROR)
sagemaker_endpoint = 'sagemaker-mxnet-2020-05-24-00-42-38-836'
sagemaker_runtime_client = boto3.client('sagemaker-runtime')


def transform_pixel_value(image_list: list) -> list:
    image_transformed = []
    try:
        for row in image_list:
            row_transformed = []
            for value in row:
                if value > 0:
                    row_transformed.append(1)
                else:
                    row_transformed.append(0)
            image_transformed.append(row_transformed)
    except Exception as e:
        logging.error(e)
        raise e
    return image_transformed


def load_and_transform_payload(image_path: str) -> str:
    try:
        jpeg_image_file: JpegImageFile = Image.open(image_path)
        image_ndarray: ndarray = np.array(jpeg_image_file)
        image_list: list = image_ndarray.tolist()
        image_transformed: list = transform_pixel_value(image_list)
        payload = json.dumps([image_transformed])
    except Exception as e:
        logging.error(e)
        raise e
    return payload


def load_and_transform_data(data: bytes) -> str:
    try:
        jpeg_image_file: JpegImageFile = Image.open(BytesIO(data))
        image_ndarray: ndarray = np.array(jpeg_image_file)
        image_list: list = image_ndarray.tolist()
        image_transformed: list = transform_pixel_value(image_list)
        payload = json.dumps([image_transformed])
    except Exception as e:
        logging.error(e)
        raise e
    return payload


def get_prediction(response: json) -> dict:
    try:
        response_body = response['Body']
        dict_response = eval(response_body.read().decode('utf-8'))
        labeled_predictions = list(zip(range(10), dict_response[0]))
        labeled_predictions.sort(key=lambda label_and_probability: 1.0 - label_and_probability[1])
        predicted_class = labeled_predictions[0][0]
        prediction = {"label": str(predicted_class)}
    except Exception as e:
        logging.error(e)
        raise e
    return prediction


def invoke_sagemaker_endpoint_by_path(image_path: str) -> str:
    response = ''
    try:
        payload = load_and_transform_payload(image_path)
        response = sagemaker_runtime_client.invoke_endpoint(EndpointName=sagemaker_endpoint,
                                                            Body=payload,
                                                            ContentType='application/json',
                                                            Accept='application/json'
                                                            )
        response = get_prediction(response)
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
    return json.dumps(response)


def invoke_sagemaker_endpoint_by_data(data) -> dict:
    response = ''
    try:
        data: bytes = deserialize_image(data)
        payload = load_and_transform_data(data)
        response = sagemaker_runtime_client.invoke_endpoint(EndpointName=sagemaker_endpoint,
                                                            Body=payload,
                                                            ContentType='application/json',
                                                            Accept='application/json'
                                                            )
        response = get_prediction(response)
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
    return response


if __name__ == '__main__':
    sagemaker_response = invoke_sagemaker_endpoint_by_path('img_1.jpg')
    print(sagemaker_response)

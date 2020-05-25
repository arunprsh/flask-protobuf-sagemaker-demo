import logging

import response_pb2


def serialize_response(response: dict) -> bytes:
    try:
        prediction = response_pb2.Prediction()
        prediction.label = response['label']
        serialized_response = prediction.SerializeToString()
    except Exception as e:
        logging.error(e)
        raise e
    return serialized_response

import logging

import response_pb2


def deserialize_response(response: bytes) -> dict:
    deserialized_response = {}
    try:
        prediction = response_pb2.Prediction().FromString(response)
        label = prediction.label
        deserialized_response['label'] = label
    except Exception as e:
        logging.error(e)
        raise e
    return deserialized_response

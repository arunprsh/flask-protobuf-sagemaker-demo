import logging

import payload_pb2

logging.basicConfig(level=logging.ERROR)


def deserialize_image(image: bytes) -> bytes:
    try:
        image_deserialized = payload_pb2.Payload().FromString(image)
        image_deserialized_bytes = image_deserialized.data
    except Exception as e:
        logging.error(e)
        raise e
    return image_deserialized_bytes

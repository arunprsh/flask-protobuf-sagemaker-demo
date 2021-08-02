import logging

import payload_pb2 as payload_pb2

logging.basicConfig(level=logging.ERROR)


def img_to_byte_arr(img_path: str) -> bytearray:
    byte_arr = bytearray()
    with open(img_path, 'rb') as image:
        try:
            f = image.read()
            byte_arr = bytearray(f)
        except Exception as e:
            logging.error(e)
            raise e
    return byte_arr


def serialize_image(image: bytes) -> bytes:
    try:
        payload = payload_pb2.Payload()
        payload.data = image
        payload_serialized = payload.SerializeToString()
    except Exception as e:
        logging.error(e)
        raise e
    return payload_serialized


if __name__ == '__main__':
    images_bytes = img_to_byte_arr('img_1.jpg')
    print(images_bytes)

#!/bin/bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. payload.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. response.proto
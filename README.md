# flask-protobuf-sagemaker-demo
### Invoke Sagemaker MXNet endpoint from a Docker container (using protobuf)



#### 1. Setup `Flask Client` using client 
- Build a docker image using the `Dockerfile` inside client
- Push the container image to your ECR private registry


#### 2. Setup `Flask Proxy` using proxy
- Build a docker image using the `Dockerfile` inside client
- Push the container image to your ECR private registry


#### 3. Create MXNet Sagemaker endpoint
- `mxnet-mnist.ipynb` contains notebook code to train a MXNet image classification model on `MNIST` data `(28X28)`
- Run the notebook to train, save and deploy the saved model as a Sagemaker inference endpoint


#### 4. Create EC2 instance and setup Docker cluster with 2 containers (client & proxy)
- Pull client & proxy images from ECR
- Run client docker container - this starts flask client on port `8080`
- Run proxy docker container - this starts flask proxy on port `8081`
- Flask client receives the input image from the user. It serializes the received image in `protobuf` format
- Flask proxy receives this payload in protobuf format from the client. It then deserializes 
the protobuf payload and invokes the MXNet Sagemaker endpoint to get the prediction (label)
- Flask proxy then serializes the prediction response in protobuf format to send it back to the 
client (which is returned to the user)

**P.S.:** Ensure to run both container in `subnet` network mode to enable communication between them :+1:


#### Steps to compile `.proto` files 
The protocol buffer files are needed to define the schema of the payload (request and response).
They are also used to generate the protobuf definitions `payload_pb2.py` and `response_pb2.py`.
If you make any changes to the `.proto` files, you would have to re-generate the protobuf definitions by
executing the following commands.

```shell script
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. payload.proto
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. response.proto
```
or run the `generate_definitions.sh` bash script 


#### Load Test Config:
- 1000 threads and 100 seconds ramp-up
- Start 1 Thread every 0.1 second until all threads are started by the time the 100 seconds are up

#### Other files:
##### 1. test-results.csv - contains latency test results for 1000 calls
##### 2. latency.png shows latency results as a line graph for 1000 calls

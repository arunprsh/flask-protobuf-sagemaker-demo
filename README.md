# flask-protobuf-sagemaker-demo
### Invoke Sagemaker MXNet endpoint from a Docker container (using protobuf)



#### 1. Setup `Flask Client` using arlo-client 
- Build a docker image using the `Dockerfile` inside arlo-client
- Push the container image to your ECR private registry


#### 2. Setup `Flask Proxy` using arlo-proxy
- Build a docker image using the `Dockerfile` inside arlo-client
- Push the container image to your ECR private registry


#### 3. Create MXNet Sagemaker endpoint
- `mxnet-mnist.ipynb` contains notebook code to train a MXNet image classification model on `MNIST` data `(28X28)`
- Run the notebook to train, save and deploy the saved model as a Sagemaker inference endpoint


#### 4. Create EC2 instance and setup Docker cluster with 2 containers (client & proxy)
- Pull arlo-client & arlo-proxy images from ECR
- Run arlo-client docker container - this starts flask client on port `8080`
- Run arlo-proxy docker container - this starts flask proxy on port `8081`
- Flask client receives the input image from the user. It serializes the received image in `protobuf` format
- Flask proxy receives this payload in protobuf format from the client. It then deserializes 
the protobuf payload and invokes the MXNet Sagemaker endpoint to get the prediction (label)
- Flask proxy then serializes the prediction response in protobuf format to send it back to the 
client (which is returned to the user)

P.S.: Ensure to run both container in `subnet` network mode to enable communication between them

#### Other files:
##### 1. arlo-test-results.csv - contains latency test results for 1000 calls
##### 2. latency.png shows latency results as a line graph for 1000 calls

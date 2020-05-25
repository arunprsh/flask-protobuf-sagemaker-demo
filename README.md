# flask-protobuf-sagemaker-demo
### Invoke Sagemaker MXNet endpoint from a Docker container (using protobuf)


1. Create MXNet MNIST Sagemaker endpoint
2. Create EC2 instance and setup Docker
3. Setup Flask client server using arlo-client 
- Build docker using the Dockerfile
- Create a docker container and start the flask server on port 8080
- Run in subnet network mode 
- This client server serializes the recieved image in protobuf format
4. Setup Flask proxy server using arlo-proxy
- Build docker using the Dockerfile
- Create a docker container and start the flask server on port 8081
- Run in subnet network mode 
- This proxy server receives the payload in protobuf format from the client server
- It deserializes the protobuf payload and invokes the MXNet Sagemaker endpoint to get the prediction
- It then serializes the response in protobuf to send it back to the client 


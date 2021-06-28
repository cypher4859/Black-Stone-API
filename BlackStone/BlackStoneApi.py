from validations import validateAction
import os

from flask import Flask, request
import grpc

from docker_manager_pb2 import ContainerAction, ContainerManagerRequest, ContainerManagerResponse
from docker_manager_pb2_grpc import ContainerManagerStub

app = Flask(__name__)

container_manager_host = os.getenv("CONTAINER_MANAGER_HOST", "localhost")
container_manager_channel = grpc.insecure_channel(
    f"{container_manager_host}:50051"
)
container_manager_client = ContainerManagerStub(container_manager_channel)


@app.route("/docker-manager", methods=["GET", "POST"])
def manageContainer():
    container_id = request.form['containerId']
    container_action = ContainerAction.Value(request.form['action'])
    container_image = request.form['image']
    requestArgs = { 'containerId': container_id, 'action': container_action, 'image': container_image }
    containerRequest = ContainerManagerRequest(
        **requestArgs
    )
    container_manager_response = container_manager_client.ManageContainer(containerRequest)
    return container_manager_response.result
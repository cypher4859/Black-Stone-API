from validations import validateAction
import os

from flask import Flask, request
import grpc
import json
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
    req = request.get_json()
    # print(req)
    container_id = req['containerId']
    container_action = ContainerAction.Value(req['action'])
    container_image = req['image']
    container_port = req['port']
    container_volume = json.dumps(req['volumes'])

    requestArgs = { 'containerId': container_id, 'action': container_action, 'image': container_image, 'exposedPort': container_port, 'volume': container_volume }
    containerRequest = ContainerManagerRequest(
        **requestArgs
    )
    container_manager_response = container_manager_client.ManageContainer(containerRequest)
    print(container_manager_response.result)
    return container_manager_response.result, 200
    # return 'Thanks', 200
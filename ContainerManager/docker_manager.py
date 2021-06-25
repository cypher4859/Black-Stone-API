from concurrent import futures
import random
import os
from flask import Flask, render_template
import grpc

from docker_manager_pb2 import (
    ContainerAction,
    ContainerManagerRequest,
    ContainerManagerResponse
)
from docker_manager_pb2_grpc import ContainerManagerStub

app = Flask(__name__)

docker_manager_host = os.getenv("DOCKER_MANAGER_HOST", "localhost")
docker_manager_channel = grpc.insecure_channel(
    f"{docker_manager_host}:50051"
)
docker_manager_client = ContainerManagerStub

@app.route("/docker-manage/up")
def dockerContainerUp():
    # startup the container
    print('Its working')
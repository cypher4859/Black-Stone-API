from concurrent import futures
import os
import grpc
import docker_manager_pb2_grpc
import docker
from docker_manager_pb2 import (
    ContainerAction,
    ContainerManagerRequest,
    ContainerManagerResponse
)

client = docker.from_env()

class ContainerManagerService(docker_manager_pb2_grpc.ContainerManagerServicer):
    def ManageContainer(self, request: ContainerManagerRequest, context) -> ContainerManagerResponse:
        # Do the docker things here
        container = client.containers.get(request.containerId)
        if request.action == ContainerAction.UP:
            print('bring it up')
            # Check that the container exists and is currnetly down
        elif request.action == ContainerAction.DOWN:
            print('bring it down')
            container.kill()
        elif request.action == ContainerAction.RECREATE:
            print('rebuild')
            imgae = ''
            container.kill()
            container.remove()
            client.images.pull()
            newContainer = client.containers.create()
            newContainer.start()
            
        elif request.action == ContainerAction.STATUS:
            print('return status')
        else:
            print('dont know what happened')
        containerResult = client.containers.list()
        print(containerResult)
        return ContainerManagerResponse(containerId=request.containerId, result=f"result: {containerResult}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    docker_manager_pb2_grpc.add_ContainerManagerServicer_to_server(ContainerManagerService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
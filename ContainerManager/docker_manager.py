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
        containerResultMessage = ''
        if request.action == ContainerAction.UP:
            print('bring it up')
            container.start()
            containerResultMessage = f"Started up container: {container.name}"
            # Check that the container exists and is currnetly down
        elif request.action == ContainerAction.DOWN:
            print('bring it down')
            container.stop()
            containerResultMessage = f"Stopped container: {container.name}"
        elif request.action == ContainerAction.RECREATE:
            # get the image we're using
            image = request.image
            # stop the current container 
            if container.status != 'exited':
                container.stop()
            print("removing container...")
            # remove the current container
            containerName = container.name
            container.remove()
            print(f"pulling image... {image}")
            # grab the updated image
            client.images.pull(image)
            # run the new container
            newContainer = client.containers.run(image, detach=True, name=containerName)
            print(newContainer.logs)
            containerResultMessage = f"Recreated container: {newContainer.name} with image {image}"
        elif request.action == ContainerAction.STATUS:
            print(f'return status updated: {container.status}')
            containerResultMessage = f"Container {container.name} status: {container.status}"
        else:
            print('dont know what happened')
            containerResultMessage = f"ERROR! Invalid Argument"
        return ContainerManagerResponse(containerId=request.containerId, result=f"{containerResultMessage}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    docker_manager_pb2_grpc.add_ContainerManagerServicer_to_server(ContainerManagerService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
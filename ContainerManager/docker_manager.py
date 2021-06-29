from concurrent import futures
from signal import signal, SIGTERM
import os
import grpc
import docker_manager_pb2_grpc
import docker
import json
from docker_manager_pb2 import (
    ContainerAction,
    ContainerManagerRequest,
    ContainerManagerResponse
)
from grpc_interceptor import ServerInterceptor

client = docker.from_env()

class ContainerManagerService(docker_manager_pb2_grpc.ContainerManagerServicer):
    def ManageContainer(self, request: ContainerManagerRequest, context) -> ContainerManagerResponse:
        # Do the docker things here
        additionalArguments = {}
        if request.exposedPort:
            additionalArguments['ports'] = { f"{request.exposedPort}/tcp" : int(request.exposedPort) } # '25565/tcp': 25565

        # if request.volumeName or request.volumeSource or request.volumeDestination:
        #     additionalArguments['volumes'] = { request.volumeName: { 'bind': request.volumeDestination, 'mode': 'rw' } }
        #     print(additionalArguments['volumes'])

        if request.volume:
            volumeJson = json.loads(request.volume)
            volume = { volumeJson['name']: { volumeJson['type']: volumeJson['destination'], 'mode': volumeJson['mode'] } }
            additionalArguments['volumes'] = volume

        image = request.image

        try:
            container = client.containers.get(request.containerId)
            print(f'Other Arguments: {additionalArguments}')
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
                newContainer = client.containers.run(image, detach=True, name=containerName, **additionalArguments)
                containerResultMessage = f"Recreated container: {newContainer.name} with image {image}"
            elif request.action == ContainerAction.STATUS:
                print(f'return status updated: {container.status}')
                containerResultMessage = f"Container {container.name} status: {container.status}"
            else:
                print('dont know what happened')
                containerResultMessage = f"ERROR! Invalid Argument"
            return ContainerManagerResponse(containerId=request.containerId, result=f"{containerResultMessage}")
        except:
            newContainer = client.containers.run(image, detach=True, name=request.containerId, **additionalArguments)
            containerResultMessage = f"No Container Found. Creating new container {newContainer.name}...\nStatus: {newContainer.status}"
            return ContainerManagerResponse(containerId=request.containerId, result=f"{containerResultMessage}")

class ErrorLogger(ServerInterceptor):
    def intercept(self, method, request, context, method_name):
        try:
            return method(request, context)
        except Exception as e:
            self.log_error(e)
            raise

    def log_error(self, e: Exception) -> None:
        # Do things with the error
        print(e)

def serve():
    interceptors = [ErrorLogger()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    docker_manager_pb2_grpc.add_ContainerManagerServicer_to_server(ContainerManagerService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()

    def handle_sigterm(*_):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(10)
        all_rpcs_done_event.wait(10)
        print("Shut down gracefully")

    signal(SIGTERM, handle_sigterm)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
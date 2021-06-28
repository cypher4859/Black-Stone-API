from docker_manager_pb2 import ContainerAction

def validateAction(containerAction: str):
    if containerAction.capitalize in ContainerAction.values:
        return True
    else:
        return False
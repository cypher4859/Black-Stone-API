# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import docker_manager_pb2 as docker__manager__pb2


class ContainerManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ManageContainer = channel.unary_unary(
                '/ContainerManager/ManageContainer',
                request_serializer=docker__manager__pb2.ContainerManagerRequest.SerializeToString,
                response_deserializer=docker__manager__pb2.ContainerManagerResponse.FromString,
                )


class ContainerManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ManageContainer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ContainerManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ManageContainer': grpc.unary_unary_rpc_method_handler(
                    servicer.ManageContainer,
                    request_deserializer=docker__manager__pb2.ContainerManagerRequest.FromString,
                    response_serializer=docker__manager__pb2.ContainerManagerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ContainerManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ContainerManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ManageContainer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ContainerManager/ManageContainer',
            docker__manager__pb2.ContainerManagerRequest.SerializeToString,
            docker__manager__pb2.ContainerManagerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
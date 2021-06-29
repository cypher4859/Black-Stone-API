# Black-Stone-API
A simple flask API used to control various microservices written in Python using gRPC and ProtoBuffs

- Create the protobuf type file
- Generate the python code making sure to change the directories with:
`python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/docker-manager.proto`

Should be placed on the docker host.

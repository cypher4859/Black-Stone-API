# Black-Stone-API
A simple flask API used to control various microservices written in Python using gRPC and ProtoBuffs

- Create the protobuf type file
- Generate the python code making sure to change the directories with:
`python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto`
- Go to the `BlackStone/` and do `FLASK_APP=BlackStoneApi.py flask run`

### On Windows
- not feasible?

### Needs Automated
- Do a git clone in `/usr/share/`
- Do the setup.sh scripts for both services
- register the daemon services with systemd by `cp`ing the service files into `/etc/services/systemd/`
- do a `systemctl daemon-reload` and start the services
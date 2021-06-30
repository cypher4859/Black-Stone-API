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


### Weird?
- Had to do an apt install python3-flask. The setup wasn't working
- Need to make sure that service is running as a user that can access the python packages
- Make a `run.sh` that works for both microservices so that if the run command needs changed then it can be changed in one place

# rVASP

**Robot VASP for TRISA demonstration and integration**

This is a simple gRPC server that implements a UI workflow and messaging framework to demonstrate sending and receiving transactions using the TRISA InterVASP protocol. The server was built to support a demonstration UI that requires a streaming interface so that a live message flow is achieved. However, the communication protocol between rVASPs also demonstrates how implementers might go about writing InterVASP services in their own codebases. The architecture is as follows:

![Architecture](fixtures/rvasp.png)

## Generating Protocol Buffers

To regenerate the Go and Python code from the protocol buffers:

```
$ go generate ./...
```

This will generate the Go code in `pb/` and the Python code in `pb/rvaspy`. Alternatively you can manually generate the code to specify different directories using the following commands:

```
$ protoc -I . --go_out=plugins=grpc:. api.proto
$ python -m grpc_tools.protoc -I . --python_out=./rvaspy --grpc_python_out=./rvaspy api.proto
```

## Quick Start

To get started using the rVASP, you can run the local server as follows:

```
$ go run ./cmd/rvasp serve
```

The server should now be listening for TRISADemo RPC messages. To send messages using the python API, make sure you can import the modules from `pb/rvaspy` and run the following script:

```python
import grpc

from api_pb2 import *
from api_pb2_grpc import *

CLIENT = "foo"


channel = grpc.insecure_channel("localhost:4434")
stub = TRISADemoStub(channel)

cmds = [
    Command(
        type=ACCOUNT, client=CLIENT, id=1, request=AccountRequest(account="foo@example.com")),
    Command(
        type=TRANSFER, client=CLIENT, id=2, request=TransferRequest(transaction=None)),
]

for msg in stub.LiveUpdates(cmds):
    print(msg)
```

Note that this code is currently untested.
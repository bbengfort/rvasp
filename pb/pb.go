package pb

//go:generate protoc -I . --go_out=plugins=grpc:. api.proto
//go:generate python -m grpc_tools.protoc -I . --python_out=./rvaspy --grpc_python_out=./rvaspy api.proto

package pb

import (
	fmt "fmt"
)

//go:generate protoc -I . --go_out=plugins=grpc:. api.proto
//go:generate python -m grpc_tools.protoc -I . --python_out=../rvaspy/rvaspy --grpc_python_out=../rvaspy/rvaspy api.proto

// Error codes for quick reference and lookups
const (
	ErrNotFound = 404
)

// Errorf is a quick one liner to create error objects
func Errorf(code int32, format string, a ...interface{}) *Error {
	if len(a) > 0 {
		format = fmt.Sprintf(format, a...)
	}
	return &Error{
		Code:    code,
		Message: format,
	}
}

// Error allows protocol buffer Error objects to implement the error interface.
func (e *Error) Error() string {
	return fmt.Sprintf("[%d] %s", e.Code, e.Message)
}

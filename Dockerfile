FROM golang:1.14.5 AS builder

WORKDIR /srv/build

COPY . .
RUN go test ./... && go build -v ./cmd/rvasp

FROM ubuntu:bionic

LABEL maintainer="TRISA <info@trisa.io>"
LABEL description="Robot VASP for TRISA demonstration and integration"

RUN apt-get update && apt-get install -y ca-certificates
RUN apt-get update && apt-get install -y wget gnupg

COPY --from=builder /srv/build/rvasp /bin/

ENTRYPOINT [ "/bin/rvasp", "serve" ]
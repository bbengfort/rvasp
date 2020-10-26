#!/usr/bin/env python3

import grpc
import argparse

from api_pb2 import *  # noqa
from api_pb2_grpc import *  # noqa
from datetime import datetime

CLIENT = "rvaspy"
VERSION = "rvaspy 1.0"
HOST = "localhost:4434"
RFC3339 = "%Y-%m-%dT%H:%M:%S.%fZ"


class RVASP(object):
    """
    An API wrapper for accessing the TRISA Demo rVASP Server.
    """

    # increment message number at the class level
    _msgseq = 0

    def __init__(self, name=CLIENT, host=HOST):
        self.channel = grpc.insecure_channel(host)
        self.stub = TRISADemoStub(self.channel)
        self.name = name

    def _wrap_command(self, rpc, request):
        """
        Helper function to wrap an account status or transfer request into a streaming
        command to actively listen
        """
        self._msgseq += 1
        kwargs = {
            "type": rpc,
            "id": self._msgseq,
            "client": self.name,
        }

        if rpc == ACCOUNT:
            kwargs["account"] = request
        elif rpc == TRANSFER:
            kwargs["transfer"] = request

        return Command(**kwargs)

    def account_request(self, account):
        req = AccountRequest(account=account)
        return self._wrap_command(ACCOUNT, req)

    def transfer_request(self, originator, beneficiary, amount, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()
        if not isinstance(timestamp, str):
            timestamp = timestamp.strftime(RFC3339)

        tx = Transaction(
            originator=originator,
            beneficiary=beneficiary,
            amount=amount,
            timestamp=timestamp
        )
        req = TransferRequest(transaction=tx)
        return self._wrap_command(TRANSFER, req)


def main(args):
    api = RVASP(args.client, args.addr)

    cmds = [
        api.account_request("robert@bobvasp"),
        api.transfer_request("robert@bobvasp", "mary@alicevasp", 42.99)
    ]

    for msg in api.stub.LiveUpdates(iter(cmds)):
        print(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="simple rvasp client")
    parser.add_argument("-v", "--version", action="version", version=VERSION)
    parser.add_argument(
        "-c", "--client", default=CLIENT, type=str, metavar="NAME",
        help="name of the client connecting to the server",
    )
    parser.add_argument(
        "-a", "--addr", default=HOST, type=str, metavar="HOST:PORT",
        help="address to connect to the rvasp server with"
    )

    args = parser.parse_args()
    main(args)
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='api.proto',
  package='pb',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\tapi.proto\x12\x02pb\"&\n\x05\x45rror\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"Y\n\x0bTransaction\x12\x12\n\noriginator\x18\x01 \x01(\t\x12\x13\n\x0b\x62\x65neficiary\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x02\x12\x11\n\ttimestamp\x18\x04 \x01(\t\"7\n\x0fTransferRequest\x12$\n\x0btransaction\x18\x01 \x01(\x0b\x32\x0f.pb.Transaction\")\n\rTransferReply\x12\x18\n\x05\x65rror\x18\x01 \x01(\x0b\x32\t.pb.Error\"!\n\x0e\x41\x63\x63ountRequest\x12\x0f\n\x07\x61\x63\x63ount\x18\x01 \x01(\t\"O\n\x0c\x41\x63\x63ountReply\x12\x18\n\x05\x65rror\x18\x01 \x01(\x0b\x32\t.pb.Error\x12%\n\x0ctransactions\x18\x02 \x03(\x0b\x32\x0f.pb.Transaction\"\x97\x01\n\x07\x43ommand\x12\x15\n\x04type\x18\x01 \x01(\x0e\x32\x07.pb.RPC\x12\n\n\x02id\x18\x02 \x01(\x04\x12\x0e\n\x06\x63lient\x18\x03 \x01(\t\x12\'\n\x08transfer\x18\x0b \x01(\x0b\x32\x13.pb.TransferRequestH\x00\x12%\n\x07\x61\x63\x63ount\x18\x0c \x01(\x0b\x32\x12.pb.AccountRequestH\x00\x42\t\n\x07request\"\xa4\x01\n\x07Message\x12\x15\n\x04type\x18\x01 \x01(\x0e\x32\x07.pb.RPC\x12\n\n\x02id\x18\x02 \x01(\x04\x12\x0e\n\x06update\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\x12%\n\x08transfer\x18\x0b \x01(\x0b\x32\x11.pb.TransferReplyH\x00\x12#\n\x07\x61\x63\x63ount\x18\x0c \x01(\x0b\x32\x10.pb.AccountReplyH\x00\x42\x07\n\x05reply*+\n\x03RPC\x12\t\n\x05NORPC\x10\x00\x12\x0c\n\x08TRANSFER\x10\x01\x12\x0b\n\x07\x41\x43\x43OUNT\x10\x02\x32\x38\n\tTRISADemo\x12+\n\x0bLiveUpdates\x12\x0b.pb.Command\x1a\x0b.pb.Message(\x01\x30\x01\x32\x7f\n\x10TRISAIntegration\x12\x34\n\nTransferTo\x12\x13.pb.TransferRequest\x1a\x11.pb.TransferReply\x12\x35\n\rAccountStatus\x12\x12.pb.AccountRequest\x1a\x10.pb.AccountReplyb\x06proto3')
)

_RPC = _descriptor.EnumDescriptor(
  name='RPC',
  full_name='pb.RPC',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NORPC', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRANSFER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCOUNT', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=685,
  serialized_end=728,
)
_sym_db.RegisterEnumDescriptor(_RPC)

RPC = enum_type_wrapper.EnumTypeWrapper(_RPC)
NORPC = 0
TRANSFER = 1
ACCOUNT = 2



_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='pb.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='pb.Error.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='pb.Error.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=55,
)


_TRANSACTION = _descriptor.Descriptor(
  name='Transaction',
  full_name='pb.Transaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='originator', full_name='pb.Transaction.originator', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='beneficiary', full_name='pb.Transaction.beneficiary', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='pb.Transaction.amount', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='pb.Transaction.timestamp', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=146,
)


_TRANSFERREQUEST = _descriptor.Descriptor(
  name='TransferRequest',
  full_name='pb.TransferRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction', full_name='pb.TransferRequest.transaction', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=148,
  serialized_end=203,
)


_TRANSFERREPLY = _descriptor.Descriptor(
  name='TransferReply',
  full_name='pb.TransferReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='pb.TransferReply.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=205,
  serialized_end=246,
)


_ACCOUNTREQUEST = _descriptor.Descriptor(
  name='AccountRequest',
  full_name='pb.AccountRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account', full_name='pb.AccountRequest.account', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=248,
  serialized_end=281,
)


_ACCOUNTREPLY = _descriptor.Descriptor(
  name='AccountReply',
  full_name='pb.AccountReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='pb.AccountReply.error', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transactions', full_name='pb.AccountReply.transactions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=283,
  serialized_end=362,
)


_COMMAND = _descriptor.Descriptor(
  name='Command',
  full_name='pb.Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='pb.Command.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='pb.Command.id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client', full_name='pb.Command.client', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transfer', full_name='pb.Command.transfer', index=3,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account', full_name='pb.Command.account', index=4,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='request', full_name='pb.Command.request',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=365,
  serialized_end=516,
)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='pb.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='pb.Message.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='pb.Message.id', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='pb.Message.update', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='pb.Message.timestamp', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transfer', full_name='pb.Message.transfer', index=4,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account', full_name='pb.Message.account', index=5,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='reply', full_name='pb.Message.reply',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=519,
  serialized_end=683,
)

_TRANSFERREQUEST.fields_by_name['transaction'].message_type = _TRANSACTION
_TRANSFERREPLY.fields_by_name['error'].message_type = _ERROR
_ACCOUNTREPLY.fields_by_name['error'].message_type = _ERROR
_ACCOUNTREPLY.fields_by_name['transactions'].message_type = _TRANSACTION
_COMMAND.fields_by_name['type'].enum_type = _RPC
_COMMAND.fields_by_name['transfer'].message_type = _TRANSFERREQUEST
_COMMAND.fields_by_name['account'].message_type = _ACCOUNTREQUEST
_COMMAND.oneofs_by_name['request'].fields.append(
  _COMMAND.fields_by_name['transfer'])
_COMMAND.fields_by_name['transfer'].containing_oneof = _COMMAND.oneofs_by_name['request']
_COMMAND.oneofs_by_name['request'].fields.append(
  _COMMAND.fields_by_name['account'])
_COMMAND.fields_by_name['account'].containing_oneof = _COMMAND.oneofs_by_name['request']
_MESSAGE.fields_by_name['type'].enum_type = _RPC
_MESSAGE.fields_by_name['transfer'].message_type = _TRANSFERREPLY
_MESSAGE.fields_by_name['account'].message_type = _ACCOUNTREPLY
_MESSAGE.oneofs_by_name['reply'].fields.append(
  _MESSAGE.fields_by_name['transfer'])
_MESSAGE.fields_by_name['transfer'].containing_oneof = _MESSAGE.oneofs_by_name['reply']
_MESSAGE.oneofs_by_name['reply'].fields.append(
  _MESSAGE.fields_by_name['account'])
_MESSAGE.fields_by_name['account'].containing_oneof = _MESSAGE.oneofs_by_name['reply']
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
DESCRIPTOR.message_types_by_name['TransferRequest'] = _TRANSFERREQUEST
DESCRIPTOR.message_types_by_name['TransferReply'] = _TRANSFERREPLY
DESCRIPTOR.message_types_by_name['AccountRequest'] = _ACCOUNTREQUEST
DESCRIPTOR.message_types_by_name['AccountReply'] = _ACCOUNTREPLY
DESCRIPTOR.message_types_by_name['Command'] = _COMMAND
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.enum_types_by_name['RPC'] = _RPC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), dict(
  DESCRIPTOR = _ERROR,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.Error)
  ))
_sym_db.RegisterMessage(Error)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), dict(
  DESCRIPTOR = _TRANSACTION,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.Transaction)
  ))
_sym_db.RegisterMessage(Transaction)

TransferRequest = _reflection.GeneratedProtocolMessageType('TransferRequest', (_message.Message,), dict(
  DESCRIPTOR = _TRANSFERREQUEST,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.TransferRequest)
  ))
_sym_db.RegisterMessage(TransferRequest)

TransferReply = _reflection.GeneratedProtocolMessageType('TransferReply', (_message.Message,), dict(
  DESCRIPTOR = _TRANSFERREPLY,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.TransferReply)
  ))
_sym_db.RegisterMessage(TransferReply)

AccountRequest = _reflection.GeneratedProtocolMessageType('AccountRequest', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTREQUEST,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.AccountRequest)
  ))
_sym_db.RegisterMessage(AccountRequest)

AccountReply = _reflection.GeneratedProtocolMessageType('AccountReply', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTREPLY,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.AccountReply)
  ))
_sym_db.RegisterMessage(AccountReply)

Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), dict(
  DESCRIPTOR = _COMMAND,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.Command)
  ))
_sym_db.RegisterMessage(Command)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:pb.Message)
  ))
_sym_db.RegisterMessage(Message)



_TRISADEMO = _descriptor.ServiceDescriptor(
  name='TRISADemo',
  full_name='pb.TRISADemo',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=730,
  serialized_end=786,
  methods=[
  _descriptor.MethodDescriptor(
    name='LiveUpdates',
    full_name='pb.TRISADemo.LiveUpdates',
    index=0,
    containing_service=None,
    input_type=_COMMAND,
    output_type=_MESSAGE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRISADEMO)

DESCRIPTOR.services_by_name['TRISADemo'] = _TRISADEMO


_TRISAINTEGRATION = _descriptor.ServiceDescriptor(
  name='TRISAIntegration',
  full_name='pb.TRISAIntegration',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=788,
  serialized_end=915,
  methods=[
  _descriptor.MethodDescriptor(
    name='TransferTo',
    full_name='pb.TRISAIntegration.TransferTo',
    index=0,
    containing_service=None,
    input_type=_TRANSFERREQUEST,
    output_type=_TRANSFERREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AccountStatus',
    full_name='pb.TRISAIntegration.AccountStatus',
    index=1,
    containing_service=None,
    input_type=_ACCOUNTREQUEST,
    output_type=_ACCOUNTREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRISAINTEGRATION)

DESCRIPTOR.services_by_name['TRISAIntegration'] = _TRISAINTEGRATION

# @@protoc_insertion_point(module_scope)
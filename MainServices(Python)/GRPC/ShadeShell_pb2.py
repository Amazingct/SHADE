# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ShadeShell.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10ShadeShell.proto\x12\x05shade\"\x1a\n\x07\x63ommand\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\"\x1c\n\x08response\x12\x10\n\x08response\x18\x01 \x01(\t\"!\n\x03log\x12\x0b\n\x03log\x18\x01 \x01(\t\x12\r\n\x05\x64\x65\x62ug\x18\x02 \x01(\t2\x9c\x01\n\nShadeShell\x12\x31\n\x0eProcessCommand\x12\x0e.shade.command\x1a\x0f.shade.response\x12\x30\n\tShellChat\x12\x0e.shade.command\x1a\x0f.shade.response(\x01\x30\x01\x12)\n\tStreamLog\x12\x0e.shade.command\x1a\n.shade.log0\x01\x62\x06proto3')



_COMMAND = DESCRIPTOR.message_types_by_name['command']
_RESPONSE = DESCRIPTOR.message_types_by_name['response']
_LOG = DESCRIPTOR.message_types_by_name['log']
command = _reflection.GeneratedProtocolMessageType('command', (_message.Message,), {
  'DESCRIPTOR' : _COMMAND,
  '__module__' : 'ShadeShell_pb2'
  # @@protoc_insertion_point(class_scope:shade.command)
  })
_sym_db.RegisterMessage(command)

response = _reflection.GeneratedProtocolMessageType('response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'ShadeShell_pb2'
  # @@protoc_insertion_point(class_scope:shade.response)
  })
_sym_db.RegisterMessage(response)

log = _reflection.GeneratedProtocolMessageType('log', (_message.Message,), {
  'DESCRIPTOR' : _LOG,
  '__module__' : 'ShadeShell_pb2'
  # @@protoc_insertion_point(class_scope:shade.log)
  })
_sym_db.RegisterMessage(log)

_SHADESHELL = DESCRIPTOR.services_by_name['ShadeShell']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMMAND._serialized_start=27
  _COMMAND._serialized_end=53
  _RESPONSE._serialized_start=55
  _RESPONSE._serialized_end=83
  _LOG._serialized_start=85
  _LOG._serialized_end=118
  _SHADESHELL._serialized_start=121
  _SHADESHELL._serialized_end=277
# @@protoc_insertion_point(module_scope)

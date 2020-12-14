# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Advertise.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import api.protoc.Common_pb2 as Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Advertise.proto',
  package='admin',
  syntax='proto3',
  serialized_options=_b('\n\033com.talkweb.admins.protobufB\tAdvertise\242\002\002SN'),
  serialized_pb=_b('\n\x0f\x41\x64vertise.proto\x12\x05\x61\x64min\x1a\x0c\x43ommon.proto\"O\n\x11\x41\x64PositionRequest\x12$\n\x06header\x18\x01 \x01(\x0b\x32\x14.admin.HeaderMessage\x12\x14\n\x0cpositionCode\x18\x03 \x01(\x03\"<\n\x12\x41\x64PositionResponse\x12&\n\x07reqCode\x18\x01 \x01(\x0b\x32\x15.admin.ReqCodeMessage2N\n\tADService\x12\x41\n\nAdPosition\x12\x18.admin.AdPositionRequest\x1a\x19.admin.AdPositionResponseB-\n\x1b\x63om.talkweb.admins.protobufB\tAdvertise\xa2\x02\x02SNb\x06proto3')
  ,
  dependencies=[Common__pb2.DESCRIPTOR,])




_ADPOSITIONREQUEST = _descriptor.Descriptor(
  name='AdPositionRequest',
  full_name='admin.AdPositionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='admin.AdPositionRequest.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='positionCode', full_name='admin.AdPositionRequest.positionCode', index=1,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=40,
  serialized_end=119,
)


_ADPOSITIONRESPONSE = _descriptor.Descriptor(
  name='AdPositionResponse',
  full_name='admin.AdPositionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reqCode', full_name='admin.AdPositionResponse.reqCode', index=0,
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
  serialized_start=121,
  serialized_end=181,
)

_ADPOSITIONREQUEST.fields_by_name['header'].message_type = Common__pb2._HEADERMESSAGE
_ADPOSITIONRESPONSE.fields_by_name['reqCode'].message_type = Common__pb2._REQCODEMESSAGE
DESCRIPTOR.message_types_by_name['AdPositionRequest'] = _ADPOSITIONREQUEST
DESCRIPTOR.message_types_by_name['AdPositionResponse'] = _ADPOSITIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdPositionRequest = _reflection.GeneratedProtocolMessageType('AdPositionRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADPOSITIONREQUEST,
  '__module__' : 'Advertise_pb2'
  # @@protoc_insertion_point(class_scope:admin.AdPositionRequest)
  })
_sym_db.RegisterMessage(AdPositionRequest)

AdPositionResponse = _reflection.GeneratedProtocolMessageType('AdPositionResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADPOSITIONRESPONSE,
  '__module__' : 'Advertise_pb2'
  # @@protoc_insertion_point(class_scope:admin.AdPositionResponse)
  })
_sym_db.RegisterMessage(AdPositionResponse)


DESCRIPTOR._options = None

_ADSERVICE = _descriptor.ServiceDescriptor(
  name='ADService',
  full_name='admin.ADService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=183,
  serialized_end=261,
  methods=[
  _descriptor.MethodDescriptor(
    name='AdPosition',
    full_name='admin.ADService.AdPosition',
    index=0,
    containing_service=None,
    input_type=_ADPOSITIONREQUEST,
    output_type=_ADPOSITIONRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ADSERVICE)

DESCRIPTOR.services_by_name['ADService'] = _ADSERVICE

# @@protoc_insertion_point(module_scope)

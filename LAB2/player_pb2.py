# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: player.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cplayer.proto\x12\x08protblog\"\xa7\x01\n\x0bPlayersList\x12,\n\x06player\x18\x01 \x03(\x0b\x32\x1c.protblog.PlayersList.Player\x1aj\n\x06Player\x12\x10\n\x08nickname\x18\x01 \x02(\t\x12\r\n\x05\x65mail\x18\x02 \x02(\t\x12\x15\n\rdate_of_birth\x18\x03 \x02(\t\x12\n\n\x02xp\x18\x04 \x02(\x05\x12\x1c\n\x03\x63ls\x18\x05 \x02(\x0e\x32\x0f.protblog.Class*5\n\x05\x43lass\x12\x0b\n\x07\x42\x65rserk\x10\x00\x12\x08\n\x04Tank\x10\x01\x12\x0b\n\x07Paladin\x10\x03\x12\x08\n\x04Mage\x10\x04')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'player_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CLASS._serialized_start=196
  _CLASS._serialized_end=249
  _PLAYERSLIST._serialized_start=27
  _PLAYERSLIST._serialized_end=194
  _PLAYERSLIST_PLAYER._serialized_start=88
  _PLAYERSLIST_PLAYER._serialized_end=194
# @@protoc_insertion_point(module_scope)
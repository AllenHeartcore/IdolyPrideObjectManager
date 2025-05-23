# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.
# source: octodb.proto
"""
octodb_pb2.py
[INTERNAL] Generated protocol buffer code for manifest database.
"""


from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.json_format import MessageToDict, ParseDict

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

# single    = \x01...
# repeated  = \x03...
# uint64    =  ...\x28\x04
# int       =  ...\x28\x05
# string    =  ...\x28\x09
# uint32    =  ...\x28\x0d

_serialized_bytes = b"".join(
    [
        b"\x0a\x0coctodb.proto",
        b"\x22\x7d\x0a\x08Database",
        b"\x12\x10\x0a\x08revision\x18\x01 \x01\x28\x05",
        b"\x12\x1e\x0a\x0fassetBundleList\x18\x02 \x03\x28\x0b\x32\x05.Data",
        b"\x12\x0f\x0a\x07tagname\x18\x03 \x03\x28\x09",
        b"\x12\x1b\x0a\x0cresourceList\x18\x04 \x03\x28\x0b\x32\x05.Data",
        b"\x12\x11\x0a\x09urlFormat\x18\x05 \x01\x28\x09",
        b"\x22\xae\x02\x0a\x04Data",
        b"\x12\x0a\x0a\x02id\x18\x01 \x01\x28\x05",
        b"\x12\x10\x0a\x08filepath\x18\x02 \x01\x28\x09",
        b"\x12\x0c\x0a\x04name\x18\x03 \x01\x28\x09",
        b"\x12\x0c\x0a\x04size\x18\x04 \x01\x28\x05",
        b"\x12\x0b\x0a\x03crc\x18\x05 \x01\x28\x0d",
        b"\x12\x10\x0a\x08priority\x18\x06 \x01\x28\x05",
        b"\x12\x0d\x0a\x05tagid\x18\x07 \x03\x28\x05",
        b"\x12\x14\x0a\x0cdependencies\x18\x08 \x03\x28\x05",
        b"\x12\x1a\x0a\x05state\x18\x09 \x01\x28\x0e\x32\x0b.Data.State",
        b"\x12\x0b\x0a\x03md5\x18\x0a \x01\x28\x09",
        b"\x12\x12\x0a\x0aobjectName\x18\x0b \x01\x28\x09",
        b"\x12\x12\x0a\x0ageneration\x18\x0c \x01\x28\x04",
        b"\x12\x17\x0a\x0fuploadVersionId\x18\x0d \x01\x28\x05",
        b"\x22\x3e\x0a\x05State",
        b"\x12\x08\x0a\x04NONE\x10\x00",
        b"\x12\x07\x0a\x03ADD\x10\x01",
        b"\x12\x0a\x0a\x06UPDATE\x10\x02",
        b"\x12\x0a\x0a\x06LATEST\x10\x03",
        b"\x12\x0a\x0a\x06DELETE\x10\x04",
        b"\x62\x06proto3",
    ]
)

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(_serialized_bytes)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "octodb_pb2", globals())

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _DATABASE._serialized_start = 16
    _DATABASE._serialized_end = 141
    _DATA._serialized_start = 144
    _DATA._serialized_end = 446
    _DATA_STATE._serialized_start = 384
    _DATA_STATE._serialized_end = 446

# @@protoc_insertion_point(module_scope)


# Interface between ProtoDB bytestring and JSON
# (Avoid lambda functions for rigorous type checking)


def pdbytes2dict(pdb: bytes) -> dict:
    return MessageToDict(Database().FromString(pdb))


def dict2pdbytes(jdict: dict) -> bytes:
    return ParseDict(jdict, Database()).SerializeToString()

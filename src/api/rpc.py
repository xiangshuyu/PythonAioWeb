import os
import grpc

from src.project.env import base_dir
from src.util.file_util import step_file_dir

grpc_pkg_name = 'src.api.protoc'
grpc_pkg_path = grpc_pkg_name.replace('.', '/')

grpc_suffix = '_grpc'
protobuf_suffix = '_pb2'

grpc_files = []

step_file_dir(os.path.join(base_dir, grpc_pkg_path), resolve=lambda x: x.endswith('.py') and grpc_files.append(x))


def _import_grpc_module(grpc_pkg=grpc_pkg_name):
    simple_names = []
    for file in grpc_files:
        if not isinstance(file, str):
            continue
        if file.__contains__("__init__"):
            continue
        begin_index = file.index(grpc_pkg_path) + grpc_pkg_path.__len__() + 1
        end_index = file.__len__() - 3
        simple_names.append(file[begin_index:end_index])

    grpc_service = dict()
    for name in simple_names:
        if not name.endswith(protobuf_suffix):
            continue

        grpc_file_name = name + grpc_suffix
        if not simple_names.__contains__(grpc_file_name):
            continue
        grpc_key = name[:-protobuf_suffix.__len__()]
        grpc_service[grpc_key] = (name, grpc_file_name)

    return grpc_service, __import__(grpc_pkg, globals(), locals(), simple_names)


class GRPCProperty(object):
    pass


class _GRPCMetaclass(type):
    def __new__(mcs, name, bases, attr):

        grpc_service, grpc_modules = _import_grpc_module(grpc_pkg=grpc_pkg_name)

        def init(self, host='127.0.0.1', port=50051):

            self.__channel = grpc.insecure_channel(f'{host}:{port}')
            self.__grpc_service = grpc_service
            self.__grpc_modules = grpc_modules

            for key, service in self.__grpc_service.items():

                protobuf_module_name, grpc_module_name = service

                protobuf_module = getattr(self.__grpc_modules, protobuf_module_name)
                grpc_module = getattr(self.__grpc_modules, grpc_module_name)

                dto_obj = GRPCProperty()
                for m_attr in dir(protobuf_module):
                    if m_attr.endswith("Request") or m_attr.endswith("Response"):
                        setattr(dto_obj, m_attr, getattr(protobuf_module, m_attr))
                    else:
                        attr_type_name = str(type(getattr(protobuf_module, m_attr)))
                        if attr_type_name.__contains__("google.protobuf"):
                            setattr(dto_obj, m_attr, getattr(protobuf_module, m_attr))

                rpc_obj = GRPCProperty()
                for m_attr in dir(grpc_module):
                    if m_attr.endswith("Stub"):
                        stub_class = getattr(grpc_module, m_attr)
                        # the class of python is a callable obj, so it can just use xxx() to create object
                        setattr(rpc_obj, m_attr, stub_class(self.__channel))

                service_obj = GRPCProperty()
                service_obj.dto = dto_obj
                service_obj.Client = rpc_obj

                if not hasattr(self, key):
                    setattr(self, key, service_obj)

        attr['__init__'] = init

        return type.__new__(mcs, name, bases, attr)


class GRPCService(metaclass=_GRPCMetaclass):

    def __init__(self):
        print("original init")

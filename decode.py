import grpc_tools.protoc

proto_file = 'gtfs-realtime.proto'

# Compile the .proto file
grpc_tools.protoc.main((
    '',
    f'--proto_path=.',
    f'--python_out=.',
    f'--grpc_python_out=.',
    proto_file,
))

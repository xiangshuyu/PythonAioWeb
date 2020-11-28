from src.api.rpc import GRPCService

grpc_service = GRPCService(host='127.0.0.1', port=50051)
grpc_index = grpc_service.Index
grpc_common = grpc_service.Common

message = grpc_common.dto.HeaderMessage(appId="2")

request = grpc_index.dto.IndexRequest(header=message)

print(grpc_index.Client.IndexServiceStub.index(request))



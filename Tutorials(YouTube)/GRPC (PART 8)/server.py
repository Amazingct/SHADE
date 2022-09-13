# python -m  grpc_tools.protoc -I protos\ --python_out=. --grpc_python_out=. protos\Math.proto
from concurrent import futures
import time
import grpc
import Math_pb2
import Math_pb2_grpc
import socket   


class MathServicer(Math_pb2_grpc.MathServicer):
    #UNARY
    def add(self, request, context):
        solution = request.a + request.b
        reply = Math_pb2.responseadd(sum=solution)
        return reply

    #SERVER STREAMING
    def count(self, request, context):
        print("streaming started")
        start = request.a
        stop = request.b
        for i in range(start,stop):
            yield Math_pb2.responseadd(sum = i)
            time.sleep(2)


    #CLIENT STREAM
    def recite(self, request_iterator, context):
        all_numbers = []
        for request in request_iterator:
            if request.command == "quit":
                break
            else:
                all_numbers.append(int(request.command))
        response = sum(all_numbers)
        return Math_pb2.response(response=str(response))



    #SERVER AND CLIENT STREAMING  
    def chat(self, request_iterator, context):
        print("chat started")
        while True:
            for request in request_iterator:
                response = "you said '{}' ".format(request.command)
                yield Math_pb2.response(response=response)


def serve():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    print("Your Computer Name is:"+hostname)   
    print("Your Computer IP Address is:"+IPAddr) 

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Math_pb2_grpc.add_MathServicer_to_server(MathServicer(), server)
    server.add_insecure_port(IPAddr+":50054")
    server.start()
    print("SERVICE STARTED")
    server.wait_for_termination()


    
if __name__ == "__main__":
    serve()

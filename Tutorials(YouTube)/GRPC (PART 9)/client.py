import grpc
import Math_pb2
import Math_pb2_grpc
  

channel = grpc.insecure_channel("192.168.56.1:50054")
Math = Math_pb2_grpc.MathStub(channel)

## TEST UNARY
command = Math_pb2.commandadd(a =5, b =10)
rx = Math.add(command)
print(rx)

## TEST SERVER STREAMING
# response = Math.count(Math_pb2.commandadd(a=0, b=10))
# for number in response:
#     print(number.sum)


## TEST CLIENT STREAMING
# def get_numbers():
#     while True:
#         number = input("number: >> ")
#         yield Math_pb2.command(command=number)
#         if number == "quit":
#             break

# response = Math.recite(get_numbers())
# print(response)


## TEST SERVER AND CLIENT STREAMING(CHAT)
# def chat():
#     while True:
#         message = input("message: >> ")
#         yield Math_pb2.command(command=message)

# response = Math.chat(chat())
# for message in response:
#     print(message.response)



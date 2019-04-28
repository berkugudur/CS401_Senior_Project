import random
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1428        # Port to listen on (non-privileged ports are > 1023)

def predictStrongestBot(usX, usY, opponentX, opponentY):
    print("Predicting strongest bot with parameters usX: {}, usY: {}, opponentX: {}, opponentY: {}".format(usX, usY, opponentX, opponentY))
    strongest_bot_name = ["Thunder", "BCP"][random.randint(0, 1)] 

    return strongest_bot_name
 

class JavaTunnel:

    def __init__(self, socket):
        self.functions = {
            "predictStrongestBot": predictStrongestBot
            }
        self.socket = socket
        

    def startReceiving(self):
        func_name = ""
        argument_size = 0
        arguments = []

        while(True):
            data = self.socket.recv(1024)

            lines = data.decode().split("\n")
            for line in lines:
                if line:
                    line_body = line.split("_")

                    if line_body[0] == "func":
                        argument_size = int(line_body[-1])
                        func_name = line_body[1]
                        argument_count = 0
                    
                    else: 
                        arguments.append(line)
                        if len(arguments) == argument_size:
                            print("Calling function {} with arguments {}".format(func_name, str(arguments)))

                            returnValue = self.functions[func_name](*arguments) + "\n"
                            
                            print("Return value is {}".format(returnValue))
                            
                            self.socket.sendall(returnValue.encode())
                            print("Return value sended.")

                            arguments = []
                            

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
 
tunnel = JavaTunnel(sock)
tunnel.startReceiving()





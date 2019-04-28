import socket
from JavaTunnel import JavaTunnel
from BotPredictor import BotPredictor
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1455        # Port to listen on (non-privileged ports are > 1023)

class MessageParser:

    def __init__(self, socket, tunnel):
        self.socket = socket
        self.tunnel = tunnel
        

    def startParsing(self):
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
                    
                    else: 
                        arguments.append(line)
                        if len(arguments) == argument_size:
                            print("Calling function {} with arguments {}".format(func_name, str(arguments)))

                            function = getattr(self.tunnel, func_name)
                            returnValue = function(*arguments) + "\n"
                            
                            print("Return value is {}".format(returnValue))
                            
                            self.socket.sendall(returnValue.encode())
                            print("Return value sended.")

                            arguments = []
                        
                            
if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    predictors = [
            BotPredictor("../AIConnection/example_data/bcpvsthunder/hpmodel/", "../AIConnection/example_data/bcpvsthunder/actionmodel/"),
            BotPredictor("../AIConnection/example_data/bcpvsutal/hpmodel/", "../AIConnection/example_data/bcpvsutal/actionmodel/"),
            BotPredictor("../AIConnection/example_data/bcpvssimpleai/hpmodel/", "../AIConnection/example_data/bcpvssimpleai/actionmodel/")
        ]
    predictor_names = ["Thunder","UtalFighter", "SimpleAI"]
    parser = MessageParser(sock, JavaTunnel(predictors, predictor_names))
    parser.startParsing()





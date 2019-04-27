from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
import random

class PythonDelegate(object):

    def predictStrongestBot(usX, usY, opponentX, opponentY):
        print("Predicting strongest bot with parameters usX: {}, usY: {}, opponentX: {}, opponentY: {}", usX, usY, opponentX, opponentY)
        strongest_bot_name = ["Thunder", "BCP"][random()] # 0 or 1

        return strongest_bot_name

    class Java:
        implements = ["BotCenter.PythonDelegate"]

if __name__ == "__main__":
    delegate = PythonDelegate()
    gateway = ClientServer(java_parameters=JavaParameters(), python_parameters=PythonParameters(), python_server_entry_point=delegate)
    print("Server created")

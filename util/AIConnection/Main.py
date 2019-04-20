import sys
from time import sleep
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
from PredictAI import PredictAI
from PredictHPAI import PredictHPAI

players = []
ai_list = []
def print_ai_list():
    print("Registered AI list")
    for i in range(len(ai_list)):
        print(str(i) + " | " + ai_list[i])

def get_player_input():
    print("Please enter AI Name correctly")
    players.append(input("P0 name: "))
    players.append(input("P1 name: "))            
    print("Player 0 is " + players[0])
    print("Player 1 is " + players[1])

def add_ai(ai_name, object):
    if object != None:
        manager.registerAI(ai_name, object)
    ai_list.append(ai_name)

def create_game():
    print("Creating game")
    game = manager.createGame("ZEN", "ZEN", players[0], players[1], 1)
    manager.runGame(game)

def run_game():
    print("Running game")

def close_gateway():
	gateway.close_callback_server()
	gateway.close()

# Creating gateway and entrypoint
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=4242), callback_server_parameters=CallbackServerParameters());
manager = gateway.entry_point

# Add your AI here, don't forget import. If it is Java AI second parameter must be None
#add_ai("PredictAI", PredictAI(gateway))
add_ai("PredictHPAI", PredictHPAI(gateway))
add_ai("Thunder", None)
add_ai("UtalFighter", None)
add_ai("BCP", None)
add_ai("ai", None)

# User Input
print_ai_list()    
get_player_input()

# Game Loop
create_game()
run_game()
close_gateway()
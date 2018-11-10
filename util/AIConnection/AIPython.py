from py4j.java_gateway import JavaGateway
import time

from predictor import Predictor

predictor = Predictor("../../notebooks/learn_from_thunder_bot/out")

input("Start ?")

# First start java game with AI that has server
gateway = JavaGateway()
while True:
    us = gateway.getFrameData().getCharacter(True)
    opponent = gateway.getFrameData().getCharacter(False)

    action = opponent.getAction().toString()
    opponent_hp = opponent.getHp()
    opponent_x = opponent.getX()
    opponent_y = opponent.getY()

    us_hp = us.getHp()
    us_x = us.getX()
    us_y = us.getY()
    
    predicted_action = predictor.predict(action, opponent_hp, opponent_x, opponent_y, us_hp, us_x, us_y)
    gateway.setAction(predicted_action)

    print(predicted_action)
    print(action)
    time.sleep(0.001)

from py4j.java_gateway import JavaGateway
import time

# First start java game with AI that has server
gateway = JavaGateway()

while True:
    data = gateway.getFrameData().getCharacter(False).getHp()
    if data > -100:
        gateway.setAction("STAND_B")
    elif data > -200:
        gateway.setAction("CROUCH_A")
    elif data > -300:
        gateway.setAction("CROUCH_B")
    print("HP:" + str(data))
    time.sleep(0.001)

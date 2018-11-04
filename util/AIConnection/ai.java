import aiinterface.AIInterface;

import java.util.Objects;
import aiinterface.CommandCenter;
import struct.FrameData;
import struct.GameData;
import struct.Key;
import py4j.*;

public class ai implements AIInterface {
    private Key key;
    private boolean playerNumber;
    private FrameData currentFrame;
    private GatewayServer server;
    private String action = "";
    private CommandCenter cc;

    @Override
    public int initialize(GameData gameData, boolean b) {
        this.playerNumber = b;
        init();
        startServer();
        return 0;
    }

    private void init() {
        this.key = new Key();
        cc = new CommandCenter();
        currentFrame = new FrameData();
    }

    private void startServer() {
        server = new GatewayServer(this);
        server.start();
    }

    @Override
    public void getInformation(FrameData frameData) {
        this.currentFrame = frameData;
        cc.setFrameData(this.currentFrame, playerNumber);
    }


    @Override
    public void processing() {
        if (!currentFrame.getEmptyFlag() &&
                currentFrame.getRemainingFramesNumber() > 0) {
            if (cc.getSkillFlag()) {
                key = cc.getSkillKey();
            } else {
                key.empty();
                cc.skillCancel();
                if (!Objects.equals(action, "")) {
                    cc.commandCall(action);
                    System.out.println("Action: " + action);
                }
            }
        }
    }

    @Override
    public Key input() {
        return key;
    }

    @Override
    public void close() {
        server.shutdown();
    }

    @Override
    public void roundEnd(int i, int i1, int i2) {
        server.shutdown();
    }

    //These two function using by python side
    public FrameData getFrameData() {
        return currentFrame;
    }

    public void setAction(String action) {
        if (!cc.getSkillFlag())
            this.action = action;
    }
}
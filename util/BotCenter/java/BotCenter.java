import aiinterface.AIInterface;
import aiinterface.CommandCenter;
import java.io.IOException;
import java.util.List;
import py4j.ClientServer;
import struct.CharacterData;
import struct.FrameData;
import struct.GameData;
import struct.Key;

/*
 * Used for run multiple agents in the same game environment.
 *
 * It loads all jar files in given folder as AIInterface instances and propagate
 * BotCenter's AIInterface method calls to them.
 *
 * @variable REAL_PLAYER is holding the real player's class name. Real player is the agent whose
 * actions applied the real game environment.
 *
 * Meric Oztiryaki 2019
 */
public class BotCenter implements AIInterface {

    private static final int PORT = 1455;

    private PythonTunnel pythonTunnel;

    private List<String> botNames;
    private List<AIInterface> ais;

    private Key inputKey;
    private FrameData frameData;
    private CommandCenter commandCenter;
    private boolean player;

    public BotCenter() {
        ResourceLoader<AIInterface> resourceLoader = new ResourceLoader<>("./data/ai/");

        botNames = ResourceLoader.loadFileNames("./data/ai/", ".jar");

        // Remove this class(BotCenter) from bot name list to prevent recursive generation of BotCenter.
        botNames.removeIf(s -> s.equals(this.getClass().getCanonicalName()));

        ais = resourceLoader.loadAllJars(botNames);

        // Logging
        System.out.println("BotCenter loaded " + ais.size() + " ais.");
        printBots();

        // Create python tunnel
        try {
            pythonTunnel = TunnelFactory.open(PORT);
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("CAN NOT CONNECT TO PYTHON");
        }
        System.out.println("Python tunnel established");
    }

    public void printBots() {
        for(String botName: botNames) {
            System.out.println("\t" + botName);
        }
    }

    @Override
    public int initialize(GameData gameData, boolean player) {
        this.player = player;
        this.inputKey = new Key();
        this.commandCenter = new CommandCenter();

        // Initialize all ais.
        for(AIInterface ai: ais) {
            ai.initialize(gameData, player);
        }

        return 0;
    }

    @Override
    public void getInformation(FrameData frameData) {
        this.frameData = frameData;

        // Pass information to all ais.
        for(AIInterface ai: ais) {
            ai.getInformation(frameData);
        }
    }

    @Override
    public void processing() {
        for(AIInterface ai: ais) {
            ai.processing();
        }
    }

    @Override
    public Key input() {
        if (this.frameData.getEmptyFlag() || this.frameData.getRemainingFramesNumber() <= 0) {
            return this.inputKey;
        } else if(this.commandCenter.getSkillFlag()) {
            return this.commandCenter.getSkillKey();
        } else {
            this.inputKey.empty();
            this.commandCenter.skillCancel();
        }

        this.commandCenter.setFrameData(this.frameData, this.player);

        CharacterData us = this.frameData.getCharacter(this.player);
        CharacterData opponent = this.frameData.getCharacter(!this.player);

        String strongestBotName = pythonTunnel.predictStrongestBot(opponent.getAction().toString(), us.getCenterX(), us.getCenterY(), opponent.getCenterX(), opponent.getCenterY());
        System.out.println("Python predicted '" + strongestBotName +"' as the strongest bot.");

        AIInterface strongestBot = ais.get(botNames.indexOf(strongestBotName));

        return strongestBot.input();
    }

    @Override
    public void close() {
        for(AIInterface ai: ais) {
            ai.close();
        }
    }

    @Override
    public void roundEnd(int i, int i1, int i2) {
        for(AIInterface ai: ais) {
            ai.roundEnd(i, i1, i2);
        }
    }

    public interface PythonDelegate {

        /*
         * Predicts the strongest bot and return its name.
         */
        String predictStrongestBot(int usX, int usY, int opponentX, int opponentY);

    }
}


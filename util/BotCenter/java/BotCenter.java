import aiinterface.AIInterface;
import aiinterface.CommandCenter;
import java.util.List;
import py4j.GatewayServer;
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
public class BotCenter {

    List<String> botNames;
    List<AIInterface> ais;

    public BotCenter() {
        ResourceLoader<AIInterface> resourceLoader = new ResourceLoader<>("./data/ai/");

        botNames = ResourceLoader.loadFileNames("./data/ai/", ".jar");

        // Remove this class(BotCenter) from bot name list to prevent recursive generation of BotCenter.
        botNames.removeIf(s -> s.equals(this.getClass().getCanonicalName()));

        ais = resourceLoader.loadAllJars(botNames);

        // Logging
        System.out.println("BotCenter loaded " + ais.size() + " ais.");
        printBots();
    }

    public int id(String botName) {
        return botNames.indexOf(botName);
    }

    public void printBots() {
        for(String botName: botNames) {
            System.out.println("\t" + botName);
        }
    }

    public int[] initialize(GameData gameData, boolean b) {
        int[] results = new int[ais.size()];

        for(int i=0; i<ais.size(); i++) {
            results[i] = ais.get(i).initialize(gameData, b);
        }

        return results;
    }

    public void getInformation(FrameData frameData) {
        for(AIInterface ai: ais) {
            ai.getInformation(frameData);
        }
    }

    public void processing() {
        for(AIInterface ai: ais) {
            ai.processing();
        }
    }

    public Key[] input() {
        Key[] results = new Key[ais.size()];
        for(int i=0; i<ais.size(); i++) {
            results[i] = ais.get(i).input();
        }
        return results;
    }

    public void close() {
        for(AIInterface ai: ais) {
            ai.close();
        }
    }

    public void roundEnd(int i, int i1, int i2) {
        for(AIInterface ai: ais) {
            ai.roundEnd(i, i1, i2);
        }
    }
}

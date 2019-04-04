import py4j.GatewayServer;

public class Main {

    private static final int PORT = 1428;

    public static void main(String[] args) {
        BotCenter botCenter = new BotCenter();
        GatewayServer gatewayServer = new GatewayServer(botCenter, PORT);
        gatewayServer.start();

        // Logging
        System.out.println("BotCenter's gateway server created on port: " + PORT);
        System.out.println("------------------------------------------------");
    }

}

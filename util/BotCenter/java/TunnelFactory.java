import java.io.IOException;
import java.net.ServerSocket;
import network.Connection;

public class TunnelFactory {

    public static PythonTunnel open(int port) throws IOException {
        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("Server started listening.");

        Connection connection = new Connection(serverSocket.accept());
        System.out.println("Server accepted new connection.");

        return new PythonTunnel(connection);
    }

}

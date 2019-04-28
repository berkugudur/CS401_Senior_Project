package network;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Server implements Runnable {

    private int port;
    private ServerSocket serverSocket;

    protected ServerDelegate delegate;

    public Server(int port) throws IOException {
        this.port = port;
        this.serverSocket = new ServerSocket(port);
        this.delegate = new NullServerDelegate();
    }

    @Override
    public void run() {

        try {
            Socket s = serverSocket.accept();
            delegate.onNewConnection(new Connection(s));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void setDelegate(ServerDelegate delegate) {
        this.delegate = delegate;
    }
}


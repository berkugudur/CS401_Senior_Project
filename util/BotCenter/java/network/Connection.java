package network;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

/*
 * Wrapper for making java.net.socket object non-blocking.
 */
public class Connection extends Thread {

    private Socket socket;
    private PrintWriter outputStream;
    private BufferedReader inputStream;

    private List<ConnectionDelegate> delegateList;

    private AtomicBoolean running;

    public Connection(Socket socket) throws IOException {
        this.socket = socket;
        this.inputStream = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        this.outputStream = new PrintWriter(socket.getOutputStream(), true);
        this.delegateList = new ArrayList();
        this.running = new AtomicBoolean(false);
    }

    public Connection(String host, int port) throws IOException {
        this(new Socket(host, port));
    }

    @Override
    public void run() {
        running.set(true);
        try {

            while(running.get() && socket.isConnected()) {
                Object message = inputStream.readLine();
                delegateList.forEach(d -> d.onMessage(message));
            }

        } catch (IOException e) {
            delegateList.forEach(ConnectionDelegate::onConnectionLost);
            running.set(false);
        } finally {
            this.close();
        }
    }

    public boolean sendObject(Object object) {
        this.outputStream.println(object);
        return true;
    }

    public void close() {
        try {
            this.socket.close();
            this.inputStream.close();
            this.outputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void addDelegate(ConnectionDelegate delegate) {
        this.delegateList.add(delegate);
    }

    public PrintWriter getOutputStream() {
        return outputStream;
    }

    public BufferedReader getInputStream() {
        return inputStream;
    }
}

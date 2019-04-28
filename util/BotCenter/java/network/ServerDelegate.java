package network;

public interface ServerDelegate {

    void onNewConnection(Connection connection);

}

class NullServerDelegate implements ServerDelegate {

    @Override
    public void onNewConnection(Connection connection) {

    }

}
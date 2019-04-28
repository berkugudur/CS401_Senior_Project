package network;


public interface ConnectionDelegate {

    void onMessage(Object message);

    void onConnectionLost();
}

class NullConnectionDelegate implements ConnectionDelegate {

    @Override
    public void onMessage(Object message) {

    }

    @Override
    public void onConnectionLost() {

    }

}
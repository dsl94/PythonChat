import sys
from select import select
from socket import socket, AF_INET, SOCK_STREAM


class Server():
    # Konstruktor
    def __init__(self):
        # ako su proslednjeni argumenti oni postaju host i port
        if len(sys.argv) == 3:
            host = sys.argv[1]
            port = int(sys.argv[2])
        # ako nisu onda ide default host i port
        else:
            host = 'localhost'
            port = 50007

        self.toFile = False
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(3)
        self.startServer(sock, host, port)

    def startServer(self, sock, host, port):
        print ("Pokrenut server: {0}:{1}".format(host, port))
        mainsocks = []
        readsocks = []
        clients = []

        mainsocks.append(sock)
        readsocks.append(sock)

        while True:
            readables, writeables, exceptions = select(readsocks, [], [])
            for sockobj in readables:
                if sockobj in mainsocks:
                    newsock, address = sockobj.accept()
                    print ('Konektovan:', address, id(newsock))
                    readsocks.append(newsock)
                    clients.append(newsock)
                else:
                    try:
                        data = sockobj.recv(1024)
                    except ConnectionResetError:
                        print ((address), " je izgubio konekciju")
                        data = None
                    if not data:
                        sockobj.close()
                        readsocks.remove(sockobj)
                        clients.remove(sockobj)
                    else:
                        for s in clients:
                            s.send(data)

if __name__ == "__main__": Server()


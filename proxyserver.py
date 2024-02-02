import urllib.request
from functools import lru_cache
from socket import *
import select


class Proxy:

    @lru_cache(maxsize=128, typed=False)
    def connect_to(self, address, port, url, connectionSocket):
        remote = socket(AF_INET, SOCK_STREAM)
        remote.connect((address, port))
        print(f'connected to {address}:{port}')
        #this seems to connect properly
        try:
            s = url.read()
            print(s)
            connectionSocket.sendall(s)
            connectionSocket.close()

        except Exception as ex:
            print(ex)

    def run(self, host, port):
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print(f'listening to {host}:{port}')

        while True:
            connectionSocket, addr = server.accept()
            request = connectionSocket.recv(4096).decode()
            req = request.split()[1]
            site = req.replace('/', '')
            website = 'http://' + site
            print('website: ' + website)
            print('request: ' + request)
            response = b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            connectionSocket.send(response)

            #try:
            with urllib.request.urlopen(website) as url:
                #s = url.read()
                #print(s)
            #except Exception as e:
                #print(e)

                self.connect_to(site, 80, url, connectionSocket)

            #if connected == False:
                #self.connect_to(site, 80, website)
                #connected = True



if __name__ == '__main__':
    try:
        proxy = Proxy()
        proxy.run('localhost', 8080)
    except Exception as e:
        print(e)

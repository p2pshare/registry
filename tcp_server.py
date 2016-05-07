import socket
import sys
from time import sleep
import sqlite3
import hashlib
import json
import registry

# Create a TCP/IP socket (socket.SOCK_DREAM = UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind() is used to associate the socket with the server address.
server_address = ('localhost', 8000)
sock.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % server_address

# listen() puts the socket into server mode and then accept() waits for an incoming connection
sock.listen(5)
while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # accept() returns an open connection between the server and the client, along with the address of the client.
        # 'connnection' is actually a different socket on another port which is assigned by the kernel.
        # Data is read from the connection with recv() and transmitted with sendall()
        # Receive the data in small chunks and retransmit it
        filename = ""
        file_descriptor = None
        while True:
            data = connection.recv(4096)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                try:
                    i = int(data)
                    ret = registry.search(str(i), "id")
                    j = {}
                    j["id"] = ret[0][0]
                    j["filename"] = ret[0][1]
                    j["hash"] = ret[0][2]
                    j["author"] = ret[0][3]
                    j["chunks"] = ret[0][4]
                    ret = registry.search(str(i), "id_trackers")
                    j["trackers"] = ret
                    r = json.dumps(j)
                    connection.sendall(r)
                except ValueError, e:
                    j = json.loads(data)
                    filename = j['filename'] # single string
                    author = j['author'] # single string
                    trackers = j['trackers'] # list expected
                    # print filename
                    # print author
                    # print trackers
                    file_id = registry.add(filename, author, trackers)
                    if file_id is not None:
                        connection.sendall(str(file_id))
                    else:
                        connection.sendall("BAD REQUEST")

                # str_arr = data.strip().split(" ")
                # if str_arr[0].strip().upper() == "ADDSHARE":
                #     filename = str_arr[1].strip()
                #     author = str_arr[2].strip()
                #     trackers = str_arr[3].strip()
                #     tracker_list = trackers.split("||")
                #     # def add(filename, author, *trackers):
                #     if registry.add(filename, author, tracker_list) == True:
                #         connection.sendall("OK")
                #     else:
                #         connection.sendall("BAD")
                #
                # elif str_arr[0].strip().upper() == "GETSHARE":
                #     # def search(search_key, search_type):
                #     search_key = str_arr[1].strip()
                #     search_type = str_arr[2].strip()
                #     ret = registry.search(search_key, search_type)
                #     print ret
                #     for each in ret:
                #         for i in range(0, len(each)):
                #             print each[i]
                #
                #         connection.sendall(ret1)
                #     connection.sendall("BAD")
                # else:
                #     print >>sys.stderr, str_arr[0].strip().upper(), ' is an invalid Request. Only ADDSHARE or GETSHARE.'
                #     connection.sendall("BAD")
                #     connection.close()
            else:
                print >>sys.stderr, 'Connection from ', client_address, ' Closed.'
                break
    finally:
        # Clean up the connection
        connection.close()

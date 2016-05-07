import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8000)
print >>sys.stderr, ' connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    while True:
        message = raw_input("json or id\n")
        print >>sys.stderr, ' sending "%s"' % message
        sock.sendall(message)
        print "Sent: ",message

        data = sock.recv(4096)
        print >>sys.stderr, 'received "%s"' % data


finally:
    print >>sys.stderr, ' Socket Closing.'
    sock.close()

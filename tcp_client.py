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
        # Send data
        # message = raw_input("What do you wanna do? 'sendfile <filename>'? ")
        message = "sendfile P1010822.JPG"
        operation = message.split(" ")
        _ = raw_input("wait? ")
        if operation[0].strip().upper() == "SENDFILE":
            message = message.upper()
            sock.sendall(message)
            print "Filename sent ", message
            file_descriptor = open(operation[1], "rb")
            print "File Opened ",operation[1]
            while True:
                chunk = file_descriptor.read(4096)
                if chunk:
                    sock.send(chunk)
                    print('Sent ', repr(chunk))
                else:
                    sock.close()
                    break
        else:
            print >>sys.stderr, ' sending "%s"' % message
            sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data = sock.recv(4096)
                amount_received += len(data)
                print >>sys.stderr, 'received "%s"' % data
finally:
    print >>sys.stderr, ' Socket Closing.'
    sock.close()

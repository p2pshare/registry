# Registry

###### Method Name: Add
- Arguments:
  - filename (string)
  - author (string)
  - trackers (Pointer to array list)
- Implementation
  - Check if the database 'FILES' and 'FILES_TRACKERS' exist
  - Connect to the database called 'share.db'
  - Hash filename and author by MD5 and convert it into hexadecimal
  - Save them into 'filename','hash', 'author', 'chunk_info'
  - Save its trackers information by file id

###### Method Name: Search
- Arguments:
  - Search_key (string)
  - Search_type (string)
    - filename or hash or author
- Implementation
  - Check if the database 'FILES' and 'FILES_TRACKERS' exist
  - Connect to the database called 'share.db'
  - Search and return results by Search_type in the table of 'FILES'

- p2pshare file format (filename.share)

```json
{
    "id": 12,
    "filename": "filename.mp4",
    "hash": "{}md5hash}",
    "author": "{{ username }}",
    "chunks": [{
        "id": 1,
        "hash": "{{hash}}"
    },
    {
        "id": 2,
        "hash": "{{hash}}"
    },
    {
        "id": 3,
        "hash": "{{hash}}"
    },
    {
        "id": 4,
        "hash": "{{hash}}"
    }],
    "trackers": [
        "t1.p2pshare.net",
        "t2.p2pshare.net",
        "t3.p2pshare.net",
        "t4.p2pshare.net"
    ]
}
```

# TCP Server
###### Usage: python tcp_server.py
- Implementation
  - Make TCP Socket by Socket.AF_INET, Socket.SOCK_STREAM
  - Bind the socket to the localhost and default port#8000
  - Listen to the port which has been connecting to the socket
  - Once a client connects to the port, the socket accepts the connection
  - COMMAND: 'Sendfile <filename>'
    - Once the file transfer is over, client will terminate the connection

# TCP Client
###### Usage: python tcp_server.py
- Implementation
  - Make TCP Socket by Socket.AF_INET, Socket.SOCK_STREAM
  - Connect the socket to a particular localhost and port
  - Command 'sendfile <filename>' to initialize a file transfer session
    - Once the file transfer is over, client will terminate the connection

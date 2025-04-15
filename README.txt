Peter Nguyen  
V00957051  

---

 Basic Chat Application – CMSC 440 Programming Assignment  

This project implements a TCP-based chat server and client in Python.  
Clients can connect to a server, send/receive messages with nicknames, and disconnect gracefully.  

---

 How to Run:

1. Start the Chat Server:
   $ python3 ChatServer.py <port>

   Example:
   $ python3 ChatServer.py 12345

2. Start a Chat Client in a separate terminal:
   $ python3 ChatClient.py <hostname/ip> <port> <nickname> <ClientID>

   Example:
   $ python3 ChatClient.py localhost 12345 Alice 001

---

 Requirements:

- Python 3
- No external libraries used (only `socket`, `threading`, `json`, `datetime`, `sys`)
- Must be run on VM Linux or GitHub Codespaces with open ports (10000–11000)

---

 Files Included:

- ChatServer.py – handles multiple clients, nickname management, and message broadcasting
- ChatClient.py – connects to the server and sends/receives formatted messages
- README.txt – this file

---

 Notes:

- Type `disconnect` in the client to end your session and show a chat summary.
- Format strictly follows the assignment spec for output.

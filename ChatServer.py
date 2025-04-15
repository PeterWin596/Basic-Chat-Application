# ChatServer.py
import socket
import threading
import json
import sys
from datetime import datetime

clients = {}
nicknames = {}

def broadcast(sender_nickname, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = json.dumps({
        "type": "broadcast",
        "nickname": sender_nickname,
        "message": message,
        "timestamp": timestamp
    })
    targets = []
    for nickname, conn in nicknames.items():
        if nickname != sender_nickname:
            try:
                conn.sendall(data.encode())
                targets.append(nickname)
            except:
                pass
    print(f"Broadcasted: {', '.join(targets)}")

def handle_client(conn, addr):
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            data = json.loads(msg)

            if data["type"] == "nickname":
                nickname = data["nickname"]
                if nickname in nicknames:
                    conn.send(json.dumps({
                        "type": "error",
                        "message": "Nickname is already in use. Please choose a different one."
                    }).encode())
                    continue

                nicknames[nickname] = conn
                clients[conn] = (addr, data["clientID"], nickname)
                print(f"{data['timestamp']} :: {nickname}: connected.")

            elif data["type"] == "message":
                ip, port = conn.getpeername()
                clientID = clients[conn][1]
                print(f"Received: IP:{ip}, Port:{port}, Client-Nickname:{data['nickname']}, ClientID:{clientID}, Date/Time:{data['timestamp']}, Msg-Size:{len(data['message'])}")
                broadcast(data['nickname'], data['message'])

            elif data["type"] == "disconnect":
                nickname = data["nickname"]
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} :: {nickname}: disconnected.")
                del nicknames[nickname]
                del clients[conn]
                conn.close()
                break
    except:
        conn.close()

def main():
    if len(sys.argv) != 2:
        print("ERR - arg 1")
        return

    try:
        port = int(sys.argv[1])
        if not (0 < port < 65536):
            raise ValueError
    except:
        print("ERR - arg 1")
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('', port))
        server.listen()
        server_ip = socket.gethostbyname(socket.gethostname())
        print(f"ChatServer started with server IP: {server_ip}, port: {port} ...")
    except:
        print(f"ERR - cannot create ChatServer socket using port number {port}")
        return

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()

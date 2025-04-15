# ChatClient.py
import socket
import sys
import threading
import json
from datetime import datetime

msg_sent = 0
msg_rcv = 0
char_sent = 0
char_rcv = 0
start_time = None

def receive(sock):
    global msg_rcv, char_rcv
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            msg = json.loads(data)

            if msg["type"] == "error":
                print(msg["message"])
                sock.close()
                return

            if msg["type"] == "broadcast":
                print(f"{msg['timestamp']} :: {msg['nickname']}: {msg['message']}")
                msg_rcv += 1
                char_rcv += len(msg["message"])
        except:
            break

def main():
    global msg_sent, char_sent, start_time

    if len(sys.argv) != 5:
        print("ERR - arg", len(sys.argv))
        return

    hostname, port, nickname, clientID = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    try:
        port = int(port)
        ip = socket.gethostbyname(hostname)
    except:
        print("ERR - arg 1")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except:
        print("ERR - cannot connect to server.")
        return

    start_time = datetime.now()
    print(f"ChatClient started with server IP: {ip}, port: {port}, nickname: {nickname}, client ID: {clientID}, Date/Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    join_msg = json.dumps({
        "type": "nickname",
        "nickname": nickname,
        "clientID": clientID,
        "timestamp": start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
    sock.send(join_msg.encode())

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        user_input = input()
        if user_input.strip().lower() == "disconnect":
            sock.send(json.dumps({
                "type": "disconnect",
                "nickname": nickname,
                "clientID": clientID
            }).encode())
            break

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = {
            "type": "message",
            "nickname": nickname,
            "message": user_input,
            "timestamp": timestamp
        }
        sock.send(json.dumps(message).encode())
        msg_sent += 1
        char_sent += len(user_input)

    end_time = datetime.now()
    print(f"Summary: start:{start_time.strftime('%Y-%m-%d %H:%M:%S')}, end:{end_time.strftime('%Y-%m-%d %H:%M:%S')}, msg sent:{msg_sent}, msg rcv:{msg_rcv}, char sent:{char_sent}, char rcv:{char_rcv}")
    sock.close()

if __name__ == "__main__":
    main()

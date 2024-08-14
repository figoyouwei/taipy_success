'''
@author: Youwei Zheng
@target: sender
@update: 2024.08.14
'''

import time
import socket
from random import randint

HOST = "127.0.0.1"
PORT = 5050

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            random_number = randint(1, 100)
            s.sendall(str(random_number).encode())
            print(f"Sending: {random_number}")
            
            # Optional: Receive server response
            # response = s.recv(1024)
            # print(f"Received: {response.decode()}")

            time.sleep(5)

            # Optional: condition to break the loop
            # if some_condition:
            #     break

except ConnectionError as e:
    print(f"Failed to connect to {HOST}:{PORT} - {e}")

except KeyboardInterrupt:
    print("Program interrupted by the user.")

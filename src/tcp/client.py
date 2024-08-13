import socket
import sys

addr = sys.argv[1]
port = int(sys.argv[2])
msg = sys.argv[3]

print(f'{addr=}')
print(f'{port=}')
print(f'{msg=}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((addr, port))
    s.sendall(msg.encode())

print('The message has been sent.')
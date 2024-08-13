import socket
import sys

addr = sys.argv[1]
port = int(sys.argv[2])

print(f'{addr=}')
print(f'{port=}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            print(f'Received from {addr}: {data.decode()}')

#!/usr/local/bin/python
import socket
import threading

import time
import main


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 31337))
s.listen(10)


C_MAX_TIME = 0.2
CHALLENGES = 100

FLAG = 'ractf{F45t35tCryp70gr4ph3rAr0und}'


def client_thread(conn, addr, timeout=20):
    conn.setblocking(0)
    start = time.time()

    conn.send(b'''[*] Welcome to my little RSA game.
[*] You will be presented with a number of questions.
[*] You have at most 200ms to solve any given question.
[*] That should be plenty for any human good at crypography.
[*] Good luck.
[*]
''')

    chal = None
    num = 0
    waiting = []
    recvd = {}
    buffer = b''
    c_start = 0

    while num < CHALLENGES:
        if chal is None:
            chal = main.gen_challenge()
            c_start = time.time()

            conn.send(f'[c] Challenge {num + 1}:\n'.encode())
            for i in chal[0]:
                conn.send(f'[:] {i}: {chal[0][i]}\n'.encode())

            waiting = list(chal[1].items())

            i = waiting[0]
            conn.send(f'[?] {i[0]}: '.encode())

        try:
            buffer += conn.recv(4096)
        except BlockingIOError:
            if time.time() - start > timeout:
                conn.close()
                return

        if b'\n' not in buffer:
            continue
        buffer = buffer.split(b'\n', 1)
        if len(buffer) == 1:
            line, buffer = buffer[0], b''
        else:
            line, buffer = buffer

        i = waiting.pop()
        recvd[i[0]] = line.strip()

        if not waiting:
            for i in chal[1]:
                if recvd.get(i, b'') != str(chal[1][i]).encode():
                    conn.send(f'[!] INCORRECT ANSWER!\n\n'.encode())
                    conn.close()
                    return

            if time.time() - c_start > C_MAX_TIME:
                conn.send(f'[!] A good cryptologist should be faster than that!\n\n'.encode())
                conn.close()
                return
            conn.send(f'[!] Correct answer\n\n'.encode())
            chal = None
            num += 1

    conn.send(f'[F] FLAG: {FLAG}\n\n'.encode())
    conn.close()


print('Server ready on :31337')
while True:
    conn, addr = s.accept()
    print(addr)
    threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()

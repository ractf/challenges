#!/usr/local/bin/python
# definitely not inspired by clamclamclam
import socket

replacements = {"0": "\r", "1": "\n"}
BINARY_ENCD_FLAG = "0111001001100001011000110111010001100110011110110111000000110011001101000111001000110001010111110011000101101110011100110011000101100100001100110101111100110100010111110110001101101100001101000110110101111101"

endings = [replacements[i] for i in BINARY_ENCD_FLAG]
send = ""
for e in endings:
    send += "ctf{pearlpearlpearl}" + e

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind(('0.0.0.0', 5000))
	while True:
		s.listen()
		conn, addr = s.accept()
		with conn:
			conn.send(bytes(send, "utf-8"))
			conn.close()

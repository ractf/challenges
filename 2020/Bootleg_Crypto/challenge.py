import random

def split_num(categories, num):
  output = []
  for i in range(categories):
    output.append(random.randint(0, num//categories))
  total = sum(output)
  if total != num:
    loops = num - total
    for i in range(loops):
      output[i%categories] += 1
  return output

def encrypt(plaintext):
  encrypted = []
  for char in plaintext:
    encrypted += split_num(4, 255-ord(char))
  return ' '.join(str(e) for e in encrypted)

def start_challenge():
  print("Welcome to MEGACORP's proprietary encryption service! Just type your message below and out will come the encrypted text!\n")
  while True:
    plaintext = input("Please enter the message you wish to encrypt: ")
    while not plaintext:
      plaintext = input("Messages cannot be empty. Try again: ")
    ciphertext = encrypt(plaintext)
    print(f"Your encrypted message is: {ciphertext}\n")

start_challenge()
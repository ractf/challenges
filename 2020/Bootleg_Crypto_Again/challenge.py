import base64

def encrypt(plaintext, key):
  ciphertext = ""
  for i in range(len(plaintext)):
    ciphertext += chr((ord(plaintext[i]) + ord(key[i % len(key)])) % 255)
  return base64.b64encode(ciphertext.encode('utf-8')).decode('utf-8')

def start_challenge():
  print("Welcome MEGACORP admin! Feel free to encrypt any sensitive information using this service to protect against data theft.\n")
  while True:
    key = input("Please enter the secret key to encrypt the data with: ")
    while not key:
      key = input("The key cannot be empty. Please try again: ")
    plaintext = input("Please enter the data that you would like to encrypt: ")
    while not plaintext:
      plaintext = input("The plaintext cannot be empty. Please try again: ")
    print(f"Your encrypted message is: {encrypt(plaintext, key)}\n")

start_challenge()
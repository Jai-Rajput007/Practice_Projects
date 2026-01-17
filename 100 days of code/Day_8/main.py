from Encryption import encrypt
from Decryption import decrypt

print("Caesar Cipher here !!")
choice = input("You want to encode or decode :")
if choice == "encode":
    text = input("Enter the text : ").lower().strip().replace(" ","")
    shift = int(input("Enter the no. of positions you want to shift : "))
    ans = encrypt(text,shift)
    print(f"Here is your cipher text: {ans}")
else:
    text = input("Enter the cipher text : ").lower().strip().replace(" ","")
    shift = int(input("Enter the no. of positions you want to shift : "))
    ans = decrypt(text,shift)
    print(f"Here is your cipher text: {ans}")

import string

alphabet = list(string.ascii_lowercase)

def decrypt(input_text:str,shift_amount:int):
    cipher_text = ""
    for letter in input_text:
        shifted_position = alphabet.index(letter) - shift_amount
        shifted_position %= len(alphabet)
        cipher_text += alphabet[shifted_position]
    return cipher_text
def StringToByteIntArray(string):
    byteint_array = []
    
    for char in string:
        byteint_array.append(ord(char))
        
    return byteint_array

def OpenFileAsByteIntArray(filename):
    byteint_array = []
    byte = input_file.read(1)
    while (byte):
        byteint = int.from_bytes(plaintext_byte,byteorder='little')
        byteint_array.append(plaintext_byteint)
        byte = input_file.read(1)
        
    return byteint_array

def PermutationEncrypt(plaintext_byteintarray):
    pass
    
def PermutationDecrypt(ciphertext_byteintarray):
    pass
    
def ModifiedRC4Encrypt(plaintext_byteintarray,key_byteintarray):
    pass
    
def ModifiedRC4Decrypt(ciphertext_byteintarray,key_byteintarray):
    pass
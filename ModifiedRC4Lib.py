def StringToByteIntArray(string):
    byteint_array = []
    
    for char in string:
        byteint_array.append(ord(char))
        
    return byteint_array

def OpenFileAsByteIntArray(filename):
    input_file = open(filename,"rb")
    
    byteint_array = []
    byte = input_file.read(1)
    while (byte):
        byteint = int.from_bytes(byte,byteorder='little')
        byteint_array.append(byteint)
        byte = input_file.read(1)
        
    input_file.close()
        
    return byteint_array

def ModifiedKey(key):
    # Create Modified key in Stream Cipher
    # Input : key (string any length)
    # Output : modified key in numbers (length >= 256)

    # Change key to numbers
    modified_key = StringToByteIntArray(key)

    # Modified key if length <256
    i = len(modified_key)
    while (i<256):
        if (i==1):
            modified_key.append((2*modified_key[i-1])%256)
        else:
            modified_key.append((modified_key[i-1]+modified_key[i-2])%256)
        i = len(modified_key)

    return modified_key

def ModifiedKSA(key):
    # Create Modified KSA in Stream Cipher
    # Input : key (string any length)
    # Output : larik S teracak (numbers 0-255)

    # Inisialisasi larik S
    larik_S = []
    for i in range(256):
        larik_S.append(i)

    # Pengacakan larik S
    # Modifikasi: larik_S[i] --> larik_S[K[i]]
    # Sehingga menghasilkan nilai j yang lebih acak
    K = ModifiedKey(key)
    j = 0
    for i in range(256):
        j = (j+larik_S[K[i]]+K[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]

    return larik_S

def PermutationEncrypt(plaintext_byteintarray):
    pass
    
def PermutationDecrypt(ciphertext_byteintarray):
    pass
    
def ModifiedRC4Encrypt(plaintext_byteintarray,key):
    # Create Normal PRGA Encrypt in Stream Cipher
    # Input :   plaintext_byteintarray (byte in array)
    #           key (string any length)
    # Output :  ciphertext (byte in array)

    larik_S = ModifiedKSA(key)
    i = 0
    j = 0
    ciphertext_byteintarray = []

    # PRGA
    for idx in range(len(plaintext_byteintarray)-1):
        i = (i+1)%256
        j = (j+larik_S[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
        temp = (larik_S[j] + larik_S[i])%256
        keystream = larik_S[temp]
        ciphertext_byteintarray.append(keystream^plaintext_byteintarray[idx])
    
    return ciphertext_byteintarray
    
def ModifiedRC4Decrypt(ciphertext_byteintarray,key):
    # Create Normal PRGA Decrypt in Stream Cipher
    # Input :   ciphertext_byteintarray (byte in array)
    #           key (string any length)
    # Output :  plaintext (byte in array)

    larik_S = ModifiedKSA(key)
    i = 0
    j = 0
    plaintext_byteintarray = []

    # PRGA
    for idx in range(len(ciphertext_byteintarray)-1):
        i = (i+1)%256
        j = (j+larik_S[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
        temp = (larik_S[j] + larik_S[i])%256
        keystream = larik_S[temp]
        plaintext_byteintarray.append(keystream^ciphertext_byteintarray[idx])
    
    return plaintext_byteintarray
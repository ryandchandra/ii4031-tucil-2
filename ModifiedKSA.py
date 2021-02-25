def ModifiedKey(key):
    # Create Modified key in Stream Cipher
    # Input : key (string any length)
    # Output : modified key in numbers (length >= 256)

    # Change key to numbers
    modified_key = []
    for i in range(len(key)):
        modified_key.append(ord(key[i]))

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
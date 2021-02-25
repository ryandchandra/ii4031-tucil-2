# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from ModifiedRC4Lib import *
# Ini Stream cipher yang asli, cuma buat ngecek beda atau sama dengan modified nya
def KSA(key):
    larik_S = []
    for i in range(256):
        larik_S.append(i)
    K = []
    for i in range(len(key)):
        K.append(ord(key[i]))
    j = 0
    for i in range(256):
        j = (j+larik_S[i]+K[i%(len(K))])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
    return larik_S
def RC4Encrypt(plaintext_byteintarray,key):
    larik_S = KSA(key)
    i = 0
    j = 0
    ciphertext_byteintarray = []
    for idx in range(len(plaintext_byteintarray)-1):
        i = (i+1)%256
        j = (j+larik_S[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
        temp = (larik_S[j] + larik_S[i])%256
        keystream = larik_S[temp]
        ciphertext_byteintarray.append(keystream^plaintext_byteintarray[idx])
    return ciphertext_byteintarray
def RC4Decrypt(ciphertext_byteintarray,key_byteintarray):
    larik_S = KSA(key)
    i = 0
    j = 0
    plaintext_byteintarray = []
    for idx in range(len(ciphertext_byteintarray)-1):
        i = (i+1)%256
        j = (j+larik_S[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
        temp = (larik_S[j] + larik_S[i])%256
        keystream = larik_S[temp]
        plaintext_byteintarray.append(keystream^ciphertext_byteintarray[idx])
    return plaintext_byteintarray

key = 'aku'
plaintext = 'Hello World!'

A = ModifiedKSA(key)
B = KSA(key)
C = []
for i in range(256):
    C.append(A[i]==B[i])

D = ModifiedRC4Encrypt(StringToByteIntArray(plaintext),key)
E = RC4Encrypt(StringToByteIntArray(plaintext),key)
F = ModifiedRC4Decrypt(D, key)
G = RC4Decrypt(E, key)
print(D)
print("\n")
print(E)
print("\n")
print(F)
print("\n")
print(G)


# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from ModifiedKSA import *
# Ini KSA yang asli, cuma buat ngecek beda atau sama dengan modified nya
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

key = ' '
A = ModifiedKSA(key)
B = KSA(key)
C = []
for i in range(256):
    C.append(A[i]==B[i])
print(A)
print(B)
print(C)
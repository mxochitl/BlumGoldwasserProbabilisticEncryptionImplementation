import math
import numpy
import random
#Ensure installation of gmp lib (allows arbitrary integer maniplutation (to find modular arithmetic inverse))
try:
    import gmpy
except ImportError:
    print("Please install gmpy.")
    quit()




if __name__ == "__main__":
    # given constants
    p = 499
    q = 547
    a = -57
    b = 52
    m = '10011100000100001100'

    global x0
    x0 = [159201]

    # convert string to list of ints
    tmp = []
    for i in m:
        tmp.append(int(i))
    m=tmp


    print("The plaintext is:\t", m)

    
    ##################       Key Generation       ##################
    # Alice generates public key N and bitlength of m
    N = p*q
    L = len(m)

    ##################       Encrypt       ##################
    # Bob encodes M as a string of L bits
    bobsEncryption = []
    for i in range(L):
        # Each element is the least significant bit of x[i]
        # b_{i} equal to the least-significant bit of x_{i}.
        bobsEncryption.insert(0, int(bin(x0[i])[-1]))

        #Calculating x(i+1) = (x^2)%N
        # x_i = (x_{i-1})^2 mod N.
        x0.append( (x0[i]*x0[i])%N )

    # XORing the plaintext bits with the keystream
    cipher = []
    for i in range(L):
        # c = m XOR b
        cipher.append(int(m[i])^bobsEncryption[i])

    #Bob sends a message to Alice -- the enciphered bits and the final {\displaystyle x_{L}} x_L
    print("The Cipher text is:\t", cipher)

    ##################       Decrypt       ##################
    # Alice must compute r_{p}=y^{((p+1)/4)^{L}} mod p} and r_{q}=y^{((q+1)/4)^{L}} mod q}
    # Had to use the pow() function here because when you do a**d % n, you actually have to calculate a**d, which could be quite large. 
    # But there are ways of computing a**d % n without having to compute a**d itself, and that is what pow does. 
    r_p = pow(x0[L],(((p+1)//4)**L), p )
    r_q = pow(x0[L],(((q+1)//4)**L), q)

    # Compute the initial seed x_{0}=(q(q^{-1} mod p)*r_{p}+p(p^{-1} mod q)*r_{q} mod N
    p_inv = int(gmpy.invert(p, q))
    q_inv = int(gmpy.invert(q, p))

    x0 = [((q * (q_inv % p) * r_p) + (p * (p_inv % p) * r_q)) % N]
    
    #From x0, recompute the bit-vector b using the BBS generator, as in the encryption algorithm.
    bobsDecryption = []
    for i in range(L):
        # Each element is the least significant bit of x[i]
        # b_{i} equal to the least-significant bit of x_{i}.
        bobsDecryption.insert(0, int(bin(x0[i])[-1]))

        #Calculating x(i+1) = (x^2)%N
        # x_i = (x_{i-1})^2 mod N
        x0.append( (x0[i]*x0[i])%N )

    #Compute the plaintext by XORing the keystream with the ciphertext: {\displaystyle {\vec {m}}={\vec {c}}\oplus {\vec {b}}} {\vec m} = {\vec c} \oplus {\vec b}.
    ptxt = []
    for i in range(L):
        # c = m XOR b
        ptxt.append(int(cipher[i])^bobsDecryption[i])

    print("Alice deciphered to:\t", ptxt)
    print("Original message was:\t", m)
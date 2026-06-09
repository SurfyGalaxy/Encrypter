p = 23 #int(input("Prime number? "))
g = 5#int(input("Base? "))
a_private = 6#int(input("Secret a? "))
b_private = 15#int(input("Secret b? "))

a_public = (g ** a_private) % p
b_public = (g ** b_private) % p

print(f"A's public key: {a_public}")
print(f"B's public key: {b_public}")

a_common = (b_public ** a_private) % p
b_common = (a_public ** b_private) % p

print(f"Shared key: {a_common}, {b_common}")

# sigma0 bc funcs go here ig
def sigma0(x):
    MASK = 0xFFFFFFFF # Because python tries to be helpful / lossless
    rot7 = ((x >> 7) | (x << (32 - 7))) & MASK
    rot18 = ((x >> 18) | (x << (32 - 18))) & MASK
    shift3 = (x >> 3) & MASK
    return rot7 ^ rot18 ^ shift3 # XOR goes brrr

def sigma1(x):
    MASK = 0xFFFFFFFF
    rot17 = ((x >> 17) | (x << (32 - 17))) & MASK
    rot19 = ((x >> 19) | (x << (32 - 19))) & MASK
    shift10 = (x >> 10) & MASK
    return rot17 ^ rot19 ^ shift10 # XOR goes brrr vol. 2

# SHA256 TIME!!!!!

bits = f"{a_common:032b}" # 00000000000000000000000000000010
original_length = len(bits) # 32
original_length = f"{original_length:064b}" # 0000000000000000000000000000000000000000000000000000000000100000
print(f"Binary representation: {bits}")

bits = bits + '1' # 000000000000000000000000000000101
length = len(bits) # 33
padding = (448 - length) % 512 # 415

if padding == 0: # Because SHA256 likes being pedantic
    padding = 512
while padding != 0: # wooo 0 spam which is inefficient but idc
    padding -= 1
    bits = bits + '0'

# bits = 101000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000

bits = bits + original_length # Wow this will be long, you're getting it in hex
# 0x2800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020

# Ok time to parse

W = [bits[i:i+32] for i in range(0, 512, 32)] # 16 'words', W0 - W15

# W list:
# ['00000000000000000000000000000010', '10000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000000000', 
# '00000000000000000000000000000000', '00000000000000000000000000100000']
# Hope you like massive green text blocks!

W_ints = [int(word, 2) for word in W]
W_ints += [0] * 48 # oh no 

# [2, 2147483648, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
# 0, 0, 0]

for t in range(16, 64):
    # You could say... it's pretty sigma. 
    # I'll go now
    MASK = 0xFFFFFFFF
    next_word = sigma1(W_ints[t-2]) + W_ints[t-7] + sigma0(W_ints[t-15]) + W_ints[t-16]
    
    W_ints[t] = next_word & MASK

# [2, 2147483648, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 285220866, 2148794368, 335874728, 2149602568, 
# 604244416, 537221121, 2245072800, 403232086, 689514007, 2215434200, 937659630, 356146034, 3622600175, 
# 3970113100, 160481134, 602958137, 3999801780, 28148939, 1381843214, 1371659939, 1771734514, 310471629, 
# 1451437370, 33644316, 2994081427, 2491372921, 3232651549, 2570414982, 367623277, 1320604515, 164107689,
#  112315124, 2186246912, 3844969496, 2038881117, 687767609, 833828520, 1636763283, 3393557549, 2590202533, < y u stick out
# 1161748692, 2314927931, 3674480832, 1926178234, 2270863185, 3853778291, 1526002070, 2628575069]

# Var definitions bc im too lazy to scroll up
h0 = 0x6a09e667
h1 = 0xbb67ae85
h2 = 0x3c6ef372
h3 = 0xa54ff53a
h4 = 0x510e527f
h5 = 0x9b05688c
h6 = 0x1f83d9ab
h7 = 0x5be0cd19
a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

MASK = 0xFFFFFFFF

# All this for one var?
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]
# Sigma, but even better? If i was like 8 i'd be makig a joke abt sigma
def UpperSigma0(x):
    return (((x >> 2) | (x << 30)) ^ ((x >> 13) | (x << 19)) ^ ((x >> 22) | (x << 10))) & MASK

def UpperSigma1(x):
    return (((x >> 6) | (x << 26)) ^ ((x >> 11) | (x << 21)) ^ ((x >> 25) | (x << 7))) & MASK

def Ch(x, y, z):   return (x & y) ^ (~x & z)
def Maj(x, y, z):  return (x & y) ^ (x & z) ^ (y & z)

for t in range(0, 64):
    T1 = (h + UpperSigma1(e) + Ch(e, f, g) + K[t] + W_ints[t]) & MASK
    T2 = (UpperSigma0(a) + Maj(a, b, c)) & MASK
    
    # This aint like a minecraft shift register
    h = g
    g = f
    f = e
    e = (d + T1) & MASK
    d = c
    c = b
    b = a
    a = (T1 + T2) & MASK

# oh these guys are back hi 
h0 = (h0 + a) & MASK
h1 = (h1 + b) & MASK
h2 = (h2 + c) & MASK
h3 = (h3 + d) & MASK
h4 = (h4 + e) & MASK
h5 = (h5 + f) & MASK
h6 = (h6 + g) & MASK
h7 = (h7 + h) & MASK

the_mistake = f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}" # Still 2, trust me bro
# 433ebf5bc03dffa38536673207a21281612cef5faa9bc7a4d5b9be2fdb12cf1a  <- once was 2
# See? not scary... (don't look at the lines above)  (and rest in peices 2)

import cryptography # AGHHHH
del cryptography # good.

# Ok AES time
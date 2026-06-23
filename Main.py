p = 23 #int(input("Prime number? "))
g = 5#int(input("Base? "))
a_private = 6#int(input("Secret a? "))
b_private = 15#int(input("Secret b? "))

a_public = (g ** a_private) % p
b_public = (g ** b_private) % p

a_common = (b_public ** a_private) % p
b_common = (a_public ** b_private) % p


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

# nvm we've got to destroy our mistake again
mistake = f"{int(the_mistake, 16):0256b}" # HA binary spam again
# ['01000011001111101011111101011011', '11000000001111011111111110100011', '10000101001101100110011100110010', '00000111101000100001001010000001', 
# '01100001001011001110111101011111', '10101010100110111100011110100100', '11010101101110011011111000101111', '11011011000100101100111100011010',
#  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#  0, 0, 0, 0]


SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]
# AAAAAAAAAAAAAAAAAAHHHH WHY IS IT SO BIGGGG
RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]
def xtime(b):
    shifted = (b << 1) & 0xFF
    if b & 0x80:
        return shifted ^ 0x1B
    return shifted

INV_SBOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]
# THERES ANOTHER ONE??????????????????????????????????

def mul9(b):
    return xtime(xtime(xtime(b))) ^ b

def mul11(b):
    return xtime(xtime(xtime(b))) ^ xtime(b) ^ b

def mul13(b):
    return xtime(xtime(xtime(b))) ^ xtime(xtime(b)) ^ b

def mul14(b):
    return xtime(xtime(xtime(b))) ^ xtime(xtime(b)) ^ xtime(b)
# The gayolis field things are still scary

W = [0] * 60 # oh no not this guy again
for i in range(8):
    W[i] = mistake[i*32 : (i+1)*32]
for i in range(8, 60):
    temp = W[i-1]

    if i % 8 == 0: # RotWord, SubWord, Rcon
        # RotWord moves every byte to the left by 1, wrapping around
        byte0 = temp[0:8]
        byte1 = temp[8:16]
        byte2 = temp[16:24]
        byte3 = temp[24:32] # I'm sure there's an easier one-liner for this
        temp = byte1 + byte2 + byte3 + byte0

        # SubWord demolishes everything in a table i don't understand but exists
        byte0 = int(temp[0:8], 2)
        byte1 = int(temp[8:16], 2)
        byte2 = int(temp[16:24], 2)
        byte3 = int(temp[24:32], 2) # I'm sure there's an easier one-liner for this pt 2

        byte0 = SBOX[byte0]
        byte1 = SBOX[byte1]
        byte2 = SBOX[byte2]
        byte3 = SBOX[byte3]
        byte0 = f"{byte0:08b}"
        byte1 = f"{byte1:08b}"
        byte2 = f"{byte2:08b}"
        byte3 = f"{byte3:08b}"

        temp = byte0 + byte1 + byte2 + byte3

        # Rcon does something with the first byte to make it not patterny ig
        rcon_byte = int(temp[0:8], 2) ^ RCON[i // 8]
        temp = f"{rcon_byte:08b}" + temp[8:]
    elif i % 8 == 4: # SubWord
        byte0 = int(temp[0:8], 2)
        byte1 = int(temp[8:16], 2)
        byte2 = int(temp[16:24], 2)
        byte3 = int(temp[24:32], 2) # I'm sure there's an easier one-liner for this pt 2

        byte0 = SBOX[byte0]
        byte1 = SBOX[byte1]
        byte2 = SBOX[byte2]
        byte3 = SBOX[byte3]
        byte0 = f"{byte0:08b}"
        byte1 = f"{byte1:08b}"
        byte2 = f"{byte2:08b}"
        byte3 = f"{byte3:08b}"

        temp = byte0 + byte1 + byte2 + byte3

    back_8 = int(W[i-8], 2)
    temp = int(temp, 2)
    temp = back_8 ^ temp
    W[i] = f"{temp:032b}"

# ['01000011001111101011111101011011', '11000000001111011111111110100011', '10000101001101100110011100110010',i
#  '00000111101000100001001010000001', '01100001001011001110111101011111', '10101010100110111100011110100100',
#  '11010101101110011011111000101111', '11011011000100101100111100011010', '10001011101101000001110111100010',
#  '01001011100010011110001001000001', '11001110101111111000010101110011', '11001001000111011001011111110010',
#  '10111100100010000110011111010110', '00010110000100111010000001110010', '11000011101010100001111001011101',
#  '00011000101110001101000101000111', '11100101100010101011110101001111', '10101110000000110101111100001110',
#  '01100000101111001101101001111101', '10101001101000010100110110001111', '01101111101110101000010010100101',
#  '01111001101010010010010011010111', '10111010000000110011101010001010', '10100010101110111110101111001101',
#  '00001011011000110000000001110101', '10100101011000000101111101111011', '11000101110111001000010100000110',
#  '01101100011111011100100010001001', '00111111010001010110110000000010', '01000110111011000100100011010101',
#  '11111100111011110111001001011111', '01011110010101001001100110010010', '00100011100011010100111100101101',
#  '10000110111011010001000001010110', '01000011001100011001010101010000', '00101111010011000101110111011001',
#  '00101010011011000010000000110111', '01101100100000000110100011100010', '10010000011011110001101010111101',
#  '11001110001110111000001100101111', '11010001011000010101101010100110', '01010111100011000100101011110000',
#  '00010100101111011101111110100000', '00111011111100011000001001111001', '11001000110011010011001110000001',
#  '10100100010011010101101101100011', '00110100001000100100000111011110', '11111010000110011100001011110001',
#  '00100101010001001111101110001011', '01110010110010001011000101111011', '01100110011101010110111011011011',
#  '01011101100001001110110010100010', '10000100100100101111110110111011', '00100000110111111010011011011000',
#  '00010100111111011110011100000110', '11101110111001000010010111110111', '00001100011110111001001110100011',
#  '01111110101100110010001011011000', '00011000110001100100110000000011', '01000101010000101010000010100001']

# Wait
# WHAT DO YOU MEAN IT NEEDS TO BE A MATRIX
matricies = []

for i in range(0, 60, 4):  # because there's 15 of them for no good reason
    w0 = W[i]
    w1 = W[i+1]
    w2 = W[i+2]
    w3 = W[i+3]

    w0_b0, w0_b1, w0_b2, w0_b3 = w0[0:8], w0[8:16], w0[16:24], w0[24:32]
    w1_b0, w1_b1, w1_b2, w1_b3 = w1[0:8], w1[8:16], w1[16:24], w1[24:32]
    w2_b0, w2_b1, w2_b2, w2_b3 = w2[0:8], w2[8:16], w2[16:24], w2[24:32]
    w3_b0, w3_b1, w3_b2, w3_b3 = w3[0:8], w3[8:16], w3[16:24], w3[24:32]
    
    matricies.append([
[w0_b0, w1_b0, w2_b0, w3_b0],
[w0_b1, w1_b1, w2_b1, w3_b1],
[w0_b2, w1_b2, w2_b2, w3_b2],
[w0_b3, w1_b3, w2_b3, w3_b3]
])

# OOOOOOOOH NOOOOOOOOO
# VERY LONG COMMENT INBOUND


# 0111111', '00011101'],   <- hey why are you so short? i think vs codium has a buffer limit :/
#  ['00011101', '11100010', '10000101', '10010111'],
#  ['11100010', '01000001', '01110011', '11110010']]
# , [['10111100', '00010110', '11000011', '00011000'],
#  ['10001000', '00010011', '10101010', '10111000']
# , ['01100111', '10100000', '00011110', '11010001'
# ], ['11010110', '01110010', '01011101', '01000111']],
#  [['11100101', '10101110', '01100000', '10101001'],
#  ['10001010', '00000011', '10111100', '10100001'], 
# ['10111101', '01011111', '11011010', '01001101'],
#  ['01001111', '00001110', '01111101', '10001111']],
#  [['01101111', '01111001', '10111010', '10100010'],
#  ['10111010', '10101001', '00000011', '10111011'], 
# ['10000100', '00100100', '00111010', '11101011'],
#  ['10100101', '11010111', '10001010', '11001101']],
#  [['00001011', '10100101', '11000101', '01101100'],
#  ['01100011', '01100000', '11011100', '01111101'], 
# ['00000000', '01011111', '10000101', '11001000']
# , ['01110101', '01111011', '00000110', '10001001']], 
# [['00111111', '01000110', '11111100', '01011110'],
#  ['01000101', '11101100', '11101111', '01010100'],
#  ['01101100', '01001000', '01110010', '10011001'],
#  ['00000010', '11010101', '01011111', '10010010']]
# , [['00100011', '10000110', '01000011', '00101111'
# ], ['10001101', '11101101', '00110001', '01001100']
# , ['01001111', '00010000', '10010101', '01011101'],
#  ['00101101', '01010110', '01010000', '11011001']],
#  [['00101010', '01101100', '10010000', '11001110'],
# :3
#  ['01101100', '10000000', '01101111', '00111011'], 
# ['00100000', '01101000', '00011010', '10000011'], [
# '00110111', '11100010', '10111101', '00101111']], [
# ['11010001', '01010111', '00010100', '00111011'], [
# '01100001', '10001100', '10111101', '11110001'], 
# ['01011010', '01001010', '11011111', '10000010'],
#  ['10100110', '11110000', '10100000', '01111001']],
#  [['11001000', '10100100', '00110100', '11111010'],
#  ['11001101', '01001101', '00100010', '00011001'], 
# ['00110011', '01011011', '01000001', '11000010'],
#  ['10000001', '01100011', '11011110', '11110001']
# ], [['00100101', '01110010', '01100110', '01011101'],
#  ['01000100', '11001000', '01110101', '10000100'], 
# ['11111011', '10110001', '01101110', '11101100'],
#  ['10001011', '01111011', '11011011', '10100010']
# ], [['10000100', '00100000', '00010100', '11101110'],
#  ['10010010', '11011111', '11111101', '11100100'], 
# ['11111101', '10100110', '11100111', '00100101'], 
# ['10111011', '11011000', '00000110', '11110111']],
#  [['00001100', '01111110', '00011000', '01000101']
# , ['01111011', '10110011', '11000110', '01000010']
# , ['10010011', '00100010', '01001100', '10100000']
# , ['10100011', '11011000', '00000011', '10100001']]]

# Welp time to actually encrypt something ig :yay:
answered = False
while answered == False:
    e = input("Decrypt or Encrypt? ")
    if e == "encrypt":
        plaintext = input("What's your plaintext? ")
        answered = True
        encryption = True
    elif e == "decrypt":
        plaintext = input("What's your encrypted code? ")
        answered = True
        encryption = False
    else:
        print(f"{e} isn't encrypt or decrypt!")
death = []
if encryption == True:
    for char in plaintext:
        death.append(f"{ord(char):08b}")
else:
    for i in range(0, len(plaintext), 2):
        the_thing_hexagon = plaintext[i:i+2]
        death.append(f"{int(the_thing_hexagon, 16):08b}")
# death = ['01000001', '01110100', '01110100', '01100001', '01100011', '01101011', '00100000', '01100001', 
# '01110100', '00100000', '01100100', '01100001', '01110111', '01101110', '00100001', '00100001']
# len(death) = 16

# AES seems to be like SHA256 w/ padding in a way, so let's break out that spam

if encryption == True:
    if len(death) % 16 != 0: # bc we want 16 bc ofc we do 
        padding = 16 - (len(death) % 16)
    else: 
        padding = 16

    binary_number = f"{padding:08b}"
    while padding != 0:
        death.append(binary_number)
        padding -= 1 # this thing is still inefficient

# ['01000001', '01110100', '01110100', '01100001', '01100011', '01101011', '00100000',
#  '01100001', '01110100', '00100000', '01100100', '01100001', '01110111', '01101110',
#  '00100001', '00100001', '00010000', '00010000', '00010000', '00010000', '00010000',
#  '00010000', '00010000', '00010000', '00010000', '00010000', '00010000', '00010000',
#  '00010000', '00010000', '00010000', '00010000']

grid = []
for i in range(0, len(death), 16):
    for row_offset in range(4):
        row = []
        # Loop from the row start index to the end, skipping by 4
        for idx in range(i + row_offset, i + 16, 4):
            row.append(death[idx])
        grid.append(row)

# [['01000001', '01100011', '01110100', '01110111'], ['01110100', '01101011', '00100000', '01101110'],
#  ['01110100', '00100000', '01100100', '00100001'], ['01100001', '01100001', '01100001', '00100001'],
#  ['01000001', '01100011', '01110100', '01110111'], ['01110100', '01101011', '00100000', '01101110'],
#  ['01110100', '00100000', '01100100', '00100001'], ['01100001', '01100001', '01100001', '00100001']]

# the last part:tm:

# SubBytes > ShiftRows > MixColumns > AddRoundKey
i_dont_want_to_keep_doing_this_but_i_want_to_go_to_crux = "" # it's true

for block_index in range(0, len(grid), 4):
    current_death = grid[block_index : block_index + 4]
    if encryption == True: # Enjoy double reading the code...    sorry reviewer
        round_0_mix = []
        for r in range(4): 
            state_row = current_death[r]
            key_row = matricies[0][r] 
                
            c0 = f"{(int(state_row[0], 2) ^ int(key_row[0], 2)):08b}"
            c1 = f"{(int(state_row[1], 2) ^ int(key_row[1], 2)):08b}"
            c2 = f"{(int(state_row[2], 2) ^ int(key_row[2], 2)):08b}"
            c3 = f"{(int(state_row[3], 2) ^ int(key_row[3], 2)):08b}"
            round_0_mix.append([c0, c1, c2, c3])

        active_block_state = round_0_mix

        for round_thing in range(1, 15):
            new_thing = []
            for r in range(4):
                row = active_block_state[r]
                
                b0 = SBOX[int(row[0], 2)]
                b1 = SBOX[int(row[1], 2)]
                b2 = SBOX[int(row[2], 2)]
                b3 = SBOX[int(row[3], 2)]
                new_thing.append([f"{b0:08b}", f"{b1:08b}", f"{b2:08b}", f"{b3:08b}"])
                
            shifted_thing = [
                new_thing[0][:],                        
                new_thing[1][1:] + new_thing[1][:1],  
                new_thing[2][2:] + new_thing[2][:2],  
                new_thing[3][3:] + new_thing[3][:3] 
            ]

            if round_thing < 14: 
                mixed_thing = [[], [], [], []] 
                for col_offset in range(4):
                    s0 = int(shifted_thing[0][col_offset], 2)
                    s1 = int(shifted_thing[1][col_offset], 2)
                    s2 = int(shifted_thing[2][col_offset], 2)
                    s3 = int(shifted_thing[3][col_offset], 2)

                    new_s0 = xtime(s0) ^ (xtime(s1) ^ s1) ^ s2 ^ s3
                    new_s1 = s0 ^ xtime(s1) ^ (xtime(s2) ^ s2) ^ s3
                    new_s2 = s0 ^ s1 ^ xtime(s2) ^ (xtime(s3) ^ s3) 
                    new_s3 = (xtime(s0) ^ s0) ^ s1 ^ s2 ^ xtime(s3)

                    mixed_thing[0].append(f"{new_s0:08b}")
                    mixed_thing[1].append(f"{new_s1:08b}")
                    mixed_thing[2].append(f"{new_s2:08b}")
                    mixed_thing[3].append(f"{new_s3:08b}")
            else:
                mixed_thing = shifted_thing

            round_complete_mix = []
            for r in range(4): 
                state_row = mixed_thing[r]
                key_row = matricies[round_thing][r] 
                    
                c0 = f"{(int(state_row[0], 2) ^ int(key_row[0], 2)):08b}"
                c1 = f"{(int(state_row[1], 2) ^ int(key_row[1], 2)):08b}"
                c2 = f"{(int(state_row[2], 2) ^ int(key_row[2], 2)):08b}"
                c3 = f"{(int(state_row[3], 2) ^ int(key_row[3], 2)):08b}"
                round_complete_mix.append([c0, c1, c2, c3])
    else:

        round_0_mix = []
        for r in range(4): 
            state_row = current_death[r]
            key_row = matricies[14][r] 
                
            c0 = f"{(int(state_row[0], 2) ^ int(key_row[0], 2)):08b}"
            c1 = f"{(int(state_row[1], 2) ^ int(key_row[1], 2)):08b}"
            c2 = f"{(int(state_row[2], 2) ^ int(key_row[2], 2)):08b}"
            c3 = f"{(int(state_row[3], 2) ^ int(key_row[3], 2)):08b}"
            round_0_mix.append([c0, c1, c2, c3])

        active_block_state = round_0_mix
        for round_thing in range(1, 15):
            shifted_thing = [
            active_block_state[0][:],                        
            active_block_state[1][-1:] + active_block_state[1][:-1],  
            active_block_state[2][-2:] + active_block_state[2][:-2],  
            active_block_state[3][-3:] + active_block_state[3][:-3] 
        ]

        new_thing = []
        for r in range(4):
            row = shifted_thing[r]
            
            b0 = INV_SBOX[int(row[0], 2)]
            b1 = INV_SBOX[int(row[1], 2)]
            b2 = INV_SBOX[int(row[2], 2)]
            b3 = INV_SBOX[int(row[3], 2)]
            new_thing.append([f"{b0:08b}", f"{b1:08b}", f"{b2:08b}", f"{b3:08b}"])

        round_complete_mix = []
        for r in range(4): 
            state_row = new_thing[r]
            key_row = matricies[round_thing - 1][r]
                
            c0 = f"{(int(state_row[0], 2) ^ int(key_row[0], 2)):08b}"
            c1 = f"{(int(state_row[1], 2) ^ int(key_row[1], 2)):08b}"
            c2 = f"{(int(state_row[2], 2) ^ int(key_row[2], 2)):08b}"
            c3 = f"{(int(state_row[3], 2) ^ int(key_row[3], 2)):08b}"
            round_complete_mix.append([c0, c1, c2, c3])

        if round_thing > 1: # FIX: Bound tracks > 1 in reverse flow
            mixed_thing = [[], [], [], []] 
            for col_offset in range(4):
                s0 = int(round_complete_mix[0][col_offset], 2)
                s1 = int(round_complete_mix[1][col_offset], 2)
                s2 = int(round_complete_mix[2][col_offset], 2)
                s3 = int(round_complete_mix[3][col_offset], 2)

                # FIX: The 4 Inverse MixColumns equations using your mul9-mul14 macros!
                new_s0 = mul14(s0) ^ mul11(s1) ^ mul13(s2) ^ mul9(s3)
                new_s1 = mul9(s0)  ^ mul14(s1) ^ mul11(s2) ^ mul13(s3)
                new_s2 = mul13(s0) ^ mul9(s1)  ^ mul14(s2) ^ mul11(s3)
                new_s3 = mul11(s0) ^ mul13(s1) ^ mul9(s2)  ^ mul14(s3)

                mixed_thing[0].append(f"{new_s0:08b}")
                mixed_thing[1].append(f"{new_s1:08b}")
                mixed_thing[2].append(f"{new_s2:08b}")
                mixed_thing[3].append(f"{new_s3:08b}")
                
            active_block_state = mixed_thing
        else: 
            active_block_state = round_complete_mix
                
    active_block_state = round_complete_mix

    for col in range(4):
        for row in range(4):
            binary_byte = active_block_state[row][col]
            i_dont_want_to_keep_doing_this_but_i_want_to_go_to_crux += f"{int(binary_byte, 2):02x}"

if encryption == True:
    print("The thing you want that you can't read")
    print(i_dont_want_to_keep_doing_this_but_i_want_to_go_to_crux)
else:
    print("The thing you want but you can't read but you will soon")
    print(i_dont_want_to_keep_doing_this_but_i_want_to_go_to_crux)
    decrypted_text = bytes.fromhex(i_dont_want_to_keep_doing_this_but_i_want_to_go_to_crux).decode('utf-8')
    print("The actual thing you want")
    print(decrypted_text)
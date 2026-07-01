import math

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

RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]

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

# Sigma, but even better? If i was like 8 i'd be makig a joke abt sigma

def xtime(b):
    shifted = (b << 1) & 0xFF
    if b & 0x80:
        return shifted ^ 0x1B
    return shifted

def UpperSigma0(x):
    MASK = 0xFFFFFFFF
    return (((x >> 2) | (x << 30)) ^ ((x >> 13) | (x << 19)) ^ ((x >> 22) | (x << 10))) & MASK

def UpperSigma1(x):
    MASK = 0xFFFFFFFF
    return (((x >> 6) | (x << 26)) ^ ((x >> 11) | (x << 21)) ^ ((x >> 25) | (x << 7))) & MASK

def sigma0(x):
    MASK = 0xFFFFFFFF
    return (((x >> 7) | (x << 25)) ^ ((x >> 18) | (x << 14)) ^ (x >> 3)) & MASK

def sigma1(x):
    MASK = 0xFFFFFFFF
    return (((x >> 17) | (x << 15)) ^ ((x >> 19) | (x << 13)) ^ (x >> 10)) & MASK

def Ch(x, y, z):   return (x & y) ^ (~x & z)
def Maj(x, y, z):  return (x & y) ^ (x & z) ^ (y & z)

def mul9(b):
    return xtime(xtime(xtime(b))) ^ b

def mul11(b):
    return xtime(xtime(xtime(b))) ^ xtime(b) ^ b

def mul13(b):
    return xtime(xtime(xtime(b))) ^ xtime(xtime(b)) ^ b

def mul14(b):
    return xtime(xtime(xtime(b))) ^ xtime(xtime(b)) ^ xtime(b)
# The gayolis field things are still scary


def check_prime(var: int) -> bool:
    if var <= 1:
        return False
    if var == 2:
        return True
    if var % 2 == 0:
        return False
    
    max_int = int(math.isqrt(var))
    for i in range(3, max_int + 1, 2):
        if var % i == 0:
            return False
    
    return True

# ==========================================================================================================================
# ==========================================================================================================================
# ==========================================================================================================================

def make_dhke(prime: int, base:int, private:int) -> int: # Makes a public key
    return pow(base, private, prime)

def calculate_dhke(prime: int, private: int, public: int) -> int: # Makes a shared private
    return pow(public, private, prime)

def sha256(key: int) -> str:
    temp = pad_sha256(key)
    temp = make_words_sha256(temp)
    return sha256_calculate(temp)

def pad_sha256(key: int) -> str:
    bits = f"{key:032b}" # 00000000000000000000000000000010
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
    return bits

def make_words_sha256(bits: str) -> list:
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

    return W_ints

    # [2, 2147483648, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 285220866, 2148794368, 335874728, 2149602568, 
    # 604244416, 537221121, 2245072800, 403232086, 689514007, 2215434200, 937659630, 356146034, 3622600175, 
    # 3970113100, 160481134, 602958137, 3999801780, 28148939, 1381843214, 1371659939, 1771734514, 310471629, 
    # 1451437370, 33644316, 2994081427, 2491372921, 3232651549, 2570414982, 367623277, 1320604515, 164107689,
    #  112315124, 2186246912, 3844969496, 2038881117, 687767609, 833828520, 1636763283, 3393557549, 2590202533, < y u stick out
    # 1161748692, 2314927931, 3674480832, 1926178234, 2270863185, 3853778291, 1526002070, 2628575069]

def sha256_calculate(W_ints: list) -> str:
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

    return f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}" # Still 2, trust me bro

def make_matrix(sha256: str) -> list:
    global SBOX, INV_SBOX, RCON
    mistake = f"{int(sha256, 16):0256b}"
    
    W = [0] * 60
    for i in range(8):
        W[i] = int(mistake[i*32 : (i+1)*32], 2)
    
    for i in range(8, 60):
        temp = W[i-1]
        
        if i % 8 == 0:
            # RotWord
            byte0 = (temp >> 24) & 0xFF
            byte1 = (temp >> 16) & 0xFF
            byte2 = (temp >> 8) & 0xFF
            byte3 = temp & 0xFF
            temp = (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte0
            
            # SubWord
            byte0 = SBOX[(temp >> 24) & 0xFF]
            byte1 = SBOX[(temp >> 16) & 0xFF]
            byte2 = SBOX[(temp >> 8) & 0xFF]
            byte3 = SBOX[temp & 0xFF]
            temp = (byte0 << 24) | (byte1 << 16) | (byte2 << 8) | byte3
            
            # Rcon
            rcon_byte = ((temp >> 24) & 0xFF) ^ RCON[i // 8]
            temp = (rcon_byte << 24) | (temp & 0x00FFFFFF)
            
        elif i % 8 == 4:
            # SubWord
            byte0 = SBOX[(temp >> 24) & 0xFF]
            byte1 = SBOX[(temp >> 16) & 0xFF]
            byte2 = SBOX[(temp >> 8) & 0xFF]
            byte3 = SBOX[temp & 0xFF]
            temp = (byte0 << 24) | (byte1 << 16) | (byte2 << 8) | byte3
        
        W[i] = W[i-8] ^ temp
    
    matricies = []
    for i in range(0, 60, 4):
        w0 = W[i]
        w1 = W[i+1]
        w2 = W[i+2]
        w3 = W[i+3]
        
        matricies.append([
            [(w0 >> 24) & 0xFF, (w1 >> 24) & 0xFF, (w2 >> 24) & 0xFF, (w3 >> 24) & 0xFF],
            [(w0 >> 16) & 0xFF, (w1 >> 16) & 0xFF, (w2 >> 16) & 0xFF, (w3 >> 16) & 0xFF],
            [(w0 >> 8) & 0xFF, (w1 >> 8) & 0xFF, (w2 >> 8) & 0xFF, (w3 >> 8) & 0xFF],
            [w0 & 0xFF, w1 & 0xFF, w2 & 0xFF, w3 & 0xFF]
        ])
    
    return matricies

def aes256_encrypt(plaintext, matrices):
    global SBOX, RCON, INV_SBOX
    
    # Convert plaintext to integers (bytes)
    death = []
    for char in plaintext:
        death.append(ord(char))
    
    # Add padding (PKCS#7)
    if len(death) % 16 != 0:
        padding = 16 - (len(death) % 16)
    else:
        padding = 16
    
    while padding != 0:
        death.append(padding)
        padding -= 1
    
    # Create grid of integers
    grid = []
    for i in range(0, len(death), 16):
        for row_offset in range(4):
            row = []
            for idx in range(i + row_offset, i + 16, 4):
                row.append(death[idx])
            grid.append(row)
    
    # Process encryption
    result = ""
    for block_index in range(0, len(grid), 4):
        current_death = grid[block_index: block_index + 4]
        
        # Initial AddRoundKey (Round 0)
        round_0_mix = []
        for r in range(4):
            state_row = current_death[r]
            key_row = matrices[0][r]
            
            # Key row values are integers (0-255)
            c0 = state_row[0] ^ key_row[0]
            c1 = state_row[1] ^ key_row[1]
            c2 = state_row[2] ^ key_row[2]
            c3 = state_row[3] ^ key_row[3]
            round_0_mix.append([c0, c1, c2, c3])
        
        active_block_state = round_0_mix
        
        for round_thing in range(1, 15):
            # SubBytes
            new_thing = []
            for r in range(4):
                row = active_block_state[r]
                new_thing.append([
                    SBOX[row[0]],
                    SBOX[row[1]],
                    SBOX[row[2]],
                    SBOX[row[3]]
                ])
            
            # ShiftRows
            shifted_thing = [
                new_thing[0][:],
                new_thing[1][1:] + new_thing[1][:1],
                new_thing[2][2:] + new_thing[2][:2],
                new_thing[3][3:] + new_thing[3][:3]
            ]
            
            if round_thing < 14:
                mixed_thing = [[], [], [], []]
                for col_offset in range(4):
                    s0 = shifted_thing[0][col_offset]
                    s1 = shifted_thing[1][col_offset]
                    s2 = shifted_thing[2][col_offset]
                    s3 = shifted_thing[3][col_offset]
                    
                    new_s0 = xtime(s0) ^ (xtime(s1) ^ s1) ^ s2 ^ s3
                    new_s1 = s0 ^ xtime(s1) ^ (xtime(s2) ^ s2) ^ s3
                    new_s2 = s0 ^ s1 ^ xtime(s2) ^ (xtime(s3) ^ s3)
                    new_s3 = (xtime(s0) ^ s0) ^ s1 ^ s2 ^ xtime(s3)
                    
                    mixed_thing[0].append(new_s0)
                    mixed_thing[1].append(new_s1)
                    mixed_thing[2].append(new_s2)
                    mixed_thing[3].append(new_s3)
                
                round_mix = []
                for r in range(4):
                    state_row = mixed_thing[r]
                    key_row = matrices[round_thing][r]
                    
                    round_mix.append([
                        state_row[0] ^ key_row[0],
                        state_row[1] ^ key_row[1],
                        state_row[2] ^ key_row[2],
                        state_row[3] ^ key_row[3]
                    ])
                active_block_state = round_mix
            else:
                round_mix = []
                for r in range(4):
                    state_row = shifted_thing[r]
                    key_row = matrices[round_thing][r]
                    
                    round_mix.append([
                        state_row[0] ^ key_row[0],
                        state_row[1] ^ key_row[1],
                        state_row[2] ^ key_row[2],
                        state_row[3] ^ key_row[3]
                    ])
                active_block_state = round_mix
        
        for col in range(4):
            for row in range(4):
                result += f"{active_block_state[row][col]:02x}"
    
    return result


def aes256_decrypt(ciphertext, matrices):
    global SBOX, RCON, INV_SBOX
    
    # Convert hex ciphertext to integers
    death = []
    for i in range(0, len(ciphertext), 2):
        death.append(int(ciphertext[i:i+2], 16))
    
    # Create grid
    grid = []
    for i in range(0, len(death), 16):
        for row_offset in range(4):
            row = []
            for idx in range(i + row_offset, i + 16, 4):
                row.append(death[idx])
            grid.append(row)
    
    # Process decryption
    result = ""
    for block_index in range(0, len(grid), 4):
        current_death = grid[block_index: block_index + 4]
        
        round_0_mix = []
        for r in range(4):
            state_row = current_death[r]
            key_row = matrices[14][r]
            
            round_0_mix.append([
                state_row[0] ^ key_row[0],
                state_row[1] ^ key_row[1],
                state_row[2] ^ key_row[2],
                state_row[3] ^ key_row[3]
            ])
        
        active_block_state = round_0_mix
        
        for round_thing in range(14, 0, -1):
            r0 = active_block_state[0]
            r1 = active_block_state[1]
            r2 = active_block_state[2]
            r3 = active_block_state[3]
            
            shifted_thing = [
                [r0[0], r0[1], r0[2], r0[3]],
                [r1[3], r1[0], r1[1], r1[2]],
                [r2[2], r2[3], r2[0], r2[1]],
                [r3[1], r3[2], r3[3], r3[0]]
            ]
            
            new_thing = []
            for r in range(4):
                row = shifted_thing[r]
                new_thing.append([
                    INV_SBOX[row[0]],
                    INV_SBOX[row[1]],
                    INV_SBOX[row[2]],
                    INV_SBOX[row[3]]
                ])
            
            round_complete_mix = []
            key_index = round_thing - 1
            for r in range(4):
                state_row = new_thing[r]
                key_row = matrices[key_index][r]
                
                round_complete_mix.append([
                    state_row[0] ^ key_row[0],
                    state_row[1] ^ key_row[1],
                    state_row[2] ^ key_row[2],
                    state_row[3] ^ key_row[3]
                ])
            
            if round_thing > 1:
                mixed_thing = [[], [], [], []]
                for col_offset in range(4):
                    s0 = round_complete_mix[0][col_offset]
                    s1 = round_complete_mix[1][col_offset]
                    s2 = round_complete_mix[2][col_offset]
                    s3 = round_complete_mix[3][col_offset]
                    
                    mixed_thing[0].append(mul14(s0) ^ mul11(s1) ^ mul13(s2) ^ mul9(s3))
                    mixed_thing[1].append(mul9(s0) ^ mul14(s1) ^ mul11(s2) ^ mul13(s3))
                    mixed_thing[2].append(mul13(s0) ^ mul9(s1) ^ mul14(s2) ^ mul11(s3))
                    mixed_thing[3].append(mul11(s0) ^ mul13(s1) ^ mul9(s2) ^ mul14(s3))
                
                active_block_state = mixed_thing
            else:
                active_block_state = round_complete_mix
        
        for col in range(4):
            for row in range(4):
                result += f"{active_block_state[row][col]:02x}"
    
    try:
        decrypted_bytes = bytes.fromhex(result)
        # Remove padding (PKCS#7)
        padding_len = decrypted_bytes[-1]
        if 0 < padding_len <= 16:
            decrypted_bytes = decrypted_bytes[:-padding_len]
        return decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return False


def aes256(sha256, text, encrypt):
    matrices = make_matrix(sha256)

    if encrypt == True:
        result = aes256_encrypt(text, matrices)
    else:
        result = aes256_decrypt(text, matrices)
    
    return result

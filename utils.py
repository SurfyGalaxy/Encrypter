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
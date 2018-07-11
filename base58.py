'''Accepts a integer value and returns its Base58 representation'''

import hashlib

alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

size = len(alphabet)

int_to_b58 = {i:ch for i,ch in enumerate(alphabet)}
b58_to_int = {ch:i for i,ch in enumerate(alphabet)}

def sha256(message,encoding='utf-8'): #convienient wrapper to easily compute sha256 hashes and return hex-strings (NOTE: string is without leading '0x')
    m = hashlib.sha256()
    m.update(str(message).encode(encoding))
    return m.hexdigest()

def divide(zahl,basis):
    '''Takes a number and basis, returns (times,remainder) = number modulo basis, has two return values'''
    r = zahl % basis
    t = int(zahl / basis)
    return t,r

def base58encode(integer):
    '''Takes a integer and turns it to its base58 representation as  string'''
    x = integer
    res = ''
    while x >0:
        x,remainder = divide(x,size)
        res+=int_to_b58[remainder]
    return res[::-1] #Reverse the string

def base58decode(base58_input):
    base58_string = base58_input[::-1] #First reverse the string
    res = 0
    for i in range(len(base58_string)):
        res+=b58_to_int[base58_string[i]]*(size**i)
    return res

'''
def base58check_encode(message):
    check = int(sha256(sha256(str(message)))[:4],16)
    return base58encode(str(message)+str(check))
'''

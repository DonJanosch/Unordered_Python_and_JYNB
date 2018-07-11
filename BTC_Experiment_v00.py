import hashlib #import hashlib to compute hash algorithms
import base58 #own base58 conversion modul

def sha256(message,encoding='utf-8'): #convienient wrapper to easily compute sha256 hashes and return hex-strings (NOTE: string is without leading '0x')
    m = hashlib.sha256()
    m.update(message.encode(encoding))
    return m.hexdigest()

def ripedm160(message,encoding='utf-8'):
    m = hashlib.new('ripemd160')
    m.update(message.encode(encoding))
    return m.hexdigest()

Seed ='Piggy' #Choose a seed, can be a word or phrase

pk_hex = sha256(Seed) #get the private key from seed phrase which is just the hex value of the hash
pk_int = int(pk_hex,16) #turn the hex value to an integer
pk_bin = bin(pk_int)[2:] #turn the integer to a binary bitstring and ignore the leading '0b'

pub_adr_hex = ripedm160(pk_hex)
pub_adr_int = int(pub_adr_hex,16)
pub_adr_b58 = base58.base58encode(pub_adr_int)

print(pk_hex)
print(pk_int)
print(pk_bin)

print(pub_adr_b58)

import hashlib, binascii

def sha256(message,encoding='utf-8'):
    m =hashlib.sha256()
    m.update(str(message).encode(encoding))
    return m.hexdigest()

def doublesha256(message,encoding='utf-8'):
    m = hashlib.sha256(message.encode(encoding))
    m2 = hashlib.sha256()
    m2.update(m.digest())
    return m2.hexdigest()

def hex2bin(hex_string,dim=256):
    res = bin(int(hex_string, 16))[2:]
    l = len(res)
    res = (dim-l)*'0'+res
    return res

def bin2int(binarystring):
    return int(binarystring, base=2)

BIP39_word_list = []
with open('BIP39_Wordlist.txt','r') as f:
    BIP39_word_list = f.read().splitlines()

index_to_word = {i:ch for i,ch in enumerate(BIP39_word_list)} #Make look up table for foreward encoding

entropy_input = input('Give me a string to turn it into 24 BIP39 compatible seed words')
entropy_hash_hex = sha256(entropy_input)
entropy_hash_bin = hex2bin(entropy_hash_hex)
entropy_hash_checksum = doublesha256(entropy_input)
entropy_hash_bin+= hex2bin(entropy_hash_checksum)[:8]
index = bin2int('0b'+entropy_hash_bin[:11])

word_list = []
for i in range(24):
    word_index = bin2int('0b'+entropy_hash_bin[:11])
    word_list.append(index_to_word[word_index])
    entropy_hash_bin = entropy_hash_bin[11:]

print(' '.join(word_list))


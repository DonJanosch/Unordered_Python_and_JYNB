'''
Quick and dirty little script to calculate Bitcoin BIP39 compatible seed words from a specified entropy input.
!!!DO NOT USE IF YOU DONT KNOW WHAT YOU ARE DOING AND DONT FULLY UNDERSTAND THIS SCRIPT, YOU ARE AT RISK OF LOOSING YOUR FUNDS!!!
Developed by Jan Macenka, last update 2018-02-27
'''
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

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def tobitstring(s):
    result = ''
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result+=bits
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def str_to_hex(string):
    return string.encode('utf-8').hex()

def str_to_bin(string):
    return string.encode('utf-8')

def moreSeeds(amount=1):
    '''Give me an integer as loop counter'''
    for _ in range(int(amount)):
        print(line_separator)
        print('Give me a string to turn it into a list of 24 BIP39 compatible seed words')
        entropy_input = input('')
        entropy_hash_hex = sha256(entropy_input)
        entropy_hash_bin = hex2bin(entropy_hash_hex)
        entropy_hash_checksum = doublesha256(entropy_input)
        entropy_hash_bin+= hex2bin(entropy_hash_checksum)[:8]
        print('Raw entropy: {}'.format(entropy_hash_bin))
        index = bin2int('0b'+entropy_hash_bin[:11])
        word_list = []
        for i in range(24):
            word_index = bin2int('0b'+entropy_hash_bin[:11])
            word_list.append(index_to_word[word_index])
            entropy_hash_bin = entropy_hash_bin[11:]
        print('\nYour BIP39-Seed-Words for \'{}\' are:'.format(entropy_input))
        print('\n')
        print(' '.join(word_list))
        print(line_separator)
        print('\n')

word_list_autenticity = '187db04a869dd9bc7be80d21a86497d692c0db6abd3aa8cb6be5d618ff757fae'
fileName = 'BIP39_Wordlist.txt'
openFile = open(fileName)
readFile = openFile.read()
openFile.close()
if sha256(readFile) != word_list_autenticity:
    print('The file \'{}\' does not match the required hash-value. Please provide it in original form with english word according to BIP39!'.format(fileName))
else:
    BIP39_word_list = []
    with open(fileName,'r') as f:
        BIP39_word_list = f.read().splitlines()

    index_to_word = {i:ch for i,ch in enumerate(BIP39_word_list)} #Make look up table for foreward encoding

    line_separator = '################'

    print(line_separator)
    print('DISCLAIMER:\nDies ist ein frei entwickeltes Tool, welches nicht zur Verwendung empfohlen wird.\nEs wird aus einem Entropy-Input eine BIP39 kompatible Seed-Word-Serie bestehend aus 24 Wörtern erstellt.\nEs werden für die Verwendung des Tools keinerlei Gewährleistungen gegeben oder impliziert!\nNochmal ausführen mit \'moreSeeds(<INTEGER>)\'\nAUSDRÜCKLICHE WARNUNG:\nNutze dieses Tool nicht, wenn dir die Begriffe Social-Password-Engineering, Entropy-Bits oder Rainbowtables nichts sagen!!!\nDer Mensch ist unglaublich schlecht darin, Zufall zu produzieren!')
    print(line_separator,'\n')

    moreSeeds()

'''Accepts a integer value and returns its Base58 representation'''
import hashlib #require for SHA512

alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ9'#The presmissible dictionary used in IOTA

size = len(alphabet) #Calculate the size of the dicitionary, should be 27 in cas of IOTA

int_to_b27 = {i:ch for i,ch in enumerate(alphabet)} #Make look up table for foreward encoding

def sha512(message,encoding='utf-8'): #convienient wrapper to easily compute sha256 hashes and return hex-strings (NOTE: string is without leading '0x')
    m = hashlib.sha512() #Assign new SHA512 object
    m.update(str(message).encode(encoding)) #Feed it
    return m.hexdigest() #return the hex value of the SHA512-Hash

def divide(zahl,basis): #Modulo calculation which also returns two values
    '''Takes a number and basis, returns (times,remainder) = number modulo basis, has two return values'''
    r = zahl % basis #Calculate the modulo
    t = int(zahl / basis) #Calculate the number of clock-cycles
    return t,r #Return both

def base27encode(hex_wert):
    '''Takes a hex value and turns it to its base58 representation as  string, dont use leading '0b\''''
    x = int(hex_wert,16) #Convert the hex value to integer since we are calculating in base10 in this function
    res = '' #Make an empty string as return value which gets updated during the process
    while x >0: #Reccursive function to get from base10 to base27
        x,remainder = divide(x,size) #Loop until x is zero
        res+=int_to_b27[remainder] #The remainer (modulo-value) determines the position of the letter in the used alphabeth
    return res[::-1] #Reverse the string (would not be necessary for the purpous of seed generation but mathematically it is correct this way)

def calculate_seed_from_word(message):
    '''Takes a random seed phrase or word, calculates the SHA512 hash value of it,
    the hash value equals the number range of 2^256 which equals roughly 1.1579209*10^77
    for IOTA a we need a number 27^81 which equals roughly 8.718964*10^115 so one hash value is not enough
    therefore we hash the hash again and concatenate them, then converte them to base27 and use the first 81 digits
    '''
    tmp = sha512(message) #Calculate the has of  the seed word or phrase.
    seed = base27encode(tmp)[:81] #Converte them to the Base27 letter-Alphabet and return the first 81 digits of it
    return seed

res = calculate_seed_from_word(input())

print(res)

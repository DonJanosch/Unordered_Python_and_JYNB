'''
This is a mixture of class and script meant for educational purpouse only. It shows the way BIP44 works.
Autor: Jan Macenka
'''
import hashlib, binascii

#Please read this disclaimer
disclaimer = '**********DISCLAIMER**********\n'\
             'Quick and dirty little python3-script to show how a BIP44 Wallet will produce new privateKeys from a bunch of seed-settings.\n'\
             'For educational purpous only. No conversion to base58check or Bech32, all numbers are displayed as raw hex-values.\n'\
             '\n!!!DONT USE IT TO DERIVE REAL PRIVATE KEYS!!!\n'\
             '!!!NO WARRANTY OR GUARANTEE OF ANY KIND ARE GIVEN OR IMPLIED!!!\n'\
             '\nDeveloped by Jan Macenka, last update 2018-03-22\n'\
             '******************************\n'\
             '\nType generateNewWallet() to get 10 new privateKeys from the seed-settings with a script.'\
             '\nWallets are generated from the wallet-class SHA256PRNG (see this script-code).'\
             '\nAll generaded Wallets are stored in the list open_wallets[<index>] for you to access and play around with.'

class SHA256PRNG:
    '''Class for generating privateKeys according to BIP44. JUST FOR EDUCATIONAL PURPOUS! DONT USE IN REAL WORDL-APPLICATION!'''
    def __init__(self,entropy_seed_for_Mnemonic = 1, Passphrase = '', Mnemonic = None, Derivation_coin = 0, Derivation_wallet = 0, Derivation_adress = 0, Derivation_index = 0):
        '''Initializes all class-object internal variables, derives the chain-code from SHA256(entropy_seed_for_Mnemonic)'''
        self.counter = 0 #Iteration counter to keep track of how many privateKeys we have produced so far
        self.Passphrase = Passphrase
        self.Derivation_coin = Derivation_coin
        self.Derivation_wallet = Derivation_wallet
        self.Derivation_adress = Derivation_adress
        self.Derivation_index = Derivation_index - 1
        self.entropy_seed_for_Mnemonic = entropy_seed_for_Mnemonic
        self.Derivation_path = self.makeDerivationPath()
        if Mnemonic == None:
            self.Mnemonic = self.sha256(entropy_seed_for_Mnemonic)
        else:
            self.Mnemonic = Mnemonic
            if entropy_seed_for_Mnemonic != '':
                print('Notification: You can either specify a entropy seed or a Mnemonic, they are the same thing... You specified both, will keep only the Mnemonic for further calculations')
        
    def sha256(self,message,encoding='utf-8'):
        '''Calculates the SHA256 hash on some input, input is interpreted as utf-8 formatted string'''
        m =hashlib.sha256()
        m.update(str(message).encode(encoding))
        return m.hexdigest()

    def makeDerivationPath(self):
        '''Returns the derivation path defined by the class-objects internal variables'''
        return str('m/'+str(self.Derivation_coin)+'\'/'+str(self.Derivation_wallet)+'\'/'+str(self.Derivation_adress)+'/'+str(self.Derivation_index))

    def makeNextPrivKey(self):
        '''Increases the Derivation_index of the class-object by 1 and returns a tuple with (Derivation_path,privateKey)'''
        self.Derivation_index += 1
        self.counter += 1
        self.Derivation_path = self.makeDerivationPath()
        entropy = str(self.Mnemonic)+str(self.Passphrase)+str(self.Derivation_path)
        return (self.Derivation_path,self.sha256(entropy))

    def makeManyMorePrivateKeys(self,number):
        '''Accepts integer N as input
        Returns a list of tupels like this [(Derivation_path0,privateKey0),(Derivation_path1,privateKey1), ...] with N entries'''
        res = []
        for _ in range(number):
            path,key = self.makeNextPrivKey()
            res.append((path,key))
        return res

    def tellMeHowManyPrivateKeysWeHaveGeneratedSoFar(self):
        '''Returns a counter of how many privateKeys have been generated so far from this wallet'''
        return self.counter

    def tellMeTheMnemonic(self):
        '''Returns the Mnemonic of the wallet in hexadecimal format'''
        return self.Mnemonic

    def tellMeLastDerivationPath(self):
        '''Returns a string with the current Derivation path of the latest generated privateKey'''
        return self.makeDerivationPath()

    def tellMePassphrase(self):
        '''Returns a string with the walles Passphrase'''
        return self.Passphrase
    
    def set_Derivation_coin(self,Derivation_coin):
        '''Accepts a integer as input to be the new Derivation_coin for the Derivation_path, also resets the Derivation_index to 0'''
        self.Derivation_coin = Derivation_coin
        self.Derivation_index = 0
        print('Derivation_coin now is {}. Also resetting Derivation_index to 0'.format(self.Derivation_coin))

    def set_Derivation_wallet(self,Derivation_wallet):
        '''Accepts a integer as input to be the new Derivation_wallet for the Derivation_path, also resets the Derivation_index to 0'''
        self.Derivation_wallet = Derivation_wallet
        self.Derivation_index = 0
        print('Derivation_wallet now is {}. Also resetting Derivation_index to 0'.format(self.Derivation_wallet))

    def set_Derivation_adress(self,Derivation_adress):
        '''Accepts a integer as input to be the new Derivation_adress for the Derivation_path, also resets the Derivation_index to 0'''
        self.Derivation_adress = Derivation_adress
        self.Derivation_index = 0
        print('Derivation_adress now is {}. Also resetting Derivation_index to 0'.format(self.Derivation_adress))
        
    def set_Derivation_index(self,Derivation_index):
        '''Accepts a integer as input to be the new Derivation_index for the Derivation_path'''
        self.Derivation_index = Derivation_index
        print('Derivation_index is now {}'.format(self.Derivation_index))
        if self.Derivation_index == 0:
            self.Derivation_index -= 1 #To make sure, the first generated privateKey is for index 0

    def set_Passphrase(self,new_Passphrase):
        '''Accepts a integer as input to be the new Derivation_index for the Derivation_path'''
        self.Passphrase = new_Passphrase
        print('New Passphrase is now \'{}\'. CAUTION: Now secretKeys are derived form a new source!'.format(self.Passphrase))

#A bunch of Variables required for the script to run, can be manipulated from the shell
open_wallets = [] #Will hold all the wallet-objects that are generated from the SHA256PRNG-class
my_Passphrase = '' #The additional pass-phrase as string
my_Derivation_coin = 44 #The Derivation_coin. 44 = Bitcoin
my_Derivation_wallet = 0 #The Derivation_wallet. Usually 0 = Main Wallet, 1 = Change Wallet, more are possible.
my_Derivation_adress = 0 #The Derivation_adress. Usually starting at 0, more sub-wallet-adresses can be generated
my_Derivation_index = 0 #The Derivation_inedex. This is a iterative counter which is increased by +1 to get to the next privatKey
number_of_keys_to_calculate = 10 #A loop parameter for the script to specify how many adresses shall be calculated in the beginning

def generateNewWallet():
    '''Script that generates a new wallet-object from the class SHA256PRNG and prints out the first couple of private keys.
    Afterwards the newly generated wallet is appended to the list open_wallets[] from which it can be accessed for further use.'''
    Seed = input('Give me a seed (entropy)\n')
    my_Passphrase = input('Give me a Passphrase (just press Enter to skip this step)\n')
    myPRNG = SHA256PRNG(entropy_seed_for_Mnemonic = Seed, Passphrase = my_Passphrase, Derivation_coin = my_Derivation_coin, Derivation_wallet = my_Derivation_wallet, Derivation_adress = my_Derivation_adress, Derivation_index = my_Derivation_index) #Ist von der refferenzierung her sehr unsauber gelöst, ich weiß... ist mir aber bei einem quick-and-dirty script egal
    print('\nUsing \'{}\' as seed which derives \'{}\' as chaincode.\nUsing \'{}\' as Passphrase.\nStoring the new Wallet in list open_wallets[{}].\n\nGenerating the first {} privateKeys starting at Derivation-Path {}:'.format(Seed, myPRNG.sha256(Seed), my_Passphrase,len(open_wallets),number_of_keys_to_calculate, myPRNG.makeDerivationPath()))
    for _ in range(number_of_keys_to_calculate):
        Derivation_Path, privateKey = myPRNG.makeNextPrivKey()
        print('PrivateKey of {} is \'{}\''.format(Derivation_Path, privateKey))
    open_wallets.append(myPRNG)
    #return myPRNG #The class-object can be returned but this might be confusing for the user... so beter dont do it ;-)

def makeMoreSeedsFromWallet(wallet_id,number_of_Privatekeys_to_be_generated):
    '''Script that takes as input two itegers wallet_id and number_of_privateKeys_to_be_generated.
    The wallet_id must reffer to a generated wallet in the list open_wallets[].
    Prints the specified number of generated privateKeys to console.'''
    for i in range(number_of_Privatekeys_to_be_generated):
        Derivation_Path, privateKey=open_wallets[wallet_id].makeNextPrivKey()
        print('PrivateKey of {} is \'{}\''.format(Derivation_Path, privateKey))

#Some initial print-outs for the user
functions=SHA256PRNG(Passphrase = my_Passphrase, Derivation_coin = my_Derivation_coin, Derivation_wallet = my_Derivation_wallet, Derivation_adress = my_Derivation_adress, Derivation_index = my_Derivation_index+1) #Ist von der refferenzierung her sehr unsauber gelöst, ich weiß... ist mir aber bei einem quick-and-dirty script egal
print(disclaimer)
print('\nDefault BIP44 Derivation-Path is \'{}\''.format(functions.makeDerivationPath()))
print('Default Passphrase is \'{}\''.format(my_Passphrase))

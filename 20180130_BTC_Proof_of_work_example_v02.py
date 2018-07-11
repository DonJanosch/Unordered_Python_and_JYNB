import pandas as pd
import hashlib
import time

def proof_of_work(header, difficulty_bits):
    #Calculate target difficulty
    target = 16 ** (64-difficulty_bits)#(32-difficulty_bits)
    hex_target = '{:02x}'.format(target)
    hex_target = '0'*(64-len(hex_target)) +str(hex_target)
    #print('0'*len(hex_target))
    
    max_nonce = 2 ** 32
    for nonce in range(max_nonce):
        message = str(header)+str(nonce)
        message = message.encode('ASCII')
        hash_result = hashlib.sha256(message).hexdigest()
        
        #Check if result is lower than target
        if int(hash_result,16) < target:
            sizing = int(len(hex_target)-len(hash_result))*' '
            print('Success with nonce: {}'.format(nonce))
            print('Block-Hash:\n{}{} is less than target-difficulty\n{}'.format(sizing,hash_result,hex_target))
            return hash_result,nonce
    print('Failed after {} max attempts'.format(nonce))
    return '',nonce

#Simulation parameters
static_payload = 'Hallo wie geht es dir heute so ? ?'
static = False
static_difficulty = 7

#Declare working variables
nonce = 0
hash_result = ''
prev_hash = []
payload = []
nonces = []
block_hash = []
payload_sentence = static_payload.split()
block_chain = pd.DataFrame()
headers = ['Block_ID','Difficulty_digits','Prev_Hash','Payload','Nonce','Block_Hash','Elapsed Time']

if static:
    max_difficulty_hex = static_difficulty
else:
    max_difficulty_hex = len(payload_sentence)

#Start loop to get proof-of-work
print('### Test of increasing difficultys in proof-of-work consensus ###')
for difficulty_bits in range(max_difficulty_hex):    
    difficulty = 16 ** (difficulty_bits)
    
    if difficulty_bits ==0:
        difficulty_bits_reported = 'not existing (every result is acceptable)'
    elif difficulty_bits ==1:
        difficulty_bits_reported = str(difficulty_bits) + ' leading zero (hexadecimal)'
    else:
        difficulty_bits_reported = str(difficulty_bits) + ' leading zeros (hexadecimal)'
        
    print('\nStarting iteration Nr {}:'.format(difficulty_bits))

    #make a new block which includes the has from the previous block
    if static:
        transactions = static_payload
    else:
        transactions = payload_sentence[difficulty_bits]
    
    payload.append(transactions)
    prev_hash.append(hash_result)
    
    print('Previous-Block-Hash is \'{}\''.format(prev_hash[-1]))
    print('Transaction-Payload is \'{}\''.format(payload[-1]))
    print('Target-Difficulty is {}'.format(difficulty_bits_reported))
    print('Start searching for nonce to get proof-of-work...')
    
    #Checkpoint the current time
    start_time = time.time()
    new_block =  hash_result + transactions

    #Find valid nonce
    hash_result, nonce = proof_of_work(new_block, difficulty_bits)
    nonces.append(nonce)
    block_hash.append(hash_result)

    #checkpoint how long it took to find a result
    end_time = time.time()

    elapsed_time = end_time - start_time
    if elapsed_time < 1:
        elapsed_time*=1000
        elapsed_time_report = '%.4f milliseconds' % elapsed_time
    else:
        elapsed_time_report = '%.4f seconds' % elapsed_time
        
    print('Elapsed Time: {}'.format(elapsed_time_report))
    
    if elapsed_time >0:
        hash_power = int(int(nonce)/elapsed_time)
        print('Hashing Power: {} hashes per second'.format(hash_power))
    data_slice = pd.DataFrame([difficulty_bits,difficulty_bits_reported,prev_hash[-1],transactions,nonce,hash_result,elapsed_time_report],headers)
    block_chain = block_chain.append(data_slice)


print('\n### The resulting blockchain looks like this ###',block_chain)

print('\nAll nonces:')
for i,j in enumerate(nonces):
    print(i,j)

res = pd.DataFrame([prev_hash, payload, nonces, block_hash]).transpose()
res.to_csv('results.csv',index=False, header=False)

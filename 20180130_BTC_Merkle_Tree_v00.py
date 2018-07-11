import hashlib #Required for SHA256 hashing-function

def sha256(message,mencoding='UTF-8'):
    #Accepts a string as message and computes its sha256-hexdigest
    h = hashlib.sha256()
    h.update(message.encode(mencoding))
    return h.hexdigest()

def merkle_tree(leafes, depth = 1):
    #Accepts a list of items and calculates its merkle-tree
    if len(leafes)%2 !=0: #Check if the number of entries in the input list is odd
        print('Found ',len(leafes),' leafes to calculate, reappending the last one to make it an even number')
        leafes.append(leafes[-1]) #If so, reappend the last item, now the number is even
    else:
        print('Found ',len(leafes),' leafes to calculate')
        
    new_list = [] #Make a new list to hold the 'leafes' for the next level

    for i in range(int(len(leafes)/2)): #Loop over the list, since we are always computing two entries at once, just need half the list as loop-count
        hash_input = leafes[2*i]+leafes[2*i+1] #The input for the has function is the next two items in the list just concatenated
        new_list.append(sha256(hash_input)) #Get the hash of the calculated input and append it to the list of new 'leafes'
        print('Appending hash of item ',i,': ',new_list[-1])
    if len(new_list) >1: #Check if the list of new leaves is exaclty 1 entry long, we are done else repeat reccursively
        print('Diving down into next level Nr: ',depth)
        new_list = merkle_tree(new_list, depth=depth+1) #If the list holds more than one entry, repeat the function in a reccursive matter
    return new_list #Once the list has only one entry, return the new_list. Congratulations, you found the root.


test_str = "Wir können hier auch einen ganzen Roman hinschreiben und schauen, was dann passiert. Sollen wir? OK!"

my_ls = list(test_str)

print(my_ls)

res = merkle_tree(my_ls)

print('Found the root: ',res[0])

#-------------------------------------------------------------------------------
# Name:        RNN
# Purpose:     Learning Text
#
# Author:      MacenkaJ
#
# Created:     17.10.2017
# Copyright:   (c) MacenkaJ 2017
# Licence:     none
#-------------------------------------------------------------------------------
import numpy as np
reporting = False

#Read a text file and return a list containing the lines
def readInput(Filename):
    with open('Test.txt','r') as m:
        raw_text = m.readlines()
        return raw_text

#Read a text file and return a list containing all its word
def splitReadInput(Filename):
    with open('Test.txt','r') as m:
        stri = ''
        for line in m:
            stri+=line
        word_stri = stri.split()
        return word_stri

#Digest a list of words or text
def digestSentence(sentence,encoding="utf-8"):
    res = []
    for word in sentence:
        for letter in word:
            res.append((letter))
        res.append(' ')
    return res

#Take a list of words, calculate the unique set and make an array
def createEnumeratedWordVector(WordList):
    word_set = list(set(WordList))
    #enum_set =[(j,i) for i,j in enumerate(word_set)]
    enum_set = word_set
    return enum_set

def createCharLookupTable(CharList):
    lookup_table = {}

#From the consecutive list of characters together with the unique set of characters, generate the input vector list
def createCharacterVector(CharacterList,usedCharSet):
    res = np.zeros([len(CharacterList),len(usedCharSet)],dtype=np.int8)
    n = 0
    for char in CharacterList:
        res[n][usedCharSet.index(char)] = 1
        n+=1
    return res

def returnIndexOfChoice(vector):
    n = 0
    for i in vector:
        if i ==1:
            return(n)
            break
        n+=1

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

def sigmoid_output_to_derivative(output):
    return output*(1-output)

def softmax(w, t = 1.0):
    e = np.exp(np.array(w) / t)
    dist = e / np.sum(e)
    return dist

def softmax_output_to_derivative(output):
    return output*(1-output)

def main():
#INITIALIZE PARAMETERS
    wordcount = 20 #Specify how many words of the original text are to be used
    max_Training_Iterations = 1000 # Specify the maximum training interations for Backpropagation
    alpha = 0.1 #Specify the learning rate
    hidden_dim = 50 #Specify the number of hidden neurons
    #np.random.seed(0) #Specify the seed for Debugging and comparison

#PREPARE THE INPUT INFORMATION TO TRAIN ON
    #First get the array-list of text
    raw_text_lines = splitReadInput('Test.txt')
    #"Digest" the list of text into a list of ascii-letters
    list_of_ascii_characters = digestSentence(raw_text_lines)
    #calculate the used set of characters
    used_ascii_set = createEnumeratedWordVector(list_of_ascii_characters)
    output_dim = len(used_ascii_set) #Specify the number of output neurons
    #The length of the used set of charactes determines the input neuron count
    input_dim = len(used_ascii_set)
    #generate the one hot input vector list. one vector per character.
    input_vector_list = createCharacterVector(list_of_ascii_characters[0:wordcount-1],used_ascii_set)
    #we want to predict the next letter in the sentence, therefore the output list is the inputlist moved by 1
    output_vecot_list = np.vstack((input_vector_list[1:],input_vector_list[0]))

#INITIALIZE THE WEIGHT NETWORK
    #Randomly initialize the weight matrices
    synapse_0 = 2*np.random.random((input_dim,hidden_dim))-1
    synapse_1 = 2*np.random.random((hidden_dim,output_dim))-1
    synapse_h = 2*np.random.random((hidden_dim,hidden_dim))-1
    bh, by = 2*np.random.random((1,hidden_dim))-1, 2*np.random.random((1,output_dim))-1,

    synapse_0_update = np.zeros_like(synapse_0)
    synapse_1_update = np.zeros_like(synapse_1)
    synapse_h_update = np.zeros_like(synapse_h)
    dbh, dby = np.zeros_like(bh), np.zeros_like(by)

    layer_1 = np.zeros((input_vector_list.shape[0],hidden_dim))

    overallError = 0

#FORWARD PROPAGATION
    #Store the previous results of layer_1 as old values
    layer_1_prev = layer_1
    #Forward propagate the input vectors to derive the layer_1 values and add the stored hidden values times theyr weight (the recurrent term)
    layer_1 = sigmoid(np.dot(input_vector_list,synapse_0)+np.dot(layer_1_prev,synapse_h)+bh)
    #Forward propagate the layer_1 values to derive the layer_2 values
    layer_2 = softmax(np.dot(layer_1,synapse_1))

#DETERMINE ERROR
    #Calculate the cross-entropy and update the total error
    layer_2_error = np.multiply(output_vecot_list,-np.log(layer_2)+by)
    for entry in layer_2_error:
        overallError += np.sum(entry)
    #delta_Layer_2
#BACKPROPAGATION

    print(input_vector_list.shape)

    #Some printing for debugging reasons
    if reporting:
        print(np.sum(layer_2))
        print("Input:"+str(input_vector_list.shape))
        print("W:"+str(synapse_0.shape))
        print("Hidden:"+str(layer_1.shape))
        print("Out:"+str(layer_2.shape))
        print('Out_Delta:'+str(output_vecot_list.shape))
        print(list_of_ascii_characters)
        print(len(list_of_ascii_characters))
        print(used_ascii_set)
        print(used_ascii_set.index('"'))
        print(len(used_ascii_set))
        print('Text' + str(len(raw_text_lines)))
        print('Wordset' + str(len(myset)))
        print(input_vector_list)
        print((input_vector_list).shape)
        first_char = returnIndexOfChoice(input_vector_list[0])
        print(first_char)
        print(used_ascii_set[first_char])
        print(len(used_ascii_set))
        print(str(input_vector_list[0]) + " // " + str(output_vecot_list[0]))
    print('Done!')

if __name__ == '__main__':
    main()

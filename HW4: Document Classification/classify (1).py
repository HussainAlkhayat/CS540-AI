import os
import math

"""
Given a directory and a cutoff return a list of word that occrued >= cutoff.
"""
def create_vocabulary(training_directory, cutoff):
    dirs = os.listdir(training_directory)
    Dict = {}
    dir = []
    for i in dirs:
        dir.append(training_directory +i)
    dirList = []
    for i in dir:
        tempDir = os.listdir(i)
        for j in tempDir:
            dirList.append(i +'/'+ j)
    for filename in dirList:
        file = open(filename, "r", encoding='utf-8')
        for word in file:
            correctWord = word.rstrip()
            if correctWord in Dict.keys():
                Dict[correctWord] += 1
            else:
                Dict[correctWord] = 1
        file.close()
    returnList = []
    for word in Dict.keys():
        if Dict[word] >= cutoff:
            returnList.append(word)
    return sorted(returnList)

"""
returns a bag of words corresponding to the vocab and filepath
"""
def create_bow(vocab, filepath):
    file = open(filepath, "r", encoding='utf-8')
    Dict = {}
    for word in file:
        correctWord = word.rstrip()
        if correctWord in Dict.keys():
            Dict[correctWord] += 1
        else:
            Dict[correctWord] = 1
    returnedDict = {}
    for word in Dict.keys():
        if word in vocab:
            returnedDict[word] = Dict[word]
        else:
            if None in returnedDict.keys():
                returnedDict[None] += 1
            else:
                returnedDict[None] = 1
    file.close()
    return returnedDict

"""
create and return training set (bag of words Python dictionary + label) from the files in a training directory
"""
def load_training_data(vocab, directory):
    dirs = os.listdir(directory)
    ListDict = []
    dir = []
    for i in dirs:
        dir.append(directory + i)
    dirList = []
    for i in dir:
        tempDir = os.listdir(i)
        for j in tempDir:
            dirList.append(i + '/' + j)
    for file in dirList:
        Label = ''
        if '2016' in file:
            Label = '2016'
        else:
            Label = '2020'
        insertedDict = {}
        insertedDict['label'] = Label
        insertedDict['bow'] = create_bow(vocab, file)
        ListDict.append(insertedDict)
    return ListDict

"""
given a training set, estimate and return the prior probability P(label) of each label
"""
def prior(training_data, label_list):
    Dict = {}
    for i in label_list:
        Dict[i] = 0
    for data in training_data:
        for label in label_list:
            if label == data['label']:
                Dict[label] += 1
    numFiles = len(training_data)
    for label in label_list:
        Dict[label] = math.log(Dict[label]+1)-math.log(numFiles+2)
    return Dict

"""
given a training set and a vocabulary, estimate and return the class conditional distribution
"""
def p_word_given_label(vocab, training_data, label):
    Dict = {}
    sizeOfLabel = 0

    for data in training_data:
        if data['label'] == label:
            for word in data['bow'].keys():
                sizeOfLabel += data['bow'][word]
                if word in Dict.keys():
                    Dict[word] += data['bow'][word]
                else:
                    Dict[word] = data['bow'][word]

    sizeOfVocab = len(vocab)
    returnedDict = {}
    for word in vocab:
        if word not in Dict.keys():
            Dict[word] = 0
        returnedDict[word] = math.log(Dict[word]+1)-math.log(sizeOfLabel+sizeOfVocab+1)
    if None in Dict.keys():
        returnedDict[None] = math.log(Dict[None] + 1) - math.log(sizeOfLabel + sizeOfVocab + 1)
    else:
        Dict[None] = 0
        returnedDict[None] = math.log(Dict[None] + 1) - math.log(sizeOfLabel + sizeOfVocab + 1)
    return returnedDict

"""
load the training data, estimate the prior distribution P(label) and class conditional distributions P(word|label), return the trained model
"""
def train(training_directory, cutoff):
    vocab = create_vocabulary(training_directory, cutoff)
    Dict = {}
    Dict['vocabulary'] = vocab
    training_data = load_training_data(vocab, training_directory)
    logprior = prior(training_data, ['2020', '2016'])
    Dict['log prior'] = logprior
    Dict['log p(w|y=2020)'] = p_word_given_label(vocab,training_data, '2020')
    Dict['log p(w|y=2016)'] = p_word_given_label(vocab,training_data, '2016')
    return Dict
"""
given a trained model, predict the label for the test document (see below for implementation details including the return value)
"""
def classify(model, filepath):
    sum2020 = 0
    file = open(filepath, "r", encoding='utf-8' )
    sum2016 = 0
    for word in file:
        word = word.rstrip()
        if word in model['log p(w|y=2020)'].keys():
            sum2020 += model['log p(w|y=2020)'][word]
        else:
            sum2020 += model['log p(w|y=2020)'][None]
        if word in model['log p(w|y=2016)'].keys():
            sum2016 += model['log p(w|y=2016)'][word]
        else:
            sum2016 += model['log p(w|y=2016)'][None]
    prob2020 = model['log prior']['2020']+sum2020
    prob2016 = model['log prior']['2016']+sum2016
    predicted = None
    if prob2020 > prob2016:
        predicted = '2020'
    else:
        predicted = '2016'
    Dict = {'log p(y=2020|x)': prob2020, 'log p(y=2016|x)': prob2016, 'predicted y': predicted}
    return Dict


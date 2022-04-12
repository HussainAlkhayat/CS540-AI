from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    loaded_data = np.load(filename)
    loaded_data = np.reshape(loaded_data,(2000, 784))
    centeredData = loaded_data - np.mean(loaded_data, axis=0)
    return centeredData



def get_covariance(dataset):
    return np.cov(np.transpose(dataset))

def get_eig(S, m):
    eignVal,eignVec = eigh(S)
    temp = eignVal.argsort()[::-1]
    eignVal = eignVal[temp]
    eignVec = eignVec[:, temp]

    returnDiag = np.diag(eignVal[:m])
    returnVec = []
    for i in range(m):
        returnVec.append(eignVec.transpose()[i])
    returnVec = np.array(returnVec)
    returnVec= returnVec.transpose()

    return returnDiag,returnVec



def get_eig_perc(S, perc):
    eignVal, eignVec = eigh(S)
    temp = eignVal.argsort()[::-1]
    eignVal = eignVal[temp]
    eignVec = eignVec[:, temp]
    totalVal = np.sum(eignVal)
    ThresholdNotFound = True
    i = 0
    Threshold =-1;
    while ThresholdNotFound:
        if i == len(S):
            break
        if eignVal[i]/totalVal > perc:
            Threshold +=1
        else:
            returnDiag = np.diag(eignVal[:Threshold+1])
            returnVec = []
            for j in range(Threshold+1):
                returnVec.append(eignVec.transpose()[j])
            returnVec = np.array(returnVec)
            returnVec = returnVec.transpose()
            return returnDiag, returnVec
        i+=1
    returnDiag = np.diag(eignVal)
    returnVec = []
    for j in range(Threshold+1):
        returnVec.append(eignVec.transpose()[j])
    returnVec = np.array(returnVec)
    returnVec = returnVec.transpose()
    return returnDiag, returnVec


def project_image(image, U):
    transU = U.transpose()
    m = len(transU)
    array = []
    for i in range(m):

        A = np.dot(transU[i].transpose(),image)
        array.append(np.dot(A, transU[i]))
    array = np.array(array)
    array = array.transpose()
    newArray = np.zeros(len(array),)
    i = 0
    j = 0
    while i < len(array):
        while j < len(array[i]):
            newArray[i] += array[i][j]
            j +=1
        j = 0
        i +=1
    return newArray

def display_image(orig, proj):
    matrixProj = np.zeros((28,28))
    matrixOrig = np.zeros((28,28))
    counter = 0
    for i in range(28):
        for j in range(28):
            matrixProj[i][j] = proj[counter]
            matrixOrig[i][j] = orig[counter]
            counter +=1
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False, figsize=(9,3))
    bar1 = ax1.imshow(matrixOrig, aspect='equal', cmap='gray')
    ax1.set_title('Original')
    f.colorbar(bar1, ax=ax1)
    bar2 = ax2.imshow(matrixProj, aspect='equal', cmap='gray')
    ax2.set_title('Projection')
    f.colorbar(bar2, ax=ax2)
    plt.show()

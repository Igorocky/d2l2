import random
import torch

class DataLoader:
    def __init__(self,rawText):
        self.text = rawText.lower().replace('\n', ' ')
        chars = sorted(set(self.text))
        self.char2int = {c:i for i,c in enumerate(chars)}
        self.numOfTokens = len(self.char2int)
        self.textInt = [self.char2int[ch] for ch in self.text]
        self.int2char = {i:c for c,i in self.char2int.items()}

    def getSamples(self, ctxLen, trSamplNum=10, valSampleNum=None):
        # random.seed(123)
        valSampleNum = int(trSamplNum*0.3) if valSampleNum == None else valSampleNum
        idxs = random.sample(range(0,len(self.text)-ctxLen), trSamplNum+valSampleNum)
        X,Y = [],[]
        for i in idxs:
            X.append(self.textInt[i:i+ctxLen])
            Y.append(self.textInt[i+1:i+1+ctxLen])
        Xtr = torch.tensor(X[:trSamplNum])
        Ytr = torch.tensor(Y[:trSamplNum])
        Xval = torch.tensor(X[trSamplNum:])
        Yval = torch.tensor(Y[trSamplNum:])
        return Xtr, Ytr, Xval, Yval
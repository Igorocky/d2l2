import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self,numOfTokens,ctxLen,embSize,char2int,int2char):
        super().__init__()
        self.numOfTokens = numOfTokens
        self.ctxLen = ctxLen
        self.embSize = embSize
        self.char2int = char2int
        self.int2char = int2char
        self.emb = nn.Embedding(numOfTokens,embSize)
        hidDim = 1000
        self.lin1 = nn.Linear(ctxLen*embSize,hidDim)
        self.lin2 = nn.Linear(hidDim,hidDim)
        self.lin3 = nn.Linear(hidDim,hidDim)
        self.lin4 = nn.Linear(hidDim,hidDim)
        self.lin5 = nn.Linear(hidDim,hidDim)
        self.lin6 = nn.Linear(hidDim,hidDim)
        self.lin7 = nn.Linear(hidDim,hidDim)
        self.lin8 = nn.Linear(hidDim,hidDim)
        self.lin9 = nn.Linear(hidDim,ctxLen*numOfTokens)

    def forward(self,x):
        # x: B,T
        x = self.emb(x).view(-1,self.ctxLen*self.embSize)
        # x: B,T,C

        x = F.leaky_relu(self.lin1(x))

        x = x + F.leaky_relu(self.lin2(x))
        x = x + F.leaky_relu(self.lin3(x))
        x = x + F.leaky_relu(self.lin4(x))
        x = x + F.leaky_relu(self.lin5(x))
        x = x + F.leaky_relu(self.lin6(x))
        x = x + F.leaky_relu(self.lin7(x))
        x = x + F.leaky_relu(self.lin8(x))

        x = self.lin9(x)
        
        x = x.view(-1,self.ctxLen,self.numOfTokens)
        # x: B,T,C
        return x

    def calcLoss(self,X,Y):
        Yp = self(X)
        logits = Yp.view(-1,self.numOfTokens)
        targets = Y.view(-1)
        return F.cross_entropy(logits,targets)
    
    @torch.no_grad()
    def generate(self,ctx,resLen):
        if len(ctx) < self.ctxLen:
            ctx = ' '*(self.ctxLen-len(ctx)) + ctx
        elif len(ctx) > self.ctxLen:
            ctx = ctx[-self.ctxLen:]
        res = []
        while len(res) < resLen:
            x = torch.tensor([self.char2int[ch] for ch in ctx]).unsqueeze(0)
            logits = self(x)[0,-1]
            probs = F.softmax(logits,dim=0)
            nextToken = torch.multinomial(probs, 1)
            nextChar = self.int2char[nextToken[0].item()]
            res.append(nextChar)
            ctx = ctx[1:] + nextChar
        return ''.join(res)
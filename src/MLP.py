import torch
import torch.nn as nn
import torch.nn.functional as F

class MlpPredictor(nn.Module):
    def __init__(self,numOfTokens,ctxLen,embSize,char2int,int2char):
        super().__init__()
        self.numOfTokens = numOfTokens
        self.ctxLen = ctxLen
        self.embSize = embSize
        self.char2int = char2int
        self.int2char = int2char
        self.emb = nn.Embedding(numOfTokens,embSize)
        hidDim1 = 1000
        hidDim2 = 1000
        hidDim3 = 1000
        hidDim4 = 1000
        hidDim5 = 1000
        hidDim6 = 1000
        hidDim7 = 1000
        hidDim8 = 1000
        self.lin1 = nn.Linear(ctxLen*embSize,hidDim1)
        self.lin2 = nn.Linear(hidDim1,hidDim2)
        self.lin3 = nn.Linear(hidDim2,hidDim3)
        self.lin4 = nn.Linear(hidDim3,hidDim4)
        self.lin5 = nn.Linear(hidDim4,hidDim5)
        self.lin6 = nn.Linear(hidDim5,hidDim6)
        self.lin7 = nn.Linear(hidDim6,hidDim7)
        self.lin8 = nn.Linear(hidDim7,hidDim8)
        self.lin9 = nn.Linear(hidDim8,ctxLen*numOfTokens)

    def forward(self,x):
        x = self.emb(x).view(-1,self.ctxLen*self.embSize)

        x = self.lin1(x)
        x = F.leaky_relu(x)
        r1 = x

        x = self.lin2(x)
        x = F.leaky_relu(x)
        r2 = x

        x = self.lin3(x+r1)
        x = F.leaky_relu(x)
        r3 = x

        x = self.lin4(x+r2)
        x = F.leaky_relu(x)
        r4 = x

        x = self.lin5(x+r3)
        x = F.leaky_relu(x)
        r5 = x

        x = self.lin6(x+r4)
        x = F.leaky_relu(x)
        r6 = x

        x = self.lin7(x+r5)
        x = F.leaky_relu(x)
        r7 = x

        x = self.lin8(x+r6)
        x = F.leaky_relu(x)

        x = self.lin9(x+r7)
        
        x = x.view(-1,self.ctxLen,self.numOfTokens)
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
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

    def forward(self,x,targets=None):
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
        
        y = x.view(-1,self.ctxLen,self.numOfTokens)
        # x: B,T,C

        if targets == None:
            loss = None
        else:
            loss = F.cross_entropy(y.view(-1,self.numOfTokens),targets.view(-1), ignore_index=-1)
        return y, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0):
        for _ in range(max_new_tokens):
            ctx = idx if idx.size(1) <= self.ctxLen else idx[:, -self.ctxLen:]
            logits, _ = self(ctx)
            logits = logits[:, -1, :] / temperature
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)

        return idx
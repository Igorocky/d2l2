import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# https://github.com/karpathy/nanoGPT.git

class SelfAttention(nn.Module):
    def __init__(self, embLen, headCnt, bias, dropout, ctxLen):
        super().__init__()
        self.embLen = embLen
        self.headCnt = headCnt
        assert embLen % headCnt == 0
        self.headSize = embLen // headCnt
        self.bias = bias
        self.dropout = dropout
        self.ctxLen = ctxLen
        self.attScale = 1.0 / math.sqrt(self.headSize)
        self.wQkv = nn.Linear(embLen, 3 * embLen, bias=bias)
        self.wOut = nn.Linear(embLen, embLen, bias=bias)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer(
            "mask",
            (torch.tril(torch.ones(ctxLen, ctxLen)) == 0).view(1, 1, ctxLen, ctxLen)
        )

    def forward(self, x):
        B, T, C = x.size()

        q, k, v = self.wQkv(x).split(self.embLen, dim=2)
        q = q.view(B, T, self.headCnt, self.headSize).transpose(1, 2)  # (B, hn, T, hs)
        k = k.view(B, T, self.headCnt, self.headSize).transpose(1, 2)  # (B, hn, T, hs)
        v = v.view(B, T, self.headCnt, self.headSize).transpose(1, 2)  # (B, hn, T, hs)

        att = (q @ k.transpose(-2, -1)) * self.attScale
        att = att.masked_fill(self.mask[:, :, :T, :T], float('-inf'))
        att = F.softmax(att, dim=-1)
        att = self.dropout(att)

        y = att @ v  # (B, hn, T, T) x (B, hn, T, hs) -> (B, hn, T, hs)
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.dropout(self.wOut(y))
        return y


class FeedForward(nn.Module):

    def __init__(self, embLen, bias, dropout):
        super().__init__()
        self.lin1 = nn.Linear(embLen, 4 * embLen, bias=bias)
        self.gelu = nn.GELU()
        self.lin2 = nn.Linear(4 * embLen, embLen, bias=bias)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.lin1(x)
        x = self.gelu(x)
        x = self.lin2(x)
        x = self.dropout(x)
        return x


class Block(nn.Module):

    def __init__(self, embLen, headCnt, bias, dropout, ctxLen):
        super().__init__()
        self.ln1 = nn.LayerNorm(embLen, bias=bias)
        self.attn = SelfAttention(embLen, headCnt, bias, dropout, ctxLen)
        self.ln2 = nn.LayerNorm(embLen, bias=bias)
        self.ff = FeedForward(embLen, bias, dropout)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x


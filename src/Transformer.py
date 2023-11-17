import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# https://github.com/karpathy/nanoGPT.git

class SelfAttention(nn.Module):
    def __init__(self, embLen, headCnt, bias, dropout, maxCtxLen):
        super().__init__()
        self.embLen = embLen
        self.headCnt = headCnt
        assert embLen % headCnt == 0
        self.headSize = embLen // headCnt
        self.bias = bias
        self.dropout = dropout
        self.maxCtxLen = maxCtxLen
        self.attScale = 1.0 / math.sqrt(self.headSize)
        self.wQkv = nn.Linear(embLen, 3 * embLen, bias=bias)
        self.wOut = nn.Linear(embLen, embLen, bias=bias)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer(
            "mask",
            (torch.tril(torch.ones(maxCtxLen, maxCtxLen)) == 0).view(1, 1, maxCtxLen, maxCtxLen)
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

    def __init__(self, embLen, headCnt, bias, dropout, maxCtxLen):
        super().__init__()
        self.ln1 = nn.LayerNorm(embLen, bias=bias)
        self.attn = SelfAttention(embLen, headCnt, bias, dropout, maxCtxLen)
        self.ln2 = nn.LayerNorm(embLen, bias=bias)
        self.ff = FeedForward(embLen, bias, dropout)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x


class Transformer(nn.Module):
    def __init__(self, tokenCnt, embLen, headCnt, layerCnt, bias, dropout, maxCtxLen):
        super().__init__()
        self.tokenCnt = tokenCnt
        self.embLen = embLen
        self.headCnt = headCnt
        self.bias = bias
        self.dropout = dropout
        self.maxCtxLen = maxCtxLen
        self.wte = nn.Embedding(tokenCnt, embLen)
        self.wpe = nn.Embedding(maxCtxLen, embLen)
        self.drop = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([
            Block(embLen=embLen, headCnt=headCnt, bias=bias, dropout=dropout, maxCtxLen=maxCtxLen)
            for _ in range(layerCnt)
        ])
        self.lnOut = nn.LayerNorm(embLen, bias=bias)
        self.wOut = nn.Linear(embLen, tokenCnt, bias=False)

        self.apply(self._init_weights)
        for pn, p in self.named_parameters():
            # print(f'{pn=}')
            if pn.endswith('lin2.weight'):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * headCnt))

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        B, T = idx.size()
        assert T <= self.maxCtxLen, f"Cannot forward sequence of length {T}, maxCtxLen is {self.maxCtxLen}"
        pos = torch.arange(0, T, dtype=torch.long)

        # forward the GPT model itself
        tok_emb = self.wte(idx)  # (B, T, C)
        pos_emb = self.wpe(pos)  # (B, T, C)
        x = self.drop(tok_emb + pos_emb)
        for block in self.blocks:
            x = block(x)
        x = self.lnOut(x)

        if targets is not None:
            # if we are given some desired targets also calculate the loss
            logits = self.wOut(x)
            loss = F.cross_entropy(logits.view(-1, self.tokenCnt), targets.view(-1), ignore_index=-1)
        else:
            # inference-time mini-optimization: only forward the wOut on the very last position
            logits = self.wOut(x[:, [-1], :])  # note: using list [-1] to preserve the time dim
            loss = None

        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0):
        for _ in range(max_new_tokens):
            ctx = idx if idx.size(1) <= self.maxCtxLen else idx[:, -self.maxCtxLen:]
            logits, _ = self(ctx)
            logits = logits[:, -1, :] / temperature
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)

        return idx

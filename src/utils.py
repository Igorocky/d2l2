import matplotlib.pyplot as plt
import torch
import random

def showParamsStats(model, layerNameFilter=None, figsize=(20,10)):
    params = [
        (pName, pValue)
        for pName, pValue in model.named_parameters()
        if layerNameFilter == None or layerNameFilter.match(pName)
    ]
    _,axs = plt.subplots(len(params),1, figsize=figsize)
    for i, (pName, pValue) in enumerate(params):
        hy,hx = torch.histogram(pValue, density=False)
        axs[i].plot(hx[:-1].detach(),hy.detach(), label=f'{pName}({pValue.numel():,}) mean:{pValue.mean():.4f}, std:{pValue.std():.4f}')
        # axs[i].set_title(f'{pName}({pValue.nelement()}) mean:{pValue.mean():.4f}, std:{pValue.std():.4f},')
        axs[i].legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.tight_layout()

def trainLoop(epochNum,batchesPerEpoch,batchSize,model,optimizer,dataLoader):
    for epoch in range(epochNum):
        Xtr,Ytr,Xval,Yval = dataLoader.getSamples(ctxLen=model.ctxLen, trSamplNum=batchesPerEpoch*batchSize)
        batchIdxs = [i for i in range(len(Xtr))[::batchSize]]
        random.shuffle(batchIdxs)
        for batch_begin in batchIdxs:
            batch_end = batch_begin+batchSize
            Xb = Xtr[batch_begin:batch_end]
            Yb = Ytr[batch_begin:batch_end]
            loss = model.calcLoss(Xb,Yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            trLoss = model.calcLoss(Xtr,Ytr)
            valLoss = model.calcLoss(Xval,Yval)
            print(f'epoch:{epoch}, trLoss={trLoss.item():.4f}, valLoss={valLoss.item():.4f}')
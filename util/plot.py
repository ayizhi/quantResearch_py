#coding utf-8
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import db




def plotCurrentMeanStd(tickerId,days_rang=200):
    df = db.get_current_mean_std_df(tickerId,days_rang)
    cur = df['close']
    theMin = cur.min();
    theMax = cur.max();
    mean_60 = df['ma_60']
    emwa_60 = df['ewma_60']
    std_60 = df['std_60']

    plt.plot(cur,'r',lw=0.75,linestyle='-',label='cur')
    plt.plot(std_60,'p',lw=0.75,linestyle='-',label='std_60')
    plt.plot(mean_60,'b',lw=0.75,linestyle='-',label='mean_60')
    plt.plot(emwa_60,'g',lw=0.75,linestyle='-',label='emwa_60')
    plt.ylim(float(theMin) * 0.9, float(theMax) * 1.1)
    
    plt.legend(loc=4,prop={'size':2})
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.grid(True)
    
    plt.show()



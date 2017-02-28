#coding utf-8
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import db

db.get_current_mean_std_df('DMO')


def plotCurrentMeanStd(days_rang): 
    fig  = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(y_test,'r',lw=0.75,linestyle='-',label='realY')
    ax.plot(pred_test,'b',lw=0.75,linestyle='-',label='predY')
    plt.legend(loc=2,prop={'size':9})
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    plt.grid(True)
    plt.show()
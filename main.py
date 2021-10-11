import ffn
import  matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

import seaborn as sns
import numpy as np

def plot(dataset):
    
    plt.figure(figsize=(8,4), dpi=150)
    plt.plot(dataset.close, color='green')
    plt.xlabel("Tempo")
    plt.ylabel("Prezzi")
    plt.title("Chiusure - AAPL daily")
    plt.grid(True)
    plt.show()

def plot_gaus(dataset_perc):
    plt.figure(figsize=(10,5), dpi=150)
    sns.distplot(dataset_perc.avgprice, bins=200, color="green", label='AVG Price Daily')
    sns.distplot(dataset_perc.medprice, bins=200, color="red", label='MedPrice Daily')
    sns.distplot(dataset_perc.avgprice, bins=200, color="blue", label='MedBodyPrice Daily')
    plt.xlabel("AvgPrice")
    plt.ylabel("Numero Campioni")
    plt.title("Distribuzione delle variazioni percentuali dei prezzi")
    plt.legend()
    plt.show()

def plot_heat(dataset_perc):
    plt.figure(figsize=(8,6), dpi=110)
    sns.heatmap(dataset_perc.iloc[:,:-2].corr(), cmap="RdYlGn", linecolor="white", linewidth=0.1, annot=True)
    plt.show()

def plot_heat_2(memory_avg):
    plt.figure(figsize=(8,6), dpi=110)
    sns.heatmap(memory_avg.corr(), cmap="RdYlGn", linecolor="white", linewidth=0.1, annot=True)
    plt.show()

def main():
    dataset = ffn.get('AAPL:Open,aapl:High,aapl:Low,aapl:Close',start='2007-01-01', end='2019-09-22')
    dataset.columns = ["open","high","low","close"]
    dataset = dataset.apply(lambda x: round(x,2))
    dataset["avgprice"] = dataset.mean(axis=1)
    dataset["medprice"] = dataset.open + (dataset.high - dataset.low) /2
    dataset["medbodyprice"] = dataset.open + abs(dataset.open - dataset.close) /2
    dataset["body"] = dataset.close-dataset.open
    dataset["range"] = dataset.high - dataset.low

    dataset_perc = dataset.copy().pct_change().dropna() * 100
    memory_avg= dataset_perc.copy()
    #numero_correlazioni = 10
    #for i in range(1,numero_correlazioni+1):
        #nome_colonna = "avgprice_"+str(i)
        #memory_avg[nome_colonna] = memory_avg.avgprice.shift(i)
    
    #memory_avg.drop(["open","high","low","close","medprice","medbodyprice","body","range"],axis=1,inplace=True)
    #memory_avg.dropna(inplace=True)

    threshold_low = 0
    threshold_high = 0
    memory_avg["control"] = np.where((memory_avg.avgprice.shift(1) >= threshold_low) & (memory_avg.avgprice >= threshold_high),1,0)

    total = memory_avg[(memory_avg.avgprice >= threshold_low)].avgprice.count()
    verified = memory_avg.control.sum()
    perc = verified / total *100
    print(round(perc,2))


    #print(memory_avg.head(10))


    #print(dataset_perc.describe([0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99]))

    #print(dataset.head(10))

    #plot(dataset)

    #plot_gaus(dataset_perc)
    #plot_heat(dataset_perc)
    #plot_heat_2(memory_avg)
    #print(memory_avg.head(10))

if __name__ == '__main__':
    main()

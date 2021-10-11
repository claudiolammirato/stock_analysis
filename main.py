import ffn

dataset = ffn.get('aapl:Open,aapl:High,aapl:Low,aapl:Close',start='2007-01-01', end='2019-09-22')
dataset.columns = ["open","high","low","close"]
dataset = dataset.apply(lambda x: round(x,2))
dataset["avgprice"] = dataset.mean(axis=1)
dataset["medprice"] = dataset.open + (dataset.high - dataset.low) /2
dataset["medbodyprice"] = dataset.open + abs(dataset.open - dataset.close) /2
dataset["body"] = dataset.close-dataset.open
dataset["range"] = dataset.high - dataset.low
print(dataset.head(10))

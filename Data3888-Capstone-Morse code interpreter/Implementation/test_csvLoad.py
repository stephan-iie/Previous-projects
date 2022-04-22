from threading import Timer
import time
import pandas as pd
from catch_for_main_loop import streaming_classifier
import numpy as np

## simulates SpikerBox streaming in the data every 1 second, writing over
## the old data witha new data vector

def SimulateIn(csv):
    df = pd.read_csv(csv,sep=',',header=None,names=range(9999))
    data = df.values.flatten()
    a,b=streaming_classifier(20000,data,'nice')
    return b
    # for i in range(0,len(df)):
    #     data = df.iloc[i,:]
    #     #print(data)
    #     a,b = streaming_classifier(20000,data,'nice')
    #     print(b)
    #     print('here I am')
    #     time.sleep(1)

output = SimulateIn('output.csv')#.start()
print(output)


# a,b=streaming_classifier(20000,data,model)
# print(b)

######
#USAGE
######

# data = SimulateIn('output.csv').start()
# print(data)

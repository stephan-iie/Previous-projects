

from scipy.io import wavfile
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split


pathlist_1 = ["/content/drive/MyDrive/Data3888/blinking/blink_olli_bot_v1.wav",
        "/content/drive/MyDrive/Data3888/blinking/blinking_jack_top_v1.wav",
        "/content/drive/MyDrive/Data3888/blinking/blinking_jack_top_v2.wav",
        "/content/drive/MyDrive/Data3888/blinking/blinking_ollie_top_v1.wav"]
pathlist_2 = ["/content/drive/MyDrive/Data3888/blinking/longblinkinh_ollie_bot_v2.wav",
        "/content/drive/MyDrive/Data3888/blinking/longblink_olli_top_v1.wav",
        "/content/drive/MyDrive/Data3888/blinking/longblink_jack_top_v1.wav"]
pathlist_3 = ["/content/drive/MyDrive/Data3888/double_blink/doubleblink_jack_top_v1.wav",
        "/content/drive/MyDrive/Data3888/double_blink/doublelink_jack_bot_v1.wav",
        "/content/drive/MyDrive/Data3888/double_blink/doublelink_jack_bot_v2.wav",
        "/content/drive/MyDrive/Data3888/double_blink/doublelink_jack_top_v2.wav"]


def streaming_classifier_Noraml(samplerate,Y):

    xtime = np.array(range(0, len(Y)))/int(samplerate*0.5)
    window_size = int(samplerate*0.5)
    increment = int(window_size/3)
    thresh = 150


    predicted_labels = []  # stores predicted
    lower_interval = 0  # used to increment window
    max_time = int(max(xtime) * int(samplerate*0.5))

    predicted = []
    # initialing signal vector
    counter = 0
    is_event = []


    while (max_time > lower_interval + window_size):

        if max_time < lower_interval + window_size + increment:
            upper_interval = max_time
        else:
            upper_interval = lower_interval + window_size

        interval = Y[lower_interval:upper_interval]
        xinterval = xtime[lower_interval:upper_interval]  # gets corresponding time

        zerocrossing = (np.diff(np.sign(interval)) != 0).sum()
        Mean_value = np.mean(interval)
        standarddeviation = round(np.std(interval),3)
        abssum = sum(map(abs, interval))/10000
        #print(abssum,standarddeviation,counter,lower_interval,upper_interval)

        # If it is a event, recored it as True and add one to counter
        if abssum > thresh and upper_interval != max_time:
            is_event.append(True)
            counter = counter + 1
            lower_interval = lower_interval + increment

        # If ends, and the counter is greater than 0 which means it has event not finished
        elif upper_interval == max_time and counter > 0:
            begin_time = lower_interval - increment * counter
            end_time = max_time
            predicted.append([begin_time,end_time,end_time-begin_time,Y[begin_time:end_time]])
            #print(begin_time,end_time)
            lower_interval = lower_interval + increment

        # If it is not a event, back to its previous one and adjust whether its previous is event or not
        else:
            is_event.append(False)

            if len(is_event) == 1:
                lower_interval = lower_interval + increment
            elif is_event[-2] == True:
                begin_time = lower_interval - increment * counter
                end_time = lower_interval - increment + window_size

                predicted.append([begin_time,end_time,end_time-begin_time,Y[begin_time:end_time]])
                #print(begin_time,end_time,end_time-begin_time)
                lower_interval = end_time
            else:
                lower_interval = lower_interval + increment
            counter = 0

        
    df = pd.DataFrame(predicted,columns=['begin','end','Long','Values'])
    return df
    #return predicted,eventtime

"""## Noraml Blink test"""


Long_blink=[]

Normal_blink=[]
for i in pathlist_1:
  samplerate, Y = wavfile.read(i)
  result = streaming_classifier_Noraml(samplerate,Y)
  Normal_blink.append(result)
Normal_blink = pd.concat(Normal_blink)
Normal_blink['Type'] = "Normal"

for i in pathlist_1:
  samplerate, Y = wavfile.read(i)
  xtime = np.array(range(0, len(Y)))/samplerate
  #plt.figure(figsize=(20,5))
  #plt.plot(xtime, Y)
  result = streaming_classifier_Noraml(samplerate,Y)
  for i in range(0,len(result)):
    begin = int(result.iloc[i].at['begin'])
    end = int(result.iloc[i].at['end'])
    Y = result.iloc[i].at['Values']

    xtime = np.array(range(begin, begin+len(Y)))/samplerate
    #plt.plot(xtime, Y, color='red')

"""## Long Blink test"""


for i in pathlist_2:
  samplerate, Y = wavfile.read(i)
  result = streaming_classifier_Noraml(samplerate,Y)
  Long_blink.append(result)
Long_blink = pd.concat(Long_blink)
Long_blink['Type'] = "Long"

for i in pathlist_2:
  samplerate, Y = wavfile.read(i)
  xtime = np.array(range(0, len(Y)))/samplerate
  #plt.figure(figsize=(20,5))
  #plt.plot(xtime, Y)
  result = streaming_classifier_Noraml(samplerate,Y)
  for i in range(0,len(result)):
    begin = int(result.iloc[i].at['begin'])
    end = int(result.iloc[i].at['end'])
    Y = result.iloc[i].at['Values']

    xtime = np.array(range(begin, begin+len(Y)))/samplerate
   # plt.plot(xtime, Y, color='red')

"""## Double test"""


Double_blink=[]
for i in pathlist_3:
  samplerate, Y = wavfile.read(i)
  result = streaming_classifier_Noraml(samplerate,Y)
  Double_blink.append(result)
Double_blink = pd.concat(Double_blink)
Double_blink['Type'] = "Double"

for i in pathlist_3:
  samplerate, Y = wavfile.read(i)
  xtime = np.array(range(0, len(Y)))/samplerate
 # plt.figure(figsize=(20,7))
 # plt.plot(xtime, Y)
  result = streaming_classifier_Noraml(samplerate,Y)
  for i in range(0,len(result)):
    begin = int(result.iloc[i].at['begin'])
    end = int(result.iloc[i].at['end'])
    Y = result.iloc[i].at['Values']

    xtime = np.array(range(begin, begin+len(Y)))/samplerate
  #  plt.plot(xtime, Y, color='red')

"""# Combine table and Features

## Catch22
"""

EventFrame = pd.concat([Normal_blink,Long_blink,Double_blink], ignore_index=True)
flawed=EventFrame.index[[0,26, 35, 45, 46, 48, 54, 72, 75, 147, 148, 149, 150, 151, 152, 153, 154, 161, 162, 165, 166, 167,168, 169, 170, 171, 172, 174, 175, 176, 177, 178, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 198, 200, 201,202, 203, 204, 206, 213, 214,221, 222, 231, 280]]
EventFrame=EventFrame.drop(flawed)
EventFrame

"""## Peak and Withs"""

import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def peaks(y): #gives the number of peaks
  y=np.array(y)
  peaks, properties = find_peaks(abs(y),height=1700, width=200)
  return sum(np.diff(peaks)>400)+1

def betweenlastpeaks(y): #gives diff in indexes of first and last peak
  y=np.array(y)
  peaks, properties = find_peaks(abs(y),height=1700, width=200)
  if len(peaks)==0:
    return 0
  return peaks[-1]-peaks[0]

col = [
    'Type',
    'Len_between_peaks',
    'Peaks',
    'DN_HistogramMode_5',
    'DN_HistogramMode_10',
    'CO_f1ecac',
    'CO_FirstMin_ac',
    'CO_HistogramAMI_even_2_5',
    'CO_trev_1_num',
    'MD_hrv_classic_pnn40',
    'SB_BinaryStats_mean_longstretch1',
    'SB_TransitionMatrix_3ac_sumdiagcov',
    'PD_PeriodicityWang_th0_01',
    'CO_Embed2_Dist_tau_d_expfit_meandiff',
    'IN_AutoMutualInfoStats_40_gaussian_fmmi',
    'FC_LocalSimple_mean1_tauresrat',
    'DN_OutlierInclude_p_001_mdrmd',
    'DN_OutlierInclude_n_001_mdrmd',
    'SP_Summaries_welch_rect_area_5_1',
    'SB_BinaryStats_diff_longstretch0',
    'SB_MotifThree_quantile_hh',
    'SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1',
    'SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1',
    'SP_Summaries_welch_rect_centroid',
    'FC_LocalSimple_mean3_stderr']
df=pd.DataFrame(columns= col)

from catch22 import catch22_all


for i in range(0,len(EventFrame)):
  current_row = EventFrame[i:i+1]
  current_type = current_row['Type'].to_string().split()[1]
  Y = sum(current_row["Values"]).tolist()
  t = catch22_all(Y)
  features = t["values"]
  features.insert(0,current_type)
  features.insert(1,peaks(Y))
  features.insert(1,betweenlastpeaks(Y))
  df.loc[i]=features
df

"""# Modles Selection"""

from sklearn.model_selection import train_test_split 
#from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

"""##Random Forest"""

#this is from a feature selection algorihtmn, ive harcoded it since it might change and only need this for the main loop to trina
selected_feat=['Len_between_peaks', 'Peaks', 'CO_f1ecac', 'CO_FirstMin_ac',
       'SB_TransitionMatrix_3ac_sumdiagcov',
       'SP_Summaries_welch_rect_area_5_1',
       'SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1',
       'SP_Summaries_welch_rect_centroid']
rfselected=df[selected_feat]
rfselected #note- higher than before!
y= df['Type']

import delayed
from sklearn.ensemble import RandomForestClassifier
RDF = RandomForestClassifier(n_estimators=100)

x_train,x_test,y_train,y_test = train_test_split(rfselected,y,test_size=0.2,random_state=1)
model = RandomForestClassifier(n_estimators=100).fit(x_train, y_train)

print("Training set score: {:.3f}".format(model.score(x_train, y_train)))
print("Test set score: {:.3f}".format(model.score(x_test, y_test)))

"""# Fuction rewrite"""

from scipy.io import wavfile
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
import catch22



#########
# samplerate and Y can be change to streaming file path if neend
# modle can be use as any model
#########
def get_features(eventin):
  amount=eventin.tolist()

  col=       ['Len_between_peaks', 'Peaks', 'CO_f1ecac', 'CO_FirstMin_ac',
       'SB_TransitionMatrix_3ac_sumdiagcov',
       'SP_Summaries_welch_rect_area_5_1',
       'SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1',
       'SP_Summaries_welch_rect_centroid']
  insidedf=pd.DataFrame(columns=col)
  row=[]
  row.append(betweenlastpeaks(amount))
  row.append(peaks(amount))
  row.append(catch22.CO_f1ecac(amount))
  row.append(catch22.CO_FirstMin_ac(amount))
  row.append(catch22.SB_TransitionMatrix_3ac_sumdiagcov(amount))
  row.append(catch22.SP_Summaries_welch_rect_area_5_1(amount))
  row.append(catch22.SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1(amount))
  row.append(catch22.SP_Summaries_welch_rect_centroid(amount))


  insidedf.loc[0] = row

  return insidedf.iloc[0:1]

#1 for long blink, #0 for blink, -1 for double , -2
def eventlist(eventclassify):
  if eventclassify=="Normal":
    return 0
  if eventclassify=="Double":
    return -1
  if eventclassify=="Long":
    return 1


def streaming_classifier(samplerate,Y,model):

    ## def streaming_classifier(path,model):
    ##    samplerate, Y = wavfile.read(path)

    xtime = np.array(range(0, len(Y)))/int(samplerate*0.5)
    window_size = int(samplerate*0.5)
    increment = int(window_size/3)
    thresh = 250


    predicted_labels = []  # stores predicted
    lower_interval = 0  # used to increment window
    max_time = int(max(xtime) * int(samplerate*0.5))

    predicted = []
    # initialing signal vector
    counter = 0
    is_event = []



    while (max_time > lower_interval + window_size):

        if max_time < lower_interval + window_size + increment:
            upper_interval = max_time
        else:
            upper_interval = lower_interval + window_size

        interval = Y[lower_interval:upper_interval]
        xinterval = xtime[lower_interval:upper_interval]  # gets corresponding time

        zerocrossing = (np.diff(np.sign(interval)) != 0).sum()
        Mean_value = np.mean(interval)
        standarddeviation = round(np.std(interval),3)
        abssum = sum(map(abs, interval))/10000
        #print(abssum,standarddeviation,counter,lower_interval,upper_interval)

        # If it is a event, recored it as True and add one to counter
        if abssum > thresh and upper_interval != max_time:
            is_event.append(True)
            counter = counter + 1
            lower_interval = lower_interval + increment

        # If ends, and the counter is greater than 0 which means it has event not finished
        elif upper_interval == max_time and counter > 0:
            begin_time = lower_interval - increment * counter
            end_time = max_time

            #ADD EVENT INTO LIST AND PRINT THE prediction
            current_value = Y[begin_time:end_time]
            # Predict by model
            y_pred=model.predict(get_features(current_value))[0]

            predicted.append([begin_time,end_time,end_time-begin_time,Y[begin_time:end_time],y_pred])
            print(y_pred)

            predicted_labels.append(eventlist(y_pred))
            ######################################
            # Moss code recognition application is added here
            ######################################
            lower_interval = lower_interval + increment

        # If it is not a event, back to its previous one and adjust whether its previous is event or not
        else:
            is_event.append(False)

            if len(is_event) == 1:
                lower_interval = lower_interval + increment
            elif is_event[-2] == True:
                begin_time = lower_interval - increment * counter
                end_time = lower_interval - increment + window_size
                
                #ADD EVENT INTO LIST AND PRINT THE prediction
                current_value = Y[begin_time:end_time]
                # Predict by model
                y_pred=model.predict(get_features(current_value))[0]
                predicted.append([begin_time,end_time,end_time-begin_time,Y[begin_time:end_time],y_pred])
                print(y_pred)

                predicted_labels.append(eventlist(y_pred))

                #########################################
                # Moss code recognition application is added here
                #########################################
                #print(begin_time,end_time,end_time-begin_time)
                lower_interval = end_time
            else:
                lower_interval = lower_interval + increment
            counter = 0

        
    df = pd.DataFrame(predicted,columns=['begin','end','Long','Values',"type"])
    return df, predicted_labels



from threading import Timer
import time
import os

## 
## 

''' flattened array: just turns the csv file into one long vector of values '''

def SimulateIn(csv):
    df = pd.read_csv(csv,sep=',',header=None,names=range(9999))
    df = df.fillna(500) # this line is not good; there are some strange NaN values which I am just replacing here
    data = df.values.flatten()
    data = data[1:len(data)] # this line is also weird since I chop off the first value, which has an unusually high value
    #a,b=streaming_classifier(10000,data,model)
    return data

''' Row by row: simulates SpikerBox streaming in the data every 1 second, writing over the old data witha new data vector'''

# def SimulateIn(csv):
#     df = pd.read_csv(csv,sep=',',header=None,names=range(9999))
#     for i in range(0,len(df)):
#         data = df.iloc[i,:]
#         a,b = streaming_classifier(10000,data,model)
#         print(b)
#         time.sleep(1)

# #os.chdir('C:/Users/oayda/Desktop/PHYS3888/Code/Implementation')
# output = SimulateIn('output.csv')#.start()
# print(output)

''' Notch filter (filters out values in vicinity of 60 Hz; this will vover the 50 Hz values too because of the quality factor)
INPUT: data from Spiker box
OUTPUT: filtered data '''

from scipy import signal
#import matplotlib.pyplot as plt

def notchFilter(data):
  # Create/view notch filter
  samp_freq = 10000  # Sample frequency (Hz)
  notch_freq = 60.0  # Frequency to be removed from signal (Hz)
  quality_factor = 0.1 # Quality factor
  b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
  freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)

  # apply notch filter to signal
  y_notched = signal.filtfilt(b_notch, a_notch, data)

  # 'A T T E N U A T E D' Data
  y_notched = (y_notched - 510)*15
  #plt.plot(y_notched)
  return y_notched




"""# Class"""

class Streaming_classifier:
  def __init__(self):
    self.existing_event=[] #if cutoff
    self.events_classified_collected=[]
    self.events_classified=[] #stores the event types
    self.leftovers=[] #so it can classify all of the leftovers from last second 
    self.decapitated = False #use in if sttment 
    self.predicted = [] #this is the df
    self.is_event=[]

  def get_features(self, eventin):
    amount=eventin.tolist()

    col=       ['Len_between_peaks', 'Peaks', 'CO_f1ecac', 'CO_FirstMin_ac',
        'SB_TransitionMatrix_3ac_sumdiagcov',
        'SP_Summaries_welch_rect_area_5_1',
        'SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1',
        'SP_Summaries_welch_rect_centroid']
    insidedf=pd.DataFrame(columns=col)
    row=[]
    row.append(betweenlastpeaks(amount))
    row.append(peaks(amount))
    row.append(catch22.CO_f1ecac(amount))
    row.append(catch22.CO_FirstMin_ac(amount))
    row.append(catch22.SB_TransitionMatrix_3ac_sumdiagcov(amount))
    row.append(catch22.SP_Summaries_welch_rect_area_5_1(amount))
    row.append(catch22.SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1(amount))
    row.append(catch22.SP_Summaries_welch_rect_centroid(amount))


    insidedf.loc[0] = row

    return insidedf.iloc[0:1]

  #1 for long blink, #0 for blink, -1 for double , -2
  def eventlist(self, eventclassify):
    if eventclassify=="Normal":
      return 0
    if eventclassify=="Double":
      return -1
    if eventclassify=="Long":
      return 1


  def classify(self,samplerate,Y,model):

      #for eveyr new inerval, here is the new event list 
      self.events_classified=[]
      ## def streaming_classifier(path,model):
      ##    samplerate, Y = wavfile.read(path)

      #adds any leftovers to front of new interval
      if len(self.leftovers)>0: 
        #print("there are leftovers")
 
        Y=np.array(self.leftovers.tolist()+Y.tolist())

       # Y=np.array(l) #starts again form where it endd in last interval 
        #makes sure to restart leftovers in case it gets carried over unnecesarily
        self.leftovers=[]
      

      xtime = np.array(range(0, len(Y)))/int(samplerate*0.5)
      window_size = int(samplerate*0.5)
      increment = int(window_size/3)
      thresh = 150


      lower_interval = 0  # used to increment window
      max_time = int(max(xtime) * int(samplerate*0.5))

      
      # initialing signal vector
      counter = 0



      #at the beginning of each classificaiotn, check if there has been a half classified signal
      if len(self.existing_event)>0:
        self.decapitated=True
      else:
        self.decapitated = False



      while (max_time > lower_interval + window_size): #while the next iteration is still possible


          if max_time < lower_interval + window_size + increment: #while the window exceeds the max time
              #upper_interval = max_time
              #print("saving leftovers")
              upper_interval = lower_interval + window_size #go as far as you can
              self.leftovers=Y[upper_interval:] #saves the rest for later
              #print(lower_interval)

          else:
             # print("new interval")
              upper_interval = lower_interval + window_size 

          interval = Y[lower_interval:upper_interval]
          xinterval = xtime[lower_interval:upper_interval]  # gets corresponding time

          zerocrossing = (np.diff(np.sign(interval)) != 0).sum()
          Mean_value = np.mean(interval)
          standarddeviation = round(np.std(interval),3)
          abssum = sum(map(abs, interval))/10000
          #print(abssum,standarddeviation,counter,lower_interval,upper_interval)
          #print(abssum)

          # If it is a event, recored it as True and add one to counter
          if abssum > thresh and upper_interval != max_time:
             # print('adding to event ')

              self.is_event.append(True)
              if lower_interval ==0: #if not rolling window, we want all of it to complete it 
                self.existing_event=self.existing_event+interval[0:].tolist()

              else: #if rolling window 
                self.existing_event=self.existing_event+interval[increment*2:].tolist()
              counter = counter + 1
              lower_interval = lower_interval + increment

          # If ends, and the counter is greater than 0 which means it has event not finished
          #note can use lenthg of leftovers since it should be reinitialised as new list if had leftovers


          # If it is not a event, back to its previous one and adjust whether its previous is event or not
          else:
              self.is_event.append(False)
             # print("finished")

              if len(self.is_event) == 1: #edge case, makes sure the first window and next bit works 
                  lower_interval = lower_interval + increment

              elif self.is_event[-2] == True and self.decapitated==True: #if continuing from last call
               # print("should have event got decapitated")

               
                #classified the event
                begin_time = lower_interval - increment * counter
                end_time = lower_interval - increment + window_size
                additional=len(self.existing_event)
                current_value = np.array(self.existing_event)
               # plt.plot(current_value)
               # plt.show()


                #reinitialises exisitng event 
                self.existing_event=[]
                self.decapitated = False
                
                #ADD previous event and ones we found together

                # Predict by model
                y_pred=model.predict(self.get_features(current_value))[0]

                self.predicted.append([begin_time-additional,end_time,end_time-begin_time+additional,current_value,y_pred])
                print(y_pred)

                self.events_classified.append(self.eventlist(y_pred))
                lower_interval = lower_interval + increment


              elif self.is_event[-2] == True and self.decapitated==False: #if within normal window, no adjustments needed
                  #resets exisitng event 
                  #print("print should have event but not decapitated")
                  self.existing_event=[] 
                  self.decapitated = False

                  #classified the event
                  begin_time = lower_interval - increment * counter
                  end_time = lower_interval - increment + window_size
                  
                  #ADD EVENT INTO LIST AND PRINT THE prediction
                  current_value = Y[begin_time:end_time]
                  # Predict by model
                  y_pred=model.predict(self.get_features(current_value))[0]
                  self.predicted.append([begin_time,end_time,end_time-begin_time,Y[begin_time:end_time],y_pred])
                  print(y_pred)

                  self.events_classified.append(self.eventlist(y_pred))
                  #print(begin_time,end_time,end_time-begin_time)
                  lower_interval = end_time
              else:
                  lower_interval = lower_interval + increment
              counter = 0

          
      self.events_classified_collected.append(self.events_classified)
      df = pd.DataFrame(self.predicted,columns=['begin','end','Long','Values',"type"])
      return df, self.events_classified

#use example =======================================================================================

#classifier=Streaming_classifier()

#busamplerate, Y = wavfile.read("/content/drive/MyDrive/Data3888/blinking/blink_olli_bot_v1.wav")
# df, labels=streaming_classifier_Noraml(samplerate,Y) -> where Y is an interval , df is the dataframe of all currently predicted events and labels is the labels in the one second





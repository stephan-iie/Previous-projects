import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import catch22

def peaks(y):  # gives the number of peaks
    y = np.array(y)
    peaks, properties = find_peaks(abs(y), height=1700, width=200)
    return sum(np.diff(peaks) > 400) + 1


def betweenlastpeaks(y):  # gives diff in indexes of first and last peak
    y = np.array(y)
    peaks, properties = find_peaks(abs(y), height=1700, width=200)
    if len(peaks) == 0:
        return 0
    return peaks[-1] - peaks[0]

class Streaming_classifier:
    def __init__(self):
        self.existing_event = []  # if cutoff
        self.events_classified = []  # stores the event types
        self.events_classified_collected = []
        self.leftovers = []  # so it can classify all of the leftovers from last second
        self.decapitated = False  # use in if sttment
        self.predicted = []  # this is the df
        self.is_event = []

    def get_features(self, eventin):
        amount = eventin.tolist()

        col = ['Len_between_peaks', 'Peaks', 'CO_f1ecac', 'CO_FirstMin_ac',
               'SB_BinaryStats_mean_longstretch1', 'PD_PeriodicityWang_th0_01',
               'SB_BinaryStats_diff_longstretch0', 'SP_Summaries_welch_rect_centroid',
               'FC_LocalSimple_mean3_stderr']
        insidedf = pd.DataFrame(columns=col)
        row = []
        row.append(betweenlastpeaks(amount))
        row.append(peaks(amount))
        row.append(catch22.CO_f1ecac(amount))
        row.append(catch22.CO_FirstMin_ac(amount))
        row.append(catch22.SB_BinaryStats_mean_longstretch1(amount))
        row.append(catch22.PD_PeriodicityWang_th0_01(amount))
        row.append(catch22.SB_BinaryStats_diff_longstretch0(amount))
        row.append(catch22.SP_Summaries_welch_rect_centroid(amount))
        row.append(catch22.FC_LocalSimple_mean3_stderr(amount))

        insidedf.loc[0] = row

        return insidedf.iloc[0:1]

    # 1 for long blink, #0 for blink, -1 for double , -2
    def eventlist(self, eventclassify):
        if eventclassify == "Normal":
            return 0
        if eventclassify == "Double":
            return -1
        if eventclassify == "Long":
            return 1

    def classify(self,Y,model):
      samplerate=10000

      #for eveyr new inerval, here is the new event list 
      self.events_classified=[]


      #adds any leftovers to front of new interval
      if len(self.leftovers)>0: 

        Y=np.array(self.leftovers.tolist()+Y.tolist())
        self.leftovers=[]


      xtime = np.array(range(0, len(Y)))/int(samplerate*0.5)
      window_size = int(samplerate*0.5)
      increment = int(window_size/3)
      thresh = 320


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
              upper_interval = lower_interval + window_size #go as far as you can
              self.leftovers=Y[upper_interval:] #saves the rest for later

          else:
              upper_interval = lower_interval + window_size 

          interval = Y[lower_interval:upper_interval]
          xinterval = xtime[lower_interval:upper_interval]  # gets corresponding time

          abssum = sum(map(abs, interval))/10000

          # If it is a event, recored it as True and add one to counter
          if abssum > thresh and upper_interval != max_time:

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

              if len(self.is_event) == 1: #edge case, makes sure the first window and next bit works 
                  lower_interval = lower_interval + increment

              elif self.is_event[-2] == True and self.decapitated==True: #if continuing from last call


                #classified the event
                begin_time = lower_interval - increment * counter
                end_time = lower_interval - increment + window_size
                additional=len(self.existing_event)
                current_value = np.array(self.existing_event)

                #reinitialises exisitng event 
                self.existing_event=[]
                self.decapitated = False

                #ADD previous event and ones we found together

                # Predict by model
                y_pred=model.predict(self.get_features(current_value))[0]

                self.predicted.append([begin_time-additional,end_time,end_time-begin_time+additional,current_value,y_pred])
                ###

                self.get_features(current_value)

                ###
                self.events_classified.append(self.eventlist(y_pred))
                lower_interval = lower_interval + increment


              elif self.is_event[-2] == True and self.decapitated==False: #if within normal window, no adjustments needed
                  #resets exisitng event 
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
                  ###

                  self.get_features(current_value)

                  ###
                  self.events_classified.append(self.eventlist(y_pred))
                  lower_interval = end_time
              else:
                  lower_interval = lower_interval + increment
              counter = 0

      self.events_classified_collected.append(self.events_classified)

      df = pd.DataFrame(self.predicted,columns=['begin','end','Long','Values',"type"])
      return df, self.events_classified

from scipy.io import wavfile
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from catch22 import catch22_all
import pickle
from sklearn.ensemble import RandomForestClassifier

der = input('What is the directory of the blinking folder?\n')


pathlist_1 = [str(der) + "PROCESSED day2_ollie_blink_v1_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v2_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v3_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v4_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v5_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v6_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v7_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v8_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v9_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_blink_v10_nofilter_lists.csv"]


pathlist_2 = [str(der) + "PROCESSED day2_ollie_longblink_v1_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v2_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v3_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v4_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v5_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v6_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v7_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v8_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v9_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_longblink_v10_nofilter_lists.csv"]


pathlist_3 = [str(der) + "PROCESSED day2_ollie_doubleblink_v1_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v2_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v3_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v4_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v5_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v6_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v7_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v8_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v9_nofilter_lists.csv",
              str(der) + "PROCESSED day2_ollie_doubleblink_v10_nofilter_lists.csv",]

def streaming_training(samplerate, path, Type):
    df = pd.read_csv(path)
    df.columns = ['Values']
    Y = list(df['Values'])

    xtime = np.array(range(0, len(Y))) / int(samplerate * 0.5)
    window_size = int(samplerate * 0.5)
    increment = int(window_size / 3)
    thresh = 330

    predicted_labels = []  # stores predicted
    lower_interval = 0  # used to increment window
    max_time = int(max(xtime) * int(samplerate * 0.5))

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
        standarddeviation = round(np.std(interval), 3)
        abssum = sum(map(abs, interval)) / 10000
        # print(abssum,standarddeviation,counter,lower_interval,upper_interval)

        # If it is a event, recored it as True and add one to counter
        if abssum > thresh and upper_interval != max_time:
            is_event.append(True)
            counter = counter + 1
            lower_interval = lower_interval + increment

        # If ends, and the counter is greater than 0 which means it has event not finished
        elif upper_interval == max_time and counter > 0:
            begin_time = lower_interval - increment * counter
            end_time = max_time
            predicted.append([begin_time, end_time, end_time - begin_time, Y[begin_time:end_time]])
            # print(begin_time,end_time)
            lower_interval = lower_interval + increment

        # If it is not a event, back to its previous one and adjust whether its previous is event or not
        else:
            is_event.append(False)

            if len(is_event) == 1:
                lower_interval = lower_interval + increment
            elif is_event[-2] == True:
                begin_time = lower_interval - increment * counter
                end_time = lower_interval - increment + window_size

                predicted.append([begin_time, end_time, end_time - begin_time, Y[begin_time:end_time]])
                # print(begin_time,end_time,end_time-begin_time)
                lower_interval = end_time
            else:
                lower_interval = lower_interval + increment
            counter = 0

    df = pd.DataFrame(predicted, columns=['begin', 'end', 'Long', 'Values'])
    df["Type"] = Type
    return df
    # return predicted,eventtime


"""## Noraml Blink test"""
print("I am training the model...")

Normal_blink=[]
for path in pathlist_1:
  result = streaming_training(10000,path,"Normal")
  Normal_blink.append(result)
Normal_blink = pd.concat(Normal_blink)

"""## Long Blink test"""

Long_blink=[]
for path in pathlist_2:
  result = streaming_training(10000,path,"Long")
  Long_blink.append(result)
Long_blink = pd.concat(Long_blink)

"""## Double test"""

Double_blink=[]
for path in pathlist_3:
  result = streaming_training(10000,path,"Double")
  Double_blink.append(result)
Double_blink = pd.concat(Double_blink)

"""# Combine table and Features

## Catch22
"""

EventFrame = pd.concat([Normal_blink, Long_blink, Double_blink], ignore_index=True)
EventFrame

"""## Peak and Withs"""




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
df = pd.DataFrame(columns=col)

for i in range(0, len(EventFrame)):
    current_row = EventFrame[i:i + 1]
    current_type = current_row['Type'].to_string().split()[1]
    Y = sum(current_row["Values"]).tolist()
    t = catch22_all(Y)
    features = t["values"]
    features.insert(0, current_type)
    features.insert(1, peaks(Y))
    features.insert(1, betweenlastpeaks(Y))
    df.loc[i] = features

"""##Random Forest"""

# this is from a feature selection algorihtmn, ive harcoded it since it might change and only need this for the main loop to trina
selected_feat = ['Len_between_peaks', 'Peaks', 'CO_f1ecac', 'CO_FirstMin_ac',
                 'SB_TransitionMatrix_3ac_sumdiagcov',
                 'SP_Summaries_welch_rect_area_5_1',
                 'SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1',
                 'SP_Summaries_welch_rect_centroid']
rfselected = df[selected_feat]
y = df['Type']

model = RandomForestClassifier(n_estimators=100).fit(rfselected, y)
filename = 'model.sav'
pickle.dump(model, open(filename, 'wb'))



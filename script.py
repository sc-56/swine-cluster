#%% import
print('quite long time no see.')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import seaborn as sns

#%% import one dataframe and visualize trend
df_1 = pd.read_csv('./0-data/17.csv')
# active volume: active volume
# active length: time account for period of time
# temperature: current pig temperature
# timestamp: information for index

# clinical signs of a sick pig
## √ fever: high body temperature
### normal temperature of pig is around 38-39 centigrade.
### sensor needs to capture this relative information.
###

## off-feed: eat nothing
## √ lethargy: no movement
## nasal discharge:
## cough: soundtalks
## thumping:
## hard time breathing: cannot breathe well and easily
## diarrhea:

### hot-weather may lead to temperature raising
### pigs cannot sweat, and therefore they needs to stay cool during hotday.

# change column names
df_1.columns = ['active-volume', 'active-period', 'active-status', 'temperature', 'voltage', 'timestamp']

# change type appropriately
df_1['timestamp'] = pd.to_datetime(df_1['timestamp'])
# df_1.reset_index('timestamp', inplace=True)

# set new index as timestamp.
# df_1 = df_1.set_index('timestamp').

# visualize temperature changing with time stamp
# plt.plot(df_1.index, df_1['temperature'])
# plt.show()
# figure size should be set firstly

start_point = '2021-11-10'
end_point = '2021-11-12'

start = datetime.strptime(start_point, "%Y-%m-%d")
end = datetime.strptime(end_point, "%Y-%m-%d")

df_1 = df_1.loc[(df_1['timestamp'] >= start) & (df_1['timestamp'] <= end)]

plt.figure(figsize=(15, 6))
sns.set_style("darkgrid")
sns.lineplot(x='timestamp', y='temperature', data=df_1)
plt.show()

## temperature result are badly affected by environment, and not stable as ideal.
# study about active volume/period
## they are accumulation relative data.
## active can be taken as gentle / mid / drastic by analysis with each motion.

plt.figure(figsize=(15, 6))
sns.set_style("darkgrid")
sns.lineplot(x='timestamp', y='active-volume', data=df_1)
plt.show()

## print summarization of basic statistics.
temperature_min = df_1['temperature'].min()
temperature_max = df_1['temperature'].max()
temperature_median = df_1['temperature'].median()
temperature_avg = df_1['temperature'].mean()

## accumulated active volume
active_total = df_1['active-volume'].max() - df_1['active-volume'].min()

# count times of different moving
df_1['active-interval'] = df_1['active-period'].diff().fillna(0).astype('int32')
df_1['incremental-volume'] = df_1['active-volume'].diff().fillna(0).astype('int32')
df_1['active-fierce-rate'] = df_1['incremental-volume'] / df_1['active-interval']

# replace inf with 0
df_1['active-fierce-rate'].replace([np.inf, -np.inf], 0, inplace=True)
df_1['active-fierce-rate'].replace(np.nan, 0, inplace=True)

# set basic statistics value of fierce rate
fierce_quantile= df_1['active-fierce-rate'].quantile([0.25, 0.5, 0.75])
# set criterions of fierce motion:
## 0-1: gentle motion
## 1-2: normal motion
## 2-3: drastic motion

# add motion type into dataframe
df_1.loc[df_1['active-fierce-rate'] == 0.00, 'active-type'] = 'still'
df_1.loc[(0 < df_1['active-fierce-rate']) & (df_1['active-fierce-rate'] <= 1), 'active-type' ] = 'gentle'
df_1.loc[(1 < df_1['active-fierce-rate']) & (df_1['active-fierce-rate'] <= 2), 'active-type' ] = 'normal'
df_1.loc[2 < df_1['active-fierce-rate'], 'active-type'] = 'drastic'

# use one historgram to show the fierce rate distribution
sns.histplot(data=df_1, x='active-type')
plt.show()

print('temperature: --- --- --- --- --- --- --- --- ---')
print('min-temperature: {}'.format(temperature_min))
print('max-temperature: {}'.format(temperature_max))
print('median-temperature: {}'.format(temperature_median))
print('average-temperature: {}'.format(temperature_avg))
print("\n")

print('activity: --- --- --- --- --- --- --- --- --- ---')
print('active-volume: {}'.format(active_total))
print(df_1['active-type'].value_counts())
print("\n")

# potential features:
## temperature: median/average/max
## active: overall/active type
### use these to make cluster

#%% 48 hours may good to see.
# bulid dataframe for cluster structure

df_cluster = pd.DataFrame(columns=['temperature_min', 'temperature_max', 'temperature_median', 'active-volume',
                                   'active-gentle', 'active-normal', 'active-drastic'])

row = 0

df_cluster.loc[row, 'id'] = '1601'
df_cluster.loc[row, 'temperature_min'] = temperature_min
df_cluster.loc[row, 'temperature_max'] = temperature_max
df_cluster.loc[row, 'temperature_median'] = temperature_median
df_cluster.loc[row, 'active-volume'] = active_total
df_cluster.loc[row, 'active-gentle'] = df_1['active-type'].value_counts()['gentle']
df_cluster.loc[row, 'active-normal'] = df_1['active-type'].value_counts()['normal']
df_cluster.loc[row, 'active-drastic'] = df_1['active-type'].value_counts()['drastic']

print(df_cluster)

#%% make up loop to make up whole file.

import requests
from io import StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from matplotlib import dates
pd.options.mode.chained_assignment = None

r = requests.post(
    'https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.json')
r.encoding = 'uft-8'

df = pd.read_json(StringIO(r.text.replace("/", "-")))

mdf = pd.DataFrame(columns=['Time', '基隆市', '台北市', '新北市'])
mdf['Time'] = pd.date_range(
    start="2021-05-17", end=datetime.today().strftime('%Y%m%d'))
mdf = mdf.replace(np.nan, 0)

for i in range(len(mdf)):
    for j in range(len(df)):
        if (df['縣市'][j] == '基隆市' and df['個案研判日'][j] == mdf['Time'][i].strftime('%Y-%m-%d')):
            mdf['基隆市'][i] = df['確定病例數'][j] + mdf['基隆市'][i]
        if (df['縣市'][j] == '台北市' and df['個案研判日'][j] == mdf['Time'][i].strftime('%Y-%m-%d')):
            mdf['台北市'][i] = df['確定病例數'][j] + mdf['台北市'][i]
        if (df['縣市'][j] == '新北市' and df['個案研判日'][j] == mdf['Time'][i].strftime('%Y-%m-%d')):
            mdf['新北市'][i] = df['確定病例數'][j] + mdf['新北市'][i]

fig, ax = plt.subplots(dpi=200)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.bar(mdf["Time"], mdf["基隆市"], alpha=0.1, label="Keelung")
plt.bar(mdf["Time"], mdf["台北市"], alpha=0.1, label="Taipei")
plt.bar(mdf["Time"], mdf["新北市"], alpha=0.1, label="New Taipei")
plt.legend(prop={'size': 6})
plt.xlabel("Date")
ax.xaxis.set_major_locator(dates.DayLocator(interval=1))
fig.autofmt_xdate(rotation=45)
plt.xticks(fontsize=5)
plt.ylabel("Case")
plt.title('Comformed Cases')
plt.show()

print(mdf)

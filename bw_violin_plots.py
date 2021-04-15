# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 09:44:04 2021

@author: Michael Murphy
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wu_rainfall import WuRainfall
import datetime

VER = "_01b" # Version, any string
f = 'sw_tph_g_data_LVR.csv' # Data file, csv format

df1 = pd.read_csv('sw_tph_g_data_LVR.csv', infer_datetime_format = True)
df1["date_time"] = pd.to_datetime(df1.Date)

def string_to_num(df, col):
    """
    

    Parameters
    ----------
    df : pandas DataFrame 
        DataFrame containing numerical columns as string.
    col : pandas series ('column') contained in df
        DataFrame column with numerical values in string format

    Returns
    -------
    df with columns converted to numeric dtype

    """
    df[col] = df[col].str.replace(r"\,", '')
    df[col] = pd.to_numeric(df[col])

string_to_num(df1, "ConcentrationNumber")
string_to_num(df1, "ConcentrationNumber2")    

df2 = df1.copy()    
df2.dropna(axis=0, subset=["ConcentrationNumber2"], inplace=True)
df2.sort_values(by="date_time", inplace=True)
df2 = df2.loc[df2.date_time > '2019/11/26']
df2["Sample Location"] = df2.LocCode
print(df1.dtypes)

rain = WuRainfall('idylberry_precip_112019-032021.xlsx')
rain_monthly = rain.resamp_rain_sum(interval = 'M')
rain_monthly["Date"] = pd.to_datetime(rain_monthly["Date"])
rain_monthly["Date"] = rain_monthly["Date"] - datetime.timedelta(days=15)

#writer = pd.ExcelWriter("Idyllberry_Precip_1month_sum.xlsx")
#rain_monthly.to_excel(excel_writer = writer)
#writer.save()

sns.set_context('talk')

# plt.figure(figsize=(24, 16))
# p1 = sns.barplot(x='Date', y='rainfall_inches', data=rain_monthly, color='gray')
# p1 = sns.scatterplot()
# p1.set_xticklabels(rain_monthly.Date.dt.strftime("%Y-%m"), rotation=45)
# plt.ylabel("Monthly Cummulative Rainfall at Idylberry Ranch, inches")
# plt.xlabel("Date")
# plt.savefig("Precip_Idylberry.png")
# plt.clf()


# plt.figure(figsize=(24, 16))
# p2 = sns.swarmplot(df2.Date, df2.ConcentrationNumber2, hue = df2["Sample Location"], palette='Spectral', size=9, edgecolor='black', linewidth=0.7, alpha=1)
# #p2 = sns.swarmplot(df2.Date, df2.ConcentrationNumber2, color='gray', alpha=0.7)
# #p2 = sns.boxplot(df2.Date, df2.ConcentrationNumber2, color='white')
# p2.set_xticklabels(p2.get_xticklabels(), rotation=45)
# plt.ylabel("TPH-gasoline in surface water, ppb")
# plt.xlabel("Sample Date")
# #plt.margins(0.2)
# plt.subplots_adjust(bottom=0.2)
# plt.savefig("TPH-g_v_Date_BW_plot.png")
# plt.clf()


#df3 = df2.sort_values(by="DistanceFromSpillSite", ascending=True) # Re-sort dataframe on distance from spill site
df3 = df2.copy()
df3 = df3.loc[df3.date_time > '2019/11/26']
#df3 = df3.loc[df3.ConcentrationNumber2 > 1000]
df3["Sample Location"] = df3.LocCode
df3["Concentration, TPH-g (ppb)"] = df3.ConcentrationNumber2

df3_precip = pd.merge_asof(df3, rain_monthly, left_on = "date_time", right_on = "Date", direction = 'nearest')

# plt.figure(figsize=(24, 16))
# p3 = sns.swarmplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, hue = df3["Sample Location"], palette='Spectral', size=9, edgecolor='black', linewidth=0.7, alpha=1)
# #p3 = sns.stripplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, hue = df3.LocCode, palette='Spectral', size=8, edgecolor='black', linewidth=0.7, alpha=1, jitter=True)
# p3 = sns.boxplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, color='white')
# #p3 = sns.violinplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, color='white', inner='box', linewidth=0.8)
# p3.set_xticklabels(p3.get_xticklabels(), rotation=45)

# plt.ylabel("TPH-gasoline in surface water, ppb")
# plt.xlabel("Downstream Distance from Spill Site, feet")
# #p3.set(yscale="log")
# #p3.set(ylim=(10, 10**6))

# #plt.title
# #axis2 = p3.twiny()
# #axis2.set_xticks(ticks = df3.index)
# #axis2.set_xticklabels( df3.LocCode, rotation = 45)
# #plt.margins(0.2)
# #plt.subplots_adjust(bottom=0.2)
# plt.savefig("TPH-g_v_Dist_BW_plot_.png")
# plt.clf()

# plt.figure(figsize=(22, 16))
# p4 = sns.regplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, truncate=False, fit_reg=True)
# plt.ylabel("TPH-gasoline in surface water, ppb")
# plt.xlabel("Downstream Distance from Spill Site, feet")
# #plt.show(p4)
# plt.savefig("TPH-g_v_Dist_LinReg_plot.png")
plt.clf()

plt.figure(figsize=(22, 16))
p5 = sns.relplot(df3_precip.Date_x, df3_precip.DistanceFromSpillSite, size = df3_precip["Concentration, TPH-g (ppb)"] , hue = df3_precip["Sample Location"], palette='Spectral',
                 edgecolor='black', linewidth=0.7, alpha=1, height = 16, aspect = 1.5, sizes=(50, 1200))
#p5.secondary_yaxis('right')
plt.xticks(rotation=45)

plt.ylabel("Downstream Distance from Spill Site, feet")
plt.xlabel("Date")
ay2 = plt.twinx()
p5 = sns.barplot(df3_precip.Date_x, df3_precip.rainfall_inches, ax=ay2, alpha=0.3, color = "gray")
plt.ylabel("Monthly Rainfall, inches")
plt.subplots_adjust(right=0.82)

#p6.yaxis.tick_right()
#p6.yaxis.set_label_position("right")


#p3 = sns.stripplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, hue = df3.LocCode, palette='Spectral', size=8, edgecolor='black', linewidth=0.7, alpha=1, jitter=True)
#p3 = sns.boxplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, color='white')
#p3 = sns.violinplot(df3.DistanceFromSpillSite, df3.ConcentrationNumber2, color='white', inner='box', linewidth=0.8)

#plt.legend(handletextpad=0.1)


#p3.set(yscale="log")
#p3.set(ylim=(10, 10**6))

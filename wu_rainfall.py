# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:48:46 2021

@author: Michael Murphy

Script to process weather data from WunderGround
"""
import pandas as pd

class WuRainfall:
    def __init__(self, file):
        self.df = pd.read_excel(file, engine='openpyxl')
        self.df['rainfall_inches'] = self.df["Sum"].str.replace(r'in', '').str.rstrip()
    
    def get_df(self):
        df = self.df[["Date", "rainfall_inches"]]
        df['rainfall_inches'] = pd.to_numeric(df['rainfall_inches'])
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index(df["Date"], inplace=True)
        return df
    
    def resamp_rain_sum(self, interval):
        df = self.get_df()
        df_r = df.resample(interval).sum()
        df_r.reset_index(inplace=True)
        return df_r
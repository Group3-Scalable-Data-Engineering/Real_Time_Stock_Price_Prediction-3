import yfinance as yf

from datetime import date, timedelta

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense

import matplotlib.pyplot as plt 
import seaborn as sns

def RNN_model():
    model = Sequential()
    model.add(LSTM(128, input_shape=(30, 6), return_sequences=True))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(64))
    model.add(Dense(32))
    model.add(Dense(7, activation='linear'))

    return model


def plot_prediction(stock):
    model = RNN_model()
    model.load_weights("Weights\\"+stock+"_weights.h5")

    
    current_date = date.today().isoformat()   
    days_before = (date.today()-timedelta(days=45)).isoformat() 
    data = yf.download(stock, start=days_before, end=current_date)
    data = data.tail(30)
    data["Volume"]/=1000000
    fig = plt.figure(figsize=(12,4))
    
    label = data.index
    data = data.to_numpy()
    pred = model.predict(np.reshape(data, (1,30,6)))[0]
  
    last = label[-1]
    label_pred=[]
    for i in range(0,8):
        label_pred.append(last + timedelta(days=i))
        
        
    plt.plot(label,data[:,3], label="Actual Stock price")
    plt.title(stock+" stock price prediction.")

    
    plt.plot(label_pred,np.append(np.array([data[-1,3]]),pred), label="Predicted Stock price")
    
    
    return fig
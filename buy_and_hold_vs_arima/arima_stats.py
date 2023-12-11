# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['foo', 'say_hello', 'create_arima_prediction', 'create_auto_arima_prediction', 'create_auto_arima_prediction_future_2']

# %% ../nbs/00_core.ipynb 4
import torch
import pandas as pd
import numpy as np
import pmdarima as pm
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA


# %% ../nbs/00_core.ipynb 5
def foo(name): 
    return "Hello HAHAHAH" + name

# %% ../nbs/00_core.ipynb 6
def say_hello(to):
    "Say hello to somebody"
    return f'Hello {to}!'

# %% ../nbs/00_core.ipynb 7
def create_arima_prediction(series):
    auto_arima = pm.auto_arima(series, stepwise=False, seasonal=False)

# %% ../nbs/00_core.ipynb 11
def create_auto_arima_prediction(series_data, prediction_depth=30):
    """
    Given pandas series return a series with the same indexes (Dates)
    """
    df = pd.DataFrame()
    df['High'] = series_data
    df.index = np.arange(len(df))

    msk = (df.index < len(df)-prediction_depth)
    df_train = df[msk].copy()
    df_test = df[~msk].copy()

    df_train = df_train['High']
    df_test = df_test['High']
    
    print(df_train.isna().sum())
    
    # Doesn't work very well , Trying to Autocreate the arima parameters
    #auto_arima = pm.auto_arima(df_train.to_numpy())
    
    auto_arima = pm.auto_arima(df_train.to_numpy(), start_p=1, start_q=1, d=0, max_p=5, max_q=5,
                      out_of_sample_size=10, suppress_warnings=True,
                      stepwise=True, error_action='ignore')
    
    forecast_test_auto = auto_arima.predict(n_periods=len(df_test))
  
    
    auto_pred = pd.Series([None]*len(df_train) + list(forecast_test_auto))
    auto_pred.index = series_data.index
    print(auto_arima)
    #df['forecast_auto'] = [None]*len(df_train) + list(forecast_test_auto)

    #from statsmodels.tsa.arima.model import ARIMA
    #model = ARIMA(df_train, order=(2,1,3))
    #model_fit = model.fit()
    #forecast_test = model_fit.forecast(len(df_test))
    #df['forecast_manual'] = [None]*len(df_train) + list(forecast_test)
    #return df['forecast_auto']
    return auto_pred


# %% ../nbs/00_core.ipynb 12
def create_auto_arima_prediction_future_2(series_data,future=40):
    temp_series = pd.Series(series_data)
    temp_series=pd.concat([temp_series,pd.Series([None]*future , index=pd.date_range(series_data.index[-1], freq='D', periods=future))])
    auto_pred = create_auto_arima_prediction(temp_series,future)
    return auto_pred

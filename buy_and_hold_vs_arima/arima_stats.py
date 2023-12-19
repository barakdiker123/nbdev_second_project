# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['foo', 'say_hello', 'create_arima_prediction', 'create_auto_arima_prediction', 'create_auto_arima_prediction_future_2',
           'create_dataframe_with_series', 'create_dataframe', 'get_top_players', 'top_score',
           'create_dataframe_high_default']

# %% ../nbs/00_core.ipynb 5
#import torch
import pandas as pd
from collections import OrderedDict
import numpy as np
import pmdarima as pm
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA


# %% ../nbs/00_core.ipynb 6
def foo(name): 
    return "Hello HAHAHAH" + name

# %% ../nbs/00_core.ipynb 7
def say_hello(to):
    "Say hello to somebody"
    return f'Hello {to}!'

# %% ../nbs/00_core.ipynb 8
def create_arima_prediction(series):
    auto_arima = pm.auto_arima(series, stepwise=False, seasonal=False)

# %% ../nbs/00_core.ipynb 12
def create_auto_arima_prediction(series_data, prediction_depth=30,logger = False):
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
    
    #print(df_train.isna().sum())
    
    # Doesn't work very well , Trying to Autocreate the arima parameters
    #auto_arima = pm.auto_arima(df_train.to_numpy())
    
    auto_arima = pm.auto_arima(df_train.to_numpy(), start_p=1, start_q=1,d=0, max_p=5, max_q=5,
                      out_of_sample_size=10, suppress_warnings=True,
                      stepwise=True, error_action='ignore')
    
    forecast_test_auto = auto_arima.predict(n_periods=len(df_test))
  
    
    auto_pred = pd.Series([None]*len(df_train) + list(forecast_test_auto))
    auto_pred.index = series_data.index
    if logger:
        print(auto_arima)
    #df['forecast_auto'] = [None]*len(df_train) + list(forecast_test_auto)

    #from statsmodels.tsa.arima.model import ARIMA
    #model = ARIMA(df_train, order=(2,1,3))
    #model_fit = model.fit()
    #forecast_test = model_fit.forecast(len(df_test))
    #df['forecast_manual'] = [None]*len(df_train) + list(forecast_test)
    #return df['forecast_auto']
    return auto_pred


# %% ../nbs/00_core.ipynb 13
def create_auto_arima_prediction_future_2(series_data,future=60):
    temp_series = pd.Series(series_data)
    temp_series=pd.concat([temp_series,pd.Series([None]*future , index=pd.date_range(series_data.index[-1], freq='D', periods=future))])
    auto_pred = create_auto_arima_prediction(temp_series,future)
    return auto_pred

# %% ../nbs/00_core.ipynb 14
def create_dataframe_with_series(func , series_data,future=60):
    pred_series = func(series_data,future=60)
    df = pd.DataFrame()
    df['pred'] = pred_series
    df['High'] = series_data
    return df

# %% ../nbs/00_core.ipynb 32
def create_dataframe(companies , series_name='High'): # for example companies = ["LUMI.TA","DSCT.TA"]
    tickers = [yf.Ticker(ticker).history( start='2020-12-10')[series_name].rename(ticker) for ticker in companies]
    df = pd.concat(tickers, axis=1)
    return df
    

# %% ../nbs/00_core.ipynb 33
def get_top_players(data, n=2, order=False):
    """Get top n players by score. 

    Returns a dictionary or an `OrderedDict` if `order` is true.
    """ 
    #top = sorted(data.items(), reverse=True)[:n]
    #if order:
    #    return OrderedDict(top)
    #return dict(top)
    return dict(sorted(data.items(), key=lambda x:x[1],reverse=True)[:n])
    #return dict(sorted(data , reverse=True)[:n])

# %% ../nbs/00_core.ipynb 34
def top_score(df ,current_day , days=30 , top =2): 
    """
    df - a pd.DataFrame where each series is a stock for example the "High" of leumi 
    current_day - can use current_day and all days before 
    example to current_day -> current_day = "2022-12-10"
    days - how many days to predict into the future 
    example for days -> days = 30 
    top - select the top performed stocks for investing 
    """
    dict_profit = {}
    for series in df:
        #print(df[series].iloc[0])
        #print(df[series])
        #print(df[series].loc[:current_day])
        dataframe_predict = create_dataframe_with_series(create_auto_arima_prediction_future_2 , df[series].loc[:current_day])
        profit = dataframe_predict['pred'].dropna().iloc[days] - dataframe_predict['pred'].dropna().iloc[0]
        dict_profit[series] = profit
        #print(profit) 
    #print(dict_profit)
    #print(get_top_players(dict_profit,n=top))
    return get_top_players(dict_profit,n=top) # Best to invest ! 

# %% ../nbs/00_core.ipynb 38
def create_dataframe_high_default():
    companies = [
        "LUMI.TA",
        "DSCT.TA",
        "BEZQ.TA",
        "CEL.TA",
        "ESLT.TA",
        "NICE.TA",
        "TEVA.TA",
        "POLI.TA",
        "MZTF.TA",
        "FIBI.TA",
        "HARL.TA",
        "MGDL.TA",
        "CLIS.TA",
        "PHOE.TA",
        "MMHD.TA",
        "DRS.TA",
        "BSEN.TA",
        "HLAN.TA",
        "FTAL.TA",
        "DANE.TA",
        "ONE.TA",
        "MTRX.TA",
        "ALHE.TA",
        "UWAY.TA",
        "ICL.TA",
        "TA35.TA",
        "TA90.TA",
    ]
    tickers = [yf.Ticker(ticker).history( start='2020-12-10')['High'].rename(ticker) for ticker in companies]
    df = pd.concat(tickers, axis=1)
    return df

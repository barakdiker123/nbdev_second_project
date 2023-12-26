# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_thesis_app.ipynb.

# %% auto 0
__all__ = ['companies', 'tickers', 'df', 'external_stylesheets', 'app', 'update_output']

# %% ../nbs/03_thesis_app.ipynb 2
import buy_and_hold_vs_arima
import yfinance as yf
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
from waitress import serve
import numpy as np
import dash_bootstrap_components as dbc

from .arima_stats import create_auto_arima_prediction_future_2
from .arima_stats import create_dataframe_with_series
from .arima_stats import top_score
from .arima_stats import get_top_players
from .arima_stats import create_dataframe


# %% ../nbs/03_thesis_app.ipynb 3
from .thesis_ta35 import get_revenue_arima
from .arima_stats import create_auto_arima_prediction_future_2
from .thesis_ta35 import strategy_invest
import yfinance as yf
import pandas as pd

# %% ../nbs/03_thesis_app.ipynb 13
#tickers = [series_data["High"].rename('TA35.TA')]
#df = pd.concat(tickers, axis=1)
#df.columns
#df['TA35.TA']




#companies = ['AMZN','NFLX','GOOG']
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

#companies = companies + ticker_stocks



tickers = [yf.Ticker(ticker).history( start='2021-12-10')['High'].rename(ticker) for ticker in companies]
df = pd.concat(tickers, axis=1)
df

for a in df.columns:
    print(a)
    
df[['LUMI.TA','ICL.TA']]
#count_invested_months , total_months , expected_diff_arr , revenue_loss_diff_arr , current_date_arr , capital_arr = strategy_invest(create_auto_arima_prediction_future_2 , df['TA35.TA']['2022-12-20':'2023-6-25'])


# %% ../nbs/03_thesis_app.ipynb 15
# http://127.0.0.1:8050/

#df = px.data.gapminder()
#df.columns



external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Markdown('''
        # Comparing Arima model and Buy and Hold strategy
        This is final project of master's degree in Haifa University 
        
        Please Select one Stock or Index and wait for the program to simulate 
        
        Please note that whenever the graph is Red money is put inside the stock (Buying) 
        and whenever Its green money is given back from the stock (Selling)
        '''),
        dcc.Markdown('''
        # Here is the prediction code 
        In the following function I am doing the actual prediction 
        Please note that the `d=0` I am NOT taking the different series 
        As evidented , taking the real series product better results !! 
        ```python
        def create_auto_arima_prediction(series_data, prediction_depth=30,logger = False):
            """
            Given pandas series return a series with the same indexes (Dates)
            Given a series_data which is of type pd.Series with dates as index 
            and index/stock value as data 
            splits the data to before the last 30 values which is named df_train 
            and the last 30 values which is named df_test
            
            the arima prediction is based ONLY on df_train (without 30 last values!)
            """
            df = pd.DataFrame()
            df['High'] = series_data
            df.index = np.arange(len(df))

            msk = (df.index < len(df)-prediction_depth)
            df_train = df[msk].copy()
            df_test = df[~msk].copy()

            df_train = df_train['High']
            df_test = df_test['High']
            auto_arima = pm.auto_arima(df_train.dropna().to_numpy(), start_p=1, start_q=1,d=0, max_p=5, max_q=5,
                              out_of_sample_size=10, suppress_warnings=True,n_jobs= 1,method='nm',#seasonal=True,
                              stepwise=False, error_action='ignore')
            forecast_test_auto = auto_arima.predict(n_periods=len(df_test))
            auto_pred = pd.Series([None]*len(df_train) + list(forecast_test_auto))
            auto_pred.index = series_data.index
            return auto_pred
        ```
        ## Some auxilary functions 
        The following function help understand how I use the create_auto_arima_prediction which 
        is the core where the entire codebase based on 
        
        ```python
        def create_auto_arima_prediction_future_2(series_data,future=60):
            temp_series = pd.Series(series_data)
            temp_series=pd.concat([temp_series,pd.Series([None]*future , index=pd.date_range(series_data.index[-1], freq='D', periods=future))])
            auto_pred = create_auto_arima_prediction(temp_series,future)
            return auto_pred
        def create_dataframe_with_series(func , series_data,future=60):
            pred_series = func(series_data,future=60)
            df = pd.DataFrame()
            df['pred'] = pred_series
            df['High'] = series_data
            return df
        ```
        ## Here is a basic usage of the function 
        
        For installing the program do 
        ```bash
        pip3 install buy_and_hold_vs_arima
        ```
        To Create prediction one should simply do the following 
        ```python
        from buy_and_hold_vs_arima.arima_stats import *
        import yfinance as yf
        series_data = yf.download('LUMI.TA', start='2021-12-10', end='2022-12-30')
        df = create_dataframe_with_series(create_auto_arima_prediction_future_2 , series_data['High'])
        df.plot()
        ```
        '''),
        dcc.Dropdown(
            id="dpdn2",
            value=["TA35.TA"],
            multi=True,
            options=[{"label": x, "value": x} for x in df.columns],
        ),
        dbc.Row(
            # Values is the initial values
            # first arg and second arg are the overall range , third is the jumps 
                dcc.RangeSlider(0, len(df) - 1 , 1, count=1, value=[(len(df) - 1)*1//4 + 2, len(df) - 1] , id="range-inference") 
        ),
        dbc.Row(
            dcc.Graph(
                    id="inference-graph",
                    figure={},
                    clickData=None,
                    hoverData=None,
                    config={
                        "staticPlot": False,  # True, False
                        "scrollZoom": True,  # True, False
                        "doubleClick": "reset",  # 'reset', 'autosize' or 'reset+autosize', False
                        "showTips": False,  # True, False
                        "displayModeBar": True,  # True, False, 'hover'
                        "watermark": True,
                        # 'modeBarButtonsToAdd': ['pan2d','select2d'],
                    },
                    #className="six columns",
                ),
        ),
        dbc.Row(
            dcc.Graph(
                id='split-graph' ,
                figure={},
            )
        ),
        dcc.Markdown('''
        # Comparsion between buy and hold VS arima model 
        Here are some summary data regarding the overall performance 
        '''),
        dcc.Markdown(''' ''' , id="summary_data"),
        dcc.Markdown('''
        # Logger of the simulation 
        Here are the logs of the simulation 
        where one could see where the algorithm did well and when not so well 
        '''),
        html.Div('''''',id='logger') , 
        
    ]
)



@app.callback(
    Output(component_id="inference-graph", component_property="figure"),
    Output(component_id="split-graph", component_property="figure"),
    Output(component_id="summary_data", component_property="children"),
    Output(component_id="logger", component_property="children"),
    Input('range-inference', 'value'),
    Input(component_id="dpdn2", component_property="value"),
)
def update_output(slider_value,country_chosen):
    #print(value)
    dff = df[country_chosen]
    first_date_infer = dff.index[slider_value[0]]
    print(first_date_infer)
    last_date_infer = dff.index[slider_value[1]]
    print(last_date_infer)
    #invest_dates = pd.date_range(start=first_date_infer,end=last_date_infer ,freq="M") 

    predication = pd.DataFrame()
    #concated_data = dff[country][first_date_infer:last_date_infer].copy()
    predication = pd.concat([create_dataframe_with_series(create_auto_arima_prediction_future_2 , dff[country][first_date_infer:last_date_infer].copy()).rename(columns={"High": country, "pred": country +"pred"}) for country in country_chosen])
    #predication.drop(country_chosen, axis=1)
    for country in country_chosen:
        predication[country + "True"] = dff[country][last_date_infer:]
    fig_global = px.line(
        predication,
        #x="Dates",
        #y=["Global Minimum Reg", "High"],
        #hover_data={"Dates": "|%B %d, %Y"},
        title="Inference BackTester",
    )

    fig_global.add_vline(
        x=first_date_infer, line_dash="dash", line_color="Blue"
    )
    fig_global.add_annotation(x=first_date_infer, text=str(first_date_infer))

    fig_global.add_vline(
        x=last_date_infer, line_dash="dash", line_color="Blue"
    )
    fig_global.add_annotation(x=last_date_infer, text=str(last_date_infer))
    
    #strategy_invest(func, series_data , future = 30,start= '2017-12-31', end= '2020-10-11')
    #for country in country_chosen:
    #    predication[country + "True"] = dff[country][last_date_infer:]
    
    combined_figure = go.Figure()
    summary_report = ""
    logger = []
    for country in country_chosen:
        #country = country_chosen[0] # select TA35.TA
        #print(dff[country][first_date_infer:last_date_infer])
        count_invested_months , total_months , expected_diff_arr , revenue_loss_diff_arr , current_date_arr , capital_arr = strategy_invest(create_auto_arima_prediction_future_2 , dff[country].copy(),future = 30,start=first_date_infer, end= last_date_infer)
        
        
        invest_or_not = pd.Series(expected_diff_arr , index=current_date_arr).apply(lambda a: a > 0)
        did_profit = pd.Series(revenue_loss_diff_arr , index=current_date_arr).apply(lambda a: a > 0)

        for curr_date in current_date_arr:
            if invest_or_not[curr_date]:
                fig_global.add_vline(x=curr_date, line_dash="dash", line_color="Red")
                fig_global.add_annotation(x=curr_date,y=dff[country].loc[curr_date:].iloc[0],textangle=-45, text=str(last_date_infer)[:12] + "invest")
            else:
                fig_global.add_vline(x=curr_date, line_dash="dash", line_color="Green")
                fig_global.add_annotation(x=curr_date,y=dff[country].loc[curr_date:].iloc[0] ,textangle=-45,text=str(last_date_infer)[:12] + "not invest")
        
        seg_fig = go.Figure(
            [
            go.Scatter(
                #array = dff[country].loc[start : end],
                x=pd.date_range(start=start,end=end ,freq='B' ),
                #x=[start,end],
                y=dff[country].loc[start : end],
                line_shape="hv",
                line_color=px.colors.qualitative.Plotly[1 if invest_or_not.loc[start] else 0 ] , # color_list[tn]],
                showlegend=False,
                
            )
            for start,end in zip(current_date_arr,current_date_arr[1:])])
        combined_figure.add_traces(seg_fig['data'])
        template = """
        ## Overall profit in percentage with arima : {0}
        ## Overall profit in percentage with buy and hold : {1}
        ## How many months the algorithm decide to invest : {2}
        ## Total month of the entire period : {3}
        ## How many months we had profit : {4}
        """
        summary_report = template.format(
            capital_arr[-1] - 100, 
            (dff[country].loc[last_date_infer:].iloc[0] - dff[country].loc[first_date_infer:].iloc[0])/dff[country].loc[first_date_infer:].iloc[0] *100,
            count_invested_months , 
            total_months ,
            did_profit.value_counts()[True] ,
        )
        #summary_report += '''## Overall profit in percentage with arima :''' + str(capital_arr[-1] - 100 ) + '''\\n'''
        #summary_report += '''## Overall profit in percentage with buy and hold :''' + str(dff[country].loc[last_date_infer:].iloc[0] - dff[country].loc[first_date_infer:].iloc[0]) + '''\\n'''
        for expected_diff , revenue_loss_diff , current_date , capital in zip(expected_diff_arr , revenue_loss_diff_arr , current_date_arr , capital_arr):
            logger.append(html.P("----------------------------------------------------------"+'\n'))
            logger.append(html.P("expected relative diff : "+ str(expected_diff) + '\n'))
            logger.append(html.P("Da facto Revenue/loss " + str(revenue_loss_diff)+ '\n'))
            logger.append(html.P("current date : " + str(current_date) + '\n'))
            logger.append(html.P("current capital: " + str(capital) + '\n'))
    
    #seg_fig = {}
    return fig_global,combined_figure,summary_report,logger

# template = """This is a 
# multiline {0} with
# replacement {1} in."""

# print(template.format("string", "fields"))




# %% ../nbs/03_thesis_app.ipynb 16
if __name__ == "__main__":
    app.run_server(debug=False)
    serve(app.server, host="0.0.0.0", port=8050, threads=2)

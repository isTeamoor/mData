import pandas as pd
from prophet import Prophet

df = pd.read_csv('dataset.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df.rename(columns={'Date':'ds', 'Temp':'y'}, inplace=True)

train = df.copy()
train = train.iloc[:-31]
test = df.copy()
test = test.tail(31)


m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
m.fit(train)
train.to_excel('train.xlsx')
test.to_excel('test.xlsx')
future = m.make_future_dataframe(periods=31)
future.tail()
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
forecast.to_excel('forecast.xlsx')





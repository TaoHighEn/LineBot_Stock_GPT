from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# 透過yfinance取得個股資訊
# ticker股票名稱 start起始日 end迄止日
def get_stock_data(ticker, start, end):
  stock_info = yf.download(ticker, start=start, end=end)
  stock_info = stock_info.rename(str.lower,axis='columns')
  return stock_info

def filter_stocks(df):
  # 設定篩選條件
  rsi_threshold = 20
  macd_threshold = 0
  kd_threshold = 20
  str = []
  if (df['RSI'] is not None):
    if df['RSI'] < rsi_threshold:
      str.append("符合RSI超跌指標")
  if (df['MACD_12_26_9'] is not None):
    if df['MACD_12_26_9'] < macd_threshold:
      str.append("符合MACD超跌指標")
  if (df['STOCHk_14_3_3'] is not None):
    if df['STOCHk_14_3_3'] < kd_threshold:
      str.append("符合KD超跌指標")

  if len(str) == 0:
    str.append("未符合指標")
  return str


def get_stock_name(ticker):
  stock = yf.Ticker(ticker)
  return stock.info.get('longName', "No Name Found")


def get_KD(df):
  return pd.DataFrame(ta.stoch(df['High'], df['Low'], df['Close']))


def calculate_indicators(df):

  t_df = pd.DataFrame()
  t_df['RSI'] = ta.rsi(df['Close'], length=14)
  t_df['MACD'] = ta.macd(df['Close'], length=12, fast=26, slow=9)

  # RSI
  # df['RSI'] = ta.rsi(df['Close'], length=7)
  # # MACD
  # macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
  # df = pd.concat([df, macd], axis=1)
  # # KD
  # stoch = ta.stoch(df['High'], df['Low'], df['Close'])
  # df = pd.concat([df, stoch], axis=1)
  # return df
  return t_df

# 簡單移動平均線SMA
def get_sma_func(df,period=20):
  df0 = df.copy(deep=True)
  return df0.ta.sma(close='close',length=period,append=True)

# 指數移動平均線SMA
def get_ema_func(df,period=20):
  df0 = df.copy(deep=True)
  return df0.ta.ema(period,append=True)

# 相對強度指數RSI
def get_rsi_func(df,period=14):
  df0 = df.copy(deep=True)
  return df0.ta.rsi(period,append=True)

# MACD
def get_macd_func(df,f=12,s=26,sg=9):
  df0 = df.copy(deep=True)
  return df0.ta.macd(fast=f,slow=s,signal=sg,append=True)

# 隨機震盪(K/D)
def get_kd_func(df):
  df0 = df.copy(deep=True)
  return df0.ta.stoch(append=True)

# 平均真實區間
def get_atr_func(df,period=14):
  df0 = df.copy(deep=True)
  return df0.ta.atr(period,append=True)

# 布林通道(Bollinger Bands)
def get_bband_func(df,period=20,multi=1.5):
  df0 = df.copy(deep=True)
  return df0.ta.bbands(period,multi,append=True)

# 現金流(CMF)
def get_cmf_func(df,period=20):
  df0 = df.copy(deep=True)
  return df0.ta.cmf(period,append=True)

# 商品通道指數CCI
def get_cci_func(df,period=20):
  df0 = df.copy(deep=True)
  return df0.ta.cci(period,append=True)

# 個股分析_取得資料表格
def get_stock_info(stock_id,period=90):
  end = datetime.today()
  start = end - timedelta(days=period)
  stock_data = get_stock_data(stock_id, start, end)
  stock_info = all_strategy_info(stock_data)
  return stock_info.tail(5)

def all_strategy_info(df):
  u_df = df.copy(deep=True)
  # u_df = get_sma_func(u_df)
  # u_df = get_ema_func(u_df)
  # u_df = get_rsi_func(df)
  # u_df = get_kd_func(df)
  # u_df = get_macd_func(df)
  # u_df = get_atr_func(u_df)
  # u_df = get_cci_func(u_df)
  # u_df = get_bband_func(u_df)
  # u_df = get_cmf_func(u_df)
  u_df.ta.sma(close='close',append=True)
  u_df.ta.ema(append=True)
  u_df.ta.rsi(append=True)
  u_df.ta.macd(append=True)
  u_df.ta.stoch(append=True)
  u_df.ta.atr(append=True)
  u_df.ta.bbands(append=True)
  u_df.ta.cmf(append=True)
  u_df.ta.cci(append=True)
  return u_df

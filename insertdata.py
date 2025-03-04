import pandas as pd
import yfinance as yf
from database import insert_data

# Download NIFTY 50 data
ticker = yf.Ticker("^NSEI")
df = ticker.history(period="1y")

# Prepare SQL query
sql = "INSERT INTO data (datetime, open, high, low, close) VALUES (%s, %s, %s, %s, %s)"

# Insert into MySQL
for index, row in df.iterrows():
    values = (index.to_pydatetime(), row["Open"], row["High"], row["Low"], row["Close"])
    insert_data(sql, values)

print("✅ NIFTY OHLC data inserted successfully!")

import pandas as pd
from database import fetch_data, insert_data


def calculate_bollinger_bands():
    """Calculate and insert Bollinger Bands into MySQL."""
    # Fetch OHLC data
    df = pd.DataFrame(
        fetch_data("SELECT datetime, close FROM data ORDER BY datetime ASC"),
        columns=["datetime", "close"],
    )
    df.set_index("datetime", inplace=True)

    # Calculate Bollinger Bands
    window = 20
    window_dev = 2
    df["sma"] = df["close"].rolling(window=window).mean()
    df["std"] = df["close"].rolling(window=window).std()
    df["upper"] = df["sma"] + (df["std"] * window_dev)
    df["lower"] = df["sma"] - (df["std"] * window_dev)

    # Insert into MySQL
    sql = "INSERT INTO indicators (datetime, upper, lower, sma) VALUES (%s, %s, %s, %s)"
    for index, row in df.dropna().iterrows():
        insert_data(
            sql, (index.to_pydatetime(), row["upper"], row["lower"], row["sma"])
        )

    print("✅ Bollinger Bands calculated and inserted successfully!")

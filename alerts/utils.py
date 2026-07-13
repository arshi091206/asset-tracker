import yfinance as yf

def get_live_price(ticker):
    try:
        stock=yf.Ticker(ticker)
        history=stock.history(period="1d")
        if history.empty:
            return None
        return history["Close"].iloc[-1]
    except:
        return None


def get_recent_price_points(ticker):
    """Return the five most recent available daily closing prices."""
    try:
        history = yf.Ticker(ticker).history(period="10d", interval="1d")
        if history.empty:
            return []

        recent_history = history.tail(5)
        return [
            {
                "label": date.strftime("%d %b"),
                "price": round(float(row["Close"]), 2),
            }
            for date, row in recent_history.iterrows()
        ]
    except:
        return []

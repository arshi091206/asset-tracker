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
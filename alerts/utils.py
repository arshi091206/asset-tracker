import yfinance as yf

def get_live_price(ticker):
    try:
        stock=yf.Ticker(ticker)
        return stock.info["currentPrice"]
    except:
        return None
import yfinance as yf

def fetch_stocks(stock_universe):
        # Manual lists of stock tickers for each universe
        stock_universe_mapping = {
            "IHSG": ["BBCA", "BBRI", "TLKM"],  # Example tickers for IHSG
            "LQ45": ["ACES", "ADRO", "AKRA", "AMRT", "ANTM", "ARTO", "ASII", "BBCA", "BBNI", "BBRI", "BBTN", "BMRI", "BRIS", "BRPT", "BUKA", "CPIN", "EMTK", "ESSA", "EXCL", "GGRM", "GOTO", "HRUM", "ICBP", "INCO", "INDF", "INKP", "INTP", "ITMG", "KLBF", "MAPI", "MBMA", "MDKA", "MEDC", "MTEL", "PGAS", "PGEO", "PTBA", "PTMP", "SIDO", "SMGR", "SRTG", "TLKM", "TOWR", "UNTR", "UNVR"],
            "Syariah": ["TLKM", "BRIS"]  # Example tickers for Syariah
        }
        tickers = [ticker + ".JK" for ticker in stock_universe_mapping.get(stock_universe, [])]
        stocks = {ticker: yf.Ticker(ticker).info for ticker in tickers}
        return stocks

def apply_filter(stocks, feature, operator, value1, value2=None):
        if operator == '>':
            filtered_stocks = {ticker: info for ticker, info in stocks.items() if info.get(feature, 0) > value1}
        elif operator == '<':
            filtered_stocks = {ticker: info for ticker, info in stocks.items() if info.get(feature, 0) < value1}
        elif operator == '>=':
            filtered_stocks = {ticker: info for ticker, info in stocks.items() if info.get(feature, 0) >= value1}
        elif operator == '<=':
            filtered_stocks = {ticker: info for ticker, info in stocks.items() if info.get(feature, 0) <= value1}
        elif operator == '=':
            filtered_stocks = {ticker: info for ticker, info in stocks.items() if info.get(feature, 0) == value1}
        elif operator == 'between':
            filtered_stocks = {ticker: info for ticker, info in stocks.items() if value1 <= info.get(feature, 0) <= value2}
        else:
            filtered_stocks = stocks
        return filtered_stocks
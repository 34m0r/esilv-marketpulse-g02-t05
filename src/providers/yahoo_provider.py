"""Yahoo Finance market data provider for MarketPulse."""

import yfinance as yf

# Mapping between MarketPulse canonical tickers and Yahoo Finance symbols
YAHOO_SYMBOL_MAPPING = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(
    symbol,
    canonical_ticker,
    period="1mo",
    interval="1d",
):
    """
    Retrieve historical market prices from Yahoo Finance and normalize to canonical format.

    Args:
        symbol (str): Yahoo Finance symbol (e.g., 'AAPL' or '^GSPC').
        canonical_ticker (str): Internal canonical ticker (e.g., 'AAPL' or 'SP500').
        period (str): Historical lookback window (default: '1mo').
        interval (str): Price frequency (default: '1d').

    Returns:
        list: Canonical observation dictionaries dict(date, ticker, open, high, low, close, volume).
    """
    history = yf.Ticker(symbol).history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )

    if history.empty:
        raise ValueError(
            f"No Yahoo Finance data returned for symbol {symbol} "
            f"(period={period}, interval={interval})."
        )

    rows = []
    for timestamp, row in history.iterrows():
        rows.append({
            "date": timestamp.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    return rows


def fetch_prices_for_ticker(
    ticker,
    period="1mo",
    interval="1d",
):
    """
    Retrieve prices using only the MarketPulse ticker (e.g. 'AAPL' or 'SP500').

    Raises:
        ValueError: If the ticker is not in YAHOO_SYMBOL_MAPPING.
    """
    if ticker not in YAHOO_SYMBOL_MAPPING:
        raise ValueError(
            f"Unknown ticker '{ticker}'. "
            f"Supported tickers: {', '.join(YAHOO_SYMBOL_MAPPING)}."
        )

    return fetch_yahoo_prices(
        symbol=YAHOO_SYMBOL_MAPPING[ticker],
        canonical_ticker=ticker,
        period=period,
        interval=interval,
    )


def main():
    """Display the instrument and the benchmark over the same 1 month / daily window."""
    print("MarketPulse - Yahoo Finance stage (remote data)")
    print("Lookback : 1 month | Interval : Daily")
    print()
    for role, ticker in [("Instrument", "AAPL"), ("Benchmark", "SP500")]:
        rows = fetch_prices_for_ticker(ticker, period="1mo", interval="1d")
        print(f"{role:<10} : {ticker} ({YAHOO_SYMBOL_MAPPING[ticker]})")
        print(f"  Observations : {len(rows)}  ({rows[0]['date']} -> {rows[-1]['date']})")
        print(f"  First close  : {rows[0]['close']:.2f}")
        print(f"  Last close   : {rows[-1]['close']:.2f}")
        print()


if __name__ == "__main__":
    main()

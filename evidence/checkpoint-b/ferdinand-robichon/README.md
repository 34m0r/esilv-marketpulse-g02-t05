# Checkpoint B - Ferdinand-robichon

Status: COMPLETE

- `01_pull_request.png` : PR #6 `feature/yahoo-provider` -> `main`, merged (Yahoo provider + `fetch_prices_for_ticker`)
- `02_code_review.png` : my review on PR #5 by 34m0r (Bloomberg field mapping), approved with comments
- `03_yahoo_market_data.png` : `python tests/validate_yahoo_provider.py`, real remote Yahoo data (AAPL, SP500, UNKNOWN -> ValueError)
- `04_instrument_benchmark.png` : `python src/providers/yahoo_provider.py`, AAPL + SP500 over the same 1 month / daily window

Where Yahoo Finance is called: `src/providers/yahoo_provider.py`, `fetch_yahoo_prices()`.

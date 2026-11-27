"""TD08 - Validation de fetch_prices_for_ticker() (appel réel à Yahoo Finance)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from providers.yahoo_provider import fetch_prices_for_ticker

EXPECTED_KEYS = {"date", "ticker", "open", "high", "low", "close", "volume"}

# AAPL
apple = fetch_prices_for_ticker("AAPL")
assert len(apple) > 0
assert set(apple[0]) == EXPECTED_KEYS
assert all(row["ticker"] == "AAPL" for row in apple)
print(f"AAPL 1mo : {len(apple)} lignes, {apple[0]['date']} -> {apple[-1]['date']}")

# SP500
sp500 = fetch_prices_for_ticker("SP500")
assert len(sp500) > 0
assert all(row["ticker"] == "SP500" for row in sp500)
print(f"SP500 1mo : {len(sp500)} lignes, {sp500[0]['date']} -> {sp500[-1]['date']}")

# period / interval transmis
apple_3_months = fetch_prices_for_ticker("AAPL", period="3mo", interval="1d")
assert len(apple_3_months) > len(apple)
print(f"AAPL 3mo : {len(apple_3_months)} lignes")

# ticker inconnu
try:
    fetch_prices_for_ticker("UNKNOWN")
    raise AssertionError("UNKNOWN aurait dû lever une ValueError")
except ValueError as error:
    print(f"UNKNOWN -> ValueError : {error}")

print("Tous les tests TD08 ont réussi.")

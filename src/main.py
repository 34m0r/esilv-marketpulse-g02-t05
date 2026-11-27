"""MarketPulse - application orchestrator and terminal snapshot.

Run from the repository root:  python src/main.py
"""

from pathlib import Path
import json
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analytics import (  # noqa: E402
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from src.providers.bloomberg_provider import fetch_bloomberg_prices  # noqa: E402

DATA_DIR = ROOT_DIR / "data" / "sample"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "Bloomberg stage - APPROVED_SAMPLE"


def load_instruments():
    """Load instrument and benchmark metadata from JSON."""
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot(provider_mode="APPROVED_SAMPLE"):
    """
    Build the MarketPulse application snapshot.

    The same dictionary is used by the terminal output and by the Dash dashboard.
    """
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    raw_instrument = fetch_bloomberg_prices(instrument["ticker"], mode=provider_mode)
    raw_benchmark = fetch_bloomberg_prices(benchmark["ticker"], mode=provider_mode)

    aligned_instrument, aligned_benchmark = align_series(raw_instrument, raw_benchmark)

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    provider_name = PROVIDER_LABEL if provider_mode == "APPROVED_SAMPLE" else "Bloomberg - LIVE"

    return {
        "provider": provider_name,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": {
            "ticker": instrument["ticker"],
            "name": instrument["name"],
            "currency": instrument.get("currency", "USD"),
        },
        "benchmark": {
            "ticker": benchmark["ticker"],
            "name": benchmark["name"],
        },
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(instrument_return, benchmark_return),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def print_market_snapshot(snapshot):
    """Print the snapshot as a readable terminal summary."""
    inst = snapshot["instrument"]
    bm = snapshot["benchmark"]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider : {snapshot['provider']}")
    print(f"Period   : {snapshot['lookback']}")
    print(f"Interval : {snapshot['interval']}")
    print()
    print("Instrument")
    print(f"{inst['ticker']} - {inst['name']}")
    print(f"Observations : {len(snapshot['instrument_base_100'])}")
    print(f"Period return: {snapshot['instrument_return']:+.2f}%")
    print()
    print("Benchmark")
    print(f"{bm['ticker']} - {bm['name']}")
    print(f"Observations : {len(snapshot['benchmark_base_100'])}")
    print(f"Period return: {snapshot['benchmark_return']:+.2f}%")
    print()
    print("Performance comparison")
    print(f"Relative performance: {snapshot['relative_performance']:+.2f} percentage points")


def main():
    snapshot = build_market_snapshot()
    print_market_snapshot(snapshot)


if __name__ == "__main__":
    main()

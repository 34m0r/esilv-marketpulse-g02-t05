"""TD07 - Validation du module src/analytics.py avec des séries fictives."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


def make_series(ticker, dates, closes):
    return [
        {"date": d, "ticker": ticker, "open": c, "high": c, "low": c, "close": c, "volume": 0}
        for d, c in zip(dates, closes)
    ]


dates = ["2026-01-02", "2026-01-03", "2026-01-04"]
instrument = make_series("AAPL", dates, [100.0, 110.0, 121.0])
benchmark = make_series("SP500", dates, [200.0, 210.0, 220.0])

# 1. Rendement : 121 / 100 - 1 = +21 %, 220 / 200 - 1 = +10 %
instrument_return = calculate_period_return(instrument)
benchmark_return = calculate_period_return(benchmark)
assert math.isclose(instrument_return, 21.0)
assert math.isclose(benchmark_return, 10.0)

# 2. Base 100 : 100, 110, 121
base_100 = [row["value"] for row in calculate_base_100(instrument)]
assert all(math.isclose(a, b) for a, b in zip(base_100, [100.0, 110.0, 121.0]))

# 3. Performance relative : 21 - 10 = 11 points
assert math.isclose(calculate_relative_performance(instrument_return, benchmark_return), 11.0)

# 4. align_series avec des dates différentes (seules 01-03 et 01-04 sont communes)
other_benchmark = make_series("SP500", ["2026-01-03", "2026-01-04", "2026-01-05"], [210.0, 220.0, 230.0])
aligned_instrument, aligned_benchmark = align_series(instrument, other_benchmark)
assert [r["date"] for r in aligned_instrument] == ["2026-01-03", "2026-01-04"]
assert [r["date"] for r in aligned_benchmark] == ["2026-01-03", "2026-01-04"]

# 5. Série vide -> ValueError
try:
    calculate_period_return([])
    raise AssertionError("Une série vide aurait dû lever une ValueError")
except ValueError:
    pass

print("Tous les tests TD07 ont réussi.")

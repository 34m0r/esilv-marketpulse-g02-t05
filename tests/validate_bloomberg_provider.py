"""TD10 - Validation de src/providers/bloomberg_provider.py.

À lancer depuis la racine du dépôt : py tests/validate_bloomberg_provider.py
Mode testé : APPROVED_SAMPLE (pas de connexion Bloomberg LIVE).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.providers.bloomberg_provider import (
    fetch_bloomberg_prices,
    normalize_reference_series,
)


def expect_value_error(series, label):
    try:
        normalize_reference_series(series)
    except ValueError as exc:
        print(f"{label} : ValueError OK ({exc})")
    else:
        raise AssertionError(f"{label} : ValueError attendue")


def fake_observation(date="2026-11-18"):
    return {
        "observation_date": date,
        "open_value": "100.0", "high_value": "112.0",
        "low_value": "99.0", "close_value": "110.0",
        "volume_value": "1500",
    }


# 1. Observation complète (données fictives) -> liste canonique valide
rows = normalize_reference_series({"canonical_ticker": "AAPL", "observations": [fake_observation()]})
assert len(rows) == 1
assert set(rows[0]) == {"date", "ticker", "open", "high", "low", "close", "volume"}
assert rows[0]["ticker"] == "AAPL"
assert rows[0]["date"] == "2026-11-18"
assert rows[0]["close"] == 110.0
assert isinstance(rows[0]["close"], float)
assert isinstance(rows[0]["volume"], int)
print("Observation complète : OK")

# 2. Liste observations vide
expect_value_error({"canonical_ticker": "AAPL", "observations": []}, "Liste vide")

# 3. close_value absent
obs = fake_observation()
del obs["close_value"]
expect_value_error({"canonical_ticker": "AAPL", "observations": [obs]}, "close_value absent")

# 4. Deux dates identiques
expect_value_error(
    {"canonical_ticker": "AAPL", "observations": [fake_observation(), fake_observation()]},
    "Dates dupliquées",
)

# 5. Échantillon approuvé du dépôt
aapl = fetch_bloomberg_prices("AAPL", mode="APPROVED_SAMPLE")
sp500 = fetch_bloomberg_prices("SP500", mode="APPROVED_SAMPLE")
assert len(aapl) > 0 and len(sp500) > 0
assert all(row["ticker"] == "AAPL" for row in aapl)
assert all(row["ticker"] == "SP500" for row in sp500)

# 6. Comparaison effective avec le fichier expected
expected = json.loads((ROOT / "data/sample/bloomberg_reference_expected.json").read_text(encoding="utf-8"))
assert aapl + sp500 == expected["rows"], "Les lignes normalisées diffèrent du fichier expected"

# 7. LIVE n'est pas simulé
try:
    fetch_bloomberg_prices("AAPL", mode="LIVE")
    raise AssertionError("LIVE ne doit pas réussir sans terminal")
except NotImplementedError:
    pass

print("Bloomberg stage - APPROVED_SAMPLE")
print("AAPL:", len(aapl), "SP500:", len(sp500))
print("Lignes identiques au fichier expected :", len(expected["rows"]))
print("Tous les tests TD10 ont réussi.")

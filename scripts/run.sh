#!/usr/bin/env bash
# MarketPulse - reproducible run from a clean clone.
# Usage: ./scripts/run.sh            -> install, check, terminal snapshot
#        ./scripts/run.sh dashboard  -> same, then start the Dash dashboard
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -q -r requirements.txt

python tests/validate_analytics.py
python tests/validate_bloomberg_provider.py
python src/main.py

if [ "${1:-}" = "dashboard" ]; then
    python src/dashboard.py
fi

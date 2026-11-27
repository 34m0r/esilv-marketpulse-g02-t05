# Bloomberg Field Mapping

## 1. Objectif et modes autorisés

Le fournisseur Bloomberg doit renvoyer les mêmes données que le fournisseur Yahoo.
Comme ça, `analytics.py` marche sans changement, quelle que soit la source.

Deux modes :

| Mode | Source | Terminal Bloomberg ? |
|---|---|---|
| `APPROVED_SAMPLE` (par défaut) | `data/sample/bloomberg_reference_sample.json` | Non |
| `LIVE` | Terminal Bloomberg autorisé | Oui |

Le mode `LIVE` n'est pas implémenté : il lève `NotImplementedError`.

## 2. Identifiants AAPL / SP500

| Ticker MarketPulse | Identifiant Bloomberg | Instrument |
|---|---|---|
| `AAPL` | `AAPL US Equity` | Apple Inc. (action) |
| `SP500` | `SPX Index` | S&P 500 (indice) |

- Dans le JSON, une série se trouve avec sa clé `provider_identifier`.
- Dans les observations finales, on met toujours le ticker MarketPulse (`AAPL`, `SP500`), jamais l'identifiant Bloomberg.

Structure du JSON :

```
series[]
├── provider_identifier   "AAPL US Equity"
├── canonical_ticker      "AAPL"
└── observations[]        une ligne par jour
```

## 3. Correspondance des champs et types

| Champ Bloomberg | Champ MarketPulse | Type |
|---|---|---|
| `observation_date` | `date` | `str` (AAAA-MM-JJ) |
| `canonical_ticker` | `ticker` | `str` |
| `open_value` | `open` | `float` |
| `high_value` | `high` | `float` |
| `low_value` | `low` | `float` |
| `close_value` | `close` | `float` |
| `volume_value` | `volume` | `int` |

- `canonical_ticker` est au niveau de la série, pas dans chaque observation.
- Les nombres doivent être convertis avec `float()` et `int()`, sinon les calculs peuvent échouer.
- Le volume de `SPX Index` vaut `0` : c'est un indice, ce n'est pas une erreur.

## 4. Exemple fictif : brut → canonique

Données fictives, pas une extraction Bloomberg.

Avant :

```python
{
    "observation_date": "2026-11-18",
    "open_value": "100.0",
    "high_value": "112.0",
    "low_value": "99.0",
    "close_value": "110.0",
    "volume_value": "1500",
}
```

Après (série `AAPL US Equity`) :

```python
{
    "date": "2026-11-18",
    "ticker": "AAPL",
    "open": 100.0,
    "high": 112.0,
    "low": 99.0,
    "close": 110.0,
    "volume": 1500,
}
```

## 5. Vérifications et limites du mode LIVE

À vérifier sur chaque observation :

- Elle a exactement les 7 clés : `date`, `ticker`, `open`, `high`, `low`, `close`, `volume`.
- `ticker` vaut `AAPL` ou `SP500`.
- Les prix sont des `float` et le volume un `int`.
- Le résultat est égal à `data/sample/bloomberg_reference_expected.json` (il faut comparer les valeurs, pas seulement vérifier que le fichier existe).

Limites :

- Le JSON approuvé contient des valeurs pédagogiques, pas de vraies données Bloomberg.
- `LIVE` demande un Terminal autorisé. On ne simule jamais une connexion réussie.
- Sur chaque capture, on indique le mode réellement utilisé.

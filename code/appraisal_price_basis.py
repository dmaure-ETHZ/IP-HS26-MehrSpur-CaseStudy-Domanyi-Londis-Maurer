"""Reproducible conversion of appraisal unit values to constant 2025 CHF.

BFS annual-average total CPI, December 2015 = 100 (published precision).
Source: https://dam-api.bfs.admin.ch/hub/api/dam/assets/36970588/master
Table Index_y; retrieved 2026-11-16. Inflation only; no real-value growth.
NIBA 2016 guide, chapter 7 / appendix 2: prices 2014, real values 2030.
https://www.bav.admin.ch/dam/de/sd-web/rQmEiJ-XxI41/niba-leitfaden.pdf
"""
APPRAISAL_PRICE_YEAR = 2025
ANNUAL_CPI = {2014: 99.0, 2021: 99.1, 2025: 105.4}
SOURCE_PRICE_YEARS = {
    **dict.fromkeys(("C_TT_CAR", "C_TT_PT", "C_TT_PT_WAITING",
        "C_TT_PT_ACCESS", "C_TT_PT_TRANSFER", "C_NOISE_CAR", "C_AIR_CAR",
        "C_ACCIDENT_CAR", "C_AIR_PT", "C_NOISE_PT", "C_ACCIDENT_PT"), 2014),
    **dict.fromkeys(("BENEFIT_HEALTH_BIKE_PER_KM", "BENEFIT_HEALTH_WALK_PER_KM",
        "CO2_VALUE_CHF_PER_TONNE"), 2021),
    # No original price year is documented for these project assumptions.
    # Explicit convention: interpret the existing 35/16 CHF rates as 2025 prices.
    "C_TT_BIKE": 2025, "C_TT_WALK": 2025,
}
PRICE_FACTORS = {key: ANNUAL_CPI[APPRAISAL_PRICE_YEAR] / ANNUAL_CPI[year]
                 for key, year in SOURCE_PRICE_YEARS.items()}

def harmonize_nominal(values):
    """Convert freshly defined source values once; never pass converted values."""
    return {key: value * PRICE_FACTORS[key] if key in PRICE_FACTORS else value
            for key, value in values.items()}

def harmonize_uncertainties(registry):
    """Convert absolute monetary sensitivity bounds, retaining relative spreads.

Carbon sensitivity bounds are scenario assumptions expressed in 2021 CHF,
including the 140 CHF/t lower assumption; not a separately dated price quote.
"""
    for key, spec in registry.items():
        if key not in PRICE_FACTORS:
            continue
        for field in ("minimum", "maximum", "mode", "mean", "sigma"):
            if field in spec and not (field == "sigma" and spec.get("relative_sigma")):
                spec[field] *= PRICE_FACTORS[key]

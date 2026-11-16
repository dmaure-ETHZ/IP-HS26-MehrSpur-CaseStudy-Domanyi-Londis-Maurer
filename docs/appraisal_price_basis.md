# Appraisal price basis: constant 2025 CHF

All monetary appraisal unit values are expressed in 2025 purchasing power. Conversion uses the BFS annual-average total consumer price index (CPI), December 2015 = 100, at published precision. This is an explicit project convention for harmonising general purchasing power, not a sector-specific re-estimation of the original valuation rates.

| Source price year | Annual CPI | Factor to 2025 |
|---|---:|---:|
| 2014 | 99.0 | 105.4 / 99.0 = 1.06464646 |
| 2021 | 99.1 | 105.4 / 99.1 = 1.06357215 |
| 2025 | 105.4 | 1 |

BFS source: [Total index on all index bases](https://dam-api.bfs.admin.ch/hub/api/dam/assets/36970588/master), sheet `Index_y`, retrieved 16 November 2026. These are annual averages, not December observations. The fixed indices and conversion rules are in `code/appraisal_price_basis.py`; no network access is needed to run the model.

## Scope and assumptions

- Car/PT time, PT component time and road/rail noise, air pollution and accident coefficients inherit the NIBA price basis **2014**. The [BAV NIBA guide, December 2016](https://www.bav.admin.ch/dam/de/sd-web/rQmEiJ-XxI41/niba-leitfaden.pdf), chapter 7 and appendix 2, distinguishes **prices 2014** from **real values 2030**. CPI conversion changes only the price unit; the original real-value assumptions remain. Earlier notebook wording describing these rates collectively as 2019 CHF was incorrect.
- The group's ARE 2021 net cycling/walking health rates and carbon rate are interpreted in source-year 2021 CHF, then converted. This preserves the existing coefficients and methods rather than replacing them with a newer external-cost study. The general ARE source is [External costs and benefits of transport](https://www.are.admin.ch/de/kosten-nutzen).
- The existing cycling/walking time values, CHF 35/16 per person-hour, have no documented original price year. They are explicitly interpreted as **2025 project assumptions**, not as independently sourced 2025 estimates. The CHF 2 million option premium is likewise a 2025 project assumption.
- Package CAPEX is already indexed to 2025 in `stages.py`. It is not indexed twice. OPEX follows that CAPEX through the existing rate. CAPEX/OPEX multipliers, physical construction emissions, residual capital shares, asset lives, the discount rate and annualisation are unchanged.
- Absolute monetary sensitivity bounds for car/PT time and carbon receive the same factor as their nominal coefficient. In particular, the carbon lower bound of CHF 140/t is treated as an assumed bound in **2021 CHF**, not as a separately dated historical quote. Dimensionless and physical uncertainty distributions are unchanged.
- Carbon's calendar reference remains **2021**; its price basis becomes **2025**. The configured real annual escalation remains zero. CPI is not added again along the 40-year horizon, and the 2% discount rate remains real.

## Execution and implications

`parameters.py` converts freshly defined source-value literals once before exporting module-level values, then converts the freshly defined sensitivity registry before configuration. Re-import/reload must not compound inflation. Source literals remain readable; effective imported rates differ from them by the recorded factor. For example, car/PT time become approximately CHF 45.2901/28.2344 per hour, net cycling health CHF 0.308436/km, and carbon CHF 457.336/t.

NB05 exports source years, source values, conversion factors and effective values in `05_price_basis_conversion.csv`, together with effective valuation inputs and the complete assumption handover. Its accounting cache is rebuilt after the configuration change. Annual GP-versus-reference appraisal diagnostics are also recomputed from the existing saved OD cases. No new transport assignment or surrogate training is performed.

Physical outputs, plan timings, NB04 scenario IDs, requirements and investment/operating-cost inputs are checked against the saved NB04 experiment. Monetary benefits, NPVs, BCRs, regret and monetary audit errors change. Earlier saved monetary outputs from other notebooks are historical outputs on the previous basis; rerun their monetary displays if they are reused in the report. Other team members must rerun NB05 analyses/sensitivity after this change so results use the same price basis. Harmonisation alone does not cure the existing surrogate accuracy limitations.

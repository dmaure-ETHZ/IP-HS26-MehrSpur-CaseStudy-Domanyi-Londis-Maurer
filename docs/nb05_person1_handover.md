# NB05 work package 1: appraisal preparation and plan comparison

Completed sections: 1.1, 1.3, 1.4, 2.1, 2.2 and 2.5. Supporting sections 1.2, 2.3 and 2.4 are configured/executed for consistent displays. Parts 3–5 are unchanged and remain with the other work packages.

## Experiment

The appraisal imports the saved NB04 experiment: 200 LHS futures, seed 42, six plans, logistic e-bike and car-emission-factor paths, other transient inputs linear. Requirement: cycling trip share >=22% in every year from 30 through 40. The 22% level is an internal model-based reference, not a policy target. Walking and short trips remain in its denominator. Monitoring thresholds 17,000/20,000 peak-hour bicycle trips, persistence two years, lead times four/six years.

Use the completed NB04 export files from one run. Existing local NB04 exports have IDs 0–199; committed earlier exports may use 200–399. The loader now accepts unique integer IDs without renumbering and validates their paired outcomes and dates. IDs from different runs must not be mixed. Published NB05 outputs were verified and regenerated against the committed main NB04 inputs (IDs 200–399); local NB04 reruns were preserved. Input hashes, original IDs, applied endpoints and assumptions are recorded in `results/05_appraisal/05_case_assumptions_and_handover.json`.

NB03's surrogate and response table are loaded, never retrained. `RECHECK_GP_APPRAISAL` remains false. NB02–NB04 notebooks and their exports remain unchanged by this work package. The later authorised harmonisation changes appraisal-only unit values in `parameters.py` and corrects the carbon price-basis docstring; no transport model is refitted.

## Case-specific implementation fixes

- NB04 package columns are East/West stretch; legacy Station/Tunnel aliases remain supported.
- Imported scenario IDs are preserved in cache integrity checks.
- Inactive-section displays preserve section identity metadata required by matched-welfare checks. The original template replaced the identity with NaN, causing the baseline/project comparison to fail even with both sections disabled.
- Standalone fallback uses the cycling case's requirement and shapes; requested-but-missing NB04 input stops instead of silently changing experiments.
- Plan labels and parallel-coordinate cycling axes reflect the cycling project.

## Results and interpretation

All amounts are constant 2025 MCHF (see `docs/appraisal_price_basis.md`).

| Plan | Mean NPV | Positive NPV | All assessment years meet requirement |
|---|---:|---:|---:|
| Baseline | 0.00 | 0% (neutral zero) | 38.5% |
| East | 186.12 | 100% | 44.0% |
| Full route | 267.38 | 100% | 46.5% |
| Staged 1, early | 223.23 | 100% | 46.5% |
| Staged 2, expected demand | 99.17 | 100% | 44.0% |
| Adaptive | 55.63 | 80% | 44.0% |

Full route has zero regret in every tested future and is the sample minimax-regret alternative among the six original plans. This is not a final recommendation or a guarantee outside the sample. Staged 2 and Adaptive have crossing empirical NPV distributions. Final conclusions also require waiting, sensitivity and unpriced-effect evidence from the other packages.

Full-route value is led by cycling time (215.47), road time (52.77) and cycling health (44.14), partly offset by paid CAPEX (40.66), OPEX (8.51), walking-health losses (6.99) and construction carbon (0.81); residual credit is 1.88. The BCR is about 6.65, calculated as ensemble mean benefits divided by mean net agency costs. East has a higher BCR (7.88) but lower total NPV. Adaptive's BCR is 3.95. The separate agency-cost export isolates time-zero premiums from construction investment; they are otherwise combined in the engine's investment component.

## Limitations that must remain visible

1. **Appraisal accuracy does not meet the complete NB05 acceptance rule.** Saved total annual-benefit MAE is 0.680 MCHF/year divided by 8.925 MCHF/year mean absolute reference benefit: 7.61%, above 2%. OD-output accuracy also warns. Reference convergence, zero material sign errors and the large-error P95 safeguard pass. Cycling-time MAE is only about CHF 2,118/year (0.031% of its mean absolute reference); road-time MAE is about 1.072 MCHF/year (83% of its mean absolute reference). These checks concern annual saved test cases, not each scenario NPV or interpolation accuracy. Course feedback says further training is unnecessary; that does not turn the failed acceptance test into a pass.
2. **Harmonised price basis.** NIBA rates in source prices 2014 and ARE health/carbon rates in source prices 2021 are CPI-converted to 2025 CHF. Source price years are distinct from real valuation/calendar reference years. Cycling/walking time rates and the option premium are explicitly interpreted as 2025 project assumptions. CAPEX already uses 2025 prices; no second indexing is applied. Absolute monetary sensitivity bounds use the same conversion. See `docs/appraisal_price_basis.md` and the exported conversion register. Other NB05 work packages must rerun their monetary analyses with this configuration.
3. **Horizon accounting.** CAPEX at opening, annual OPEX, time-zero option premiums, construction-year carbon and terminal residual credits are distinct. Commitments opening after Year 40 have no in-horizon opening CAPEX but can have in-horizon construction emissions. Adaptive premiums remain payable even without construction.
4. **Physical target is separate from value.** Positive NPV is not evidence of requirement protection. Meeting the target is not an extra monetary benefit. Baseline zero NPV is not economic loss.

## Reuse

Run Setup, supporting functions and Parts 1–2 in order. Keep `USE_NB04_OUTPUTS=True` and `USE_CACHED_DATASET=True`. With an unchanged configuration the local appraisal cache is reused. Missing or stale appraisal caches are rebuilt from the saved response table, not from new assignment/training. Parts 3–5 can then use `df`, `traj_df`, `tunnel_reference_df`, the requirement definitions and the component/regret tables.

Shared comparator defaults remain Staged 1 and Static 2 as in the exercise; coordinate any change in Section 1.2 across subsequent analyses. Do not edit permanent physical stage effects or trigger rules merely to improve an economic ranking.

Tables/metadata are in `results/05_appraisal/`, figures in `figures/05_appraisal/`, and local reusable caches in `cache/05_appraisal/`. Full monetary inputs and units are exported. No final report files were edited and no commit/push was performed.

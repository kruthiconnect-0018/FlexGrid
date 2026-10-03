# Methodology

Baseline unmet energy is max(demand - solar, 0) summed over time.

FlexGrid forecasts near-term solar and demand, shifts part of flexible demand,
then dispatches the shared battery for remaining shortfall while maintaining
a reserve. Results are compared against the baseline.

The controller is deliberately rule-based and explainable for the first
prototype. More advanced optimization/forecasting can replace it later.

import numpy as np
from scipy.optimize import minimize


def find_best_allocation(total_cash, accounts, tax_engine):
    # accounts is a list of dicts: {'name': str, 'rate': float, 'is_isa': bool}
    rates = np.array([a["rate"] for a in accounts])
    is_isa = np.array([a["is_isa"] for a in accounts])

    def objective(weights):
        balances = weights * total_cash
        interest = balances * (rates / 100)

        isa_int = np.sum(interest[is_isa])
        taxable_int = np.sum(interest[~is_isa])

        # Calculate Tax
        taxable_above_psa = max(0, taxable_int - tax_engine.psa)
        tax_due = taxable_above_psa * tax_engine.rate

        return -((isa_int + taxable_int) - tax_due)

    # Constraints: Sum of weights = 1
    cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1}

    # Bounds: ISA weight limit vs others
    bounds = []
    for a in accounts:
        if a["is_isa"]:
            bounds.append((0, min(1.0, tax_engine.isa_limit / total_cash)))
        else:
            bounds.append((0, 1.0))

    res = minimize(
        objective, [1 / len(accounts)] * len(accounts), bounds=bounds, constraints=cons
    )
    return res.x * total_cash

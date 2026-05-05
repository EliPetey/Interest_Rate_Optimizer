import numpy as np
from scipy.optimize import minimize


def find_best_allocation(total_cash, accounts, tax_engine):
    """
    accounts is a list of dicts: {'name': str, 'rate': float, 'is_isa': bool}
    total_cash: Sum of all current balances
    tax_engine: Instance of UKTax2026
    """
    rates = np.array([a["rate"] for a in accounts])
    is_isa = np.array([a["is_isa"] for a in accounts])

    def objective(weights):
        # 1. Distribute total liquid wealth based on solver's current 'guess'
        balances = weights * total_cash

        # 2. Calculate Gross Interest
        interest_per_acc = balances * (rates / 100)

        # 3. Categorize Interest for Tax
        isa_interest = np.sum(interest_per_acc[is_isa])
        taxable_interest = np.sum(interest_per_acc[~is_isa])

        # 4. Apply Personal Savings Allowance (PSA)
        # NI is not paid on savings interest, only income tax.
        taxable_above_psa = max(0, taxable_interest - tax_engine.psa)
        interest_tax_due = taxable_above_psa * tax_engine.income_tax_rate

        # 5. Calculate Net Gain
        net_interest = (isa_interest + taxable_interest) - interest_tax_due

        # Minimize the negative to maximize the profit
        return -net_interest

    # Constraints: Sum of weights = 1
    cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1}

    # Bounds: ISA weight limit vs others
    bounds = []
    for a in accounts:
        if a["is_isa"]:
            bounds.append((0, min(1.0, tax_engine.isa_limit / total_cash)))
        else:
            bounds.append((0, 1.0))

    # Initial Guess: Spread money evenly
    num_acc = len(accounts)
    initial_guess = [1.0 / num_acc] * num_acc

    result = minimize(
        objective,
        initial_guess,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        tol=1e-9,
    )
    return result.x * total_cash

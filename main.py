from engine.tax_logic import UKTax2026
from engine.optimizer import find_best_allocation


def run_app():
    print("--- Interest Rate Optimizer (UK 2026) ---")
    salary = float(input("Enter your yearly salary: £"))
    total_cash = float(input("Enter total cash to allocate: £"))

    tax_engine = UKTax2026(salary)

    accounts = []
    num_banks = int(input("How many bank accounts to compare? "))
    for i in range(num_banks):
        name = input(f"Bank {i+1} Name: ")
        rate = float(input(f"Bank {i+1} Interest Rate (%): "))
        isa_q = input(f"Is {name} an ISA account? (y/n): ").lower()
        accounts.append({"name": name, "rate": rate, "is_isa": isa_q == "y"})

    results = find_best_allocation(total_cash, accounts, tax_engine)

    print("\n--- OPTIMIZED PLAN ---")
    for i, bal in enumerate(results):
        if bal > 0.01:
            print(f"{accounts[i]['name']}: £{bal:,.2f}")

    if __name__ == "__main__":
        run_app()

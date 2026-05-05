from engine.tax_logic import UKTax2026
from engine.optimizer import find_best_allocation


def run_app():
    print("--- Interest Rate Optimizer (UK 2026) ---")
    salary = float(input("Enter your yearly salary: £"))
    total_cash = float(input("Enter total cash to allocate: £"))

    try:
        # 1. Inputs
        salary = float(input("Enter your annual gross salary: £"))

        # 2. Setup Tax Engine
        tax_engine = UKTax2026(salary)
        base_take_home = tax_engine.get_take_home_salary()

        print(f"Your Take-Home Salary (After Tax & NI): £{base_take_home:,.2f}")

        # 3. Gather Bank Options & Current Balances
        accounts = []
        num_banks = int(input("How many bank accounts to compare? "))
        total_cash = 0

        for i in range(num_banks):
            name = input(f"Bank {i+1} Name: ")
            current_bal = float(input(f" Current Balance in {name}: £"))
            rate = float(input(f"Bank {i+1} Interest Rate (%): "))
            isa_q = input(f"Is {name} an ISA account? (y/n): ").lower()
            accounts.append(
                {
                    "name": name,
                    "rate": rate,
                    "is_isa": isa_q == "y",
                    "current_bal": current_bal,
                }
            )

            total_cash += current_bal

        print(f"\nTotal Net Worth detected: £{total_cash:,.2f}")
        print("Calculating Optimal Rebalancing...")

        # 4. Run Optimization
        results = find_best_allocation(total_cash, accounts, tax_engine)

        # 5. Output Results
        print("\n--- OPTIMIZED PLAN ---")
        for i, recommended_bal in enumerate(results):
            diff = recommended_bal - accounts[i]["current_bal"]
            action = "KEEP"
            if diff > 0.01:
                action = f"REMOVE £{abs(diff):,.2f}"

            print(f"-> {accounts[i]['name']}:")
            print(f"    Target Balance: £{recommended_bal:,.2f}")
            print(f"    Action: {action}\n")

    except ValueError:
        print("\n[Error] Please enter numerical values (no commas or £ signs).")


if __name__ == "__main__":
    run_app()

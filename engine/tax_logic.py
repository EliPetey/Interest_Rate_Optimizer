class UKTax2026:
    def __init__(self, gross_salary):
        self.salary = gross_salary
        self.personal_allocance = 12570
        self.isa_limit = 20000.00
        self.set_brackets()

    def set_brackets(self):
        # 2026/27 UK Thresholds
        if self.salary <= 50270:
            self.psa = 1000.0  # Basic Rate
            self.rate = 0.20
        elif self.salary <= 125140:
            self.psa = 500.0  # Higher Rate
            self.rate = 0.40
        else:
            self.psa = 0.0  # Additional Rate
            self.rate = 0.45

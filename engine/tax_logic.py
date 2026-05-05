class UKTax2026:
    def __init__(self, gross_salary):
        self.salary = gross_salary
        self.personal_allocance = 12570
        self.isa_limit = 20000.00

        # NI Thresholds (Standard Class 1 - Employee)
        self.ni_primary_threshold = 12570  # Point you start paying NI
        self.ni_upper_limit = 50270  # Point NI rate usually drops

        self.set_brackets()

    def set_brackets(self):
        # Income Tax Brackets
        if self.salary <= 50270:
            self.psa = 1000.0  # Basic Rate
            self.income_tax_rate = 0.20
        elif self.salary <= 125140:
            self.psa = 500.0  # Higher Rate
            self.income_tax_rate = 0.40
        else:
            self.psa = 0.0  # Additional Rate
            self.income_tax_rate = 0.45

    def calculate_annual_ni(self):
        """Calculates Employee Class 1 National Insurance"""
        if self.salary <= self.ni_primary_threshold:
            return 0.0

        # Standard NI rates (Using 8% for main and 2% for upper as per current rates)
        if self.salary <= self.ni_upper_limit:
            ni_bill = (self.salary - self.ni_primary_threshold) * 0.08
        else:
            # 8% on the chunk between threshold and upper limit
            main_chunk = (self.ni_upper_limit - self.ni_primary_threshold) * 0.08
            # 2% on everything above upper limit
            upper_chunk = (self.salary - self.ni_upper_limit) * 0.02
            ni_bill = main_chunk + upper_chunk

        return ni_bill

    def calculate_income_tax(self):
        taxable_income = max(0, self.salary - self.personal_allocance)
        # Note: This is a simplified flat-rate calculation for the optimizer
        # For precise salary bands, a tiered loop is better, but this works for most/
        return taxable_income * self.income_tax_rate

    def get_take_home_salary(self):
        return self.salary - self.calculate_income_tax() - self.calculate_annual_ni()

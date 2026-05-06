class UKTax2026:
    def __init__(self, gross_salary):
        self.salary = gross_salary
        self.isa_limit = 20000.00

        # NI Thresholds (Standard Class 1 - Employee)
        self.ni_primary_threshold = 12570  # Point you start paying NI
        self.ni_upper_limit = 50270  # Point NI rate usually drops

        # Calculate dynamic personal allowance
        self.personal_allocance = 12570
        if self.salary > 100000:
            reduction = (self.salary - 100000) / 2
            self.personal_allowance = max(0, 12570 - reduction)

        self.set_psa()

    def set_psa(self):
        # PSA based on the highest tax band you touch
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
            return (self.salary - self.ni_primary_threshold) * 0.08

        main_chunk = (self.ni_upper_limit - self.ni_primary_threshold) * 0.08
        upper_chunk = (self.salary - self.ni_upper_limit) * 0.02
        return main_chunk + upper_chunk

    def calculate_income_tax(self):
        taxable_income = max(0, self.salary - self.personal_allocance)
        tax = 0.0

        # Basic Rate (20%) - up to £37,700 of taxable income
        basic_slice = min(remaining_income, 37700)
        tax += basic_slice * 0.20
        remaining_income -= basic_slice

        # Higher Rate (40%) - up to next chunk
        higher_slice = min(remaining_income, 125140 - 50270)
        tax += higher_slice * 0.40
        remaining_income -= higher_slice

        # Additional Rate (45%)
        if remaining_income > 0:
            tax += remaining_income * 0.45

        return tax

    def get_take_home_salary(self):
        return self.salary - self.calculate_income_tax() - self.calculate_annual_ni()

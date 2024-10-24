class IncomeCalculator:
    def __init__(self, is_government):
        self.is_government = is_government
        self.income_from_job = 0

    def calc_income(self):
        basic_salary = int(input("Basic salary: "))
        house_rent_allowance = int(input("House rent allowance: "))
        medical_allowance = int(input("Medical allowance: "))
        festival_bonus = int(input("Festival bonus: "))

        if self.is_government == "N":
            rent_free_accommodation = int(input("Value of rent free accommodation: "))
            accommodation_at_concessional_rate = int(input("Value of accommodation at concessional rate: ")) - int(input("Rent paid by Taxpayer: "))
            vehicle_facility_provided = self._get_vehicle_facility()
            other_non_cash = self._get_other_benefits()
            self.income_from_job = (
                basic_salary + house_rent_allowance + medical_allowance + festival_bonus +
                rent_free_accommodation + accommodation_at_concessional_rate + vehicle_facility_provided +
                other_non_cash
            )
            return self.income_from_job
        
        else:
            self.income_from_job = basic_salary + house_rent_allowance + medical_allowance + festival_bonus
            other_benefits = self._get_government_benefits()
            self.income_from_job += sum(other_benefits)

            i = [self.income_from_job, basic_salary, festival_bonus]

            return i

    def _get_vehicle_facility(self):
        vehicle_facility_provided = 0
        if input("Do you have any vehicle facility? (Y/N): ").upper() == "Y":
            no_of_months = int(input("Enter the number of months you had this facility: "))
            is_higher_cc = input("Is the vehicle higher than 2500cc? (Y/N): ").upper()
            vehicle_facility_provided = no_of_months * (25000 if is_higher_cc == "Y" else 10000)
        return vehicle_facility_provided

    def _get_other_benefits(self):
        other_non_cash = 0
        if input("Do you have other benefits? (Y/N): ").upper() == "Y":
            other_non_cash += int(input("Other non-cash benefit: "))
            other_non_cash += int(input("Arrear salary: "))
            other_non_cash += int(input("Education allowance: "))
            other_non_cash += int(input("Entertainment allowance: "))
            other_non_cash += int(input("Employee's contribution to RPF: "))
            other_non_cash += int(input("Gratuity: "))
            other_non_cash += int(input("Interest accrued on RPF: "))
            other_non_cash += int(input("Leave allowance: "))
            other_non_cash += int(input("Other bonus: "))
            other_non_cash += int(input("Overtime allowance: "))
            other_non_cash += int(input("Pension: "))
            other_non_cash += int(input("TA/DA/Conveyance not expended: "))
            other_non_cash += int(input("Others: "))
        return other_non_cash

    def _get_government_benefits(self):
        benefits = []
        if input("Do you have other government benefits? (Y/N): ").upper() == "Y":
            benefits.append(int(input("Arrear pay: ")))
            benefits.append(int(input("Appointment pay: ")))
            benefits.append(int(input("Batsman allowance: ")))
            benefits.append(int(input("Charge allowance: ")))
            benefits.append(int(input("Chawki allowance: ")))
            benefits.append(int(input("Compensatory allowance: ")))
            benefits.append(int(input("Conveyance allowance: ")))
            benefits.append(int(input("Cook allowance: ")))
            benefits.append(int(input("Daily allowance: ")))
            benefits.append(int(input("Dearness allowance: ")))
            benefits.append(int(input("Defence service allowance: ")))
            benefits.append(int(input("Deputation allowance: ")))
            benefits.append(int(input("Disturbance allowance: ")))
            benefits.append(int(input("Support staff allowance: ")))
            benefits.append(int(input("Education allowance: ")))
            benefits.append(int(input("Flying pay: ")))
            benefits.append(int(input("Foreign allowance: ")))
            benefits.append(int(input("Gratuity: ")))
            benefits.append(int(input("GPF interest: ")))
            benefits.append(int(input("Good conduct pay: ")))
            benefits.append(int(input("Hazardous job allowance: ")))
            benefits.append(int(input("Haircut allowance: ")))
            benefits.append(int(input("Hill allowance: ")))
            benefits.append(int(input("Honorarium: ")))
            benefits.append(int(input("Judicial allowance: ")))
            benefits.append(int(input("Lumpgrant/Leave encashment: ")))
            benefits.append(int(input("Medal allowance: ")))
            benefits.append(int(input("Mobile/Cellphone allowance: ")))
            benefits.append(int(input("Overtime allowance: ")))
            benefits.append(int(input("Other retirement benefits: ")))
            benefits.append(int(input("Pension: ")))
            benefits.append(int(input("Personal pay: ")))
            benefits.append(int(input("Residential telephone allowance: ")))
            benefits.append(int(input("Ration allowance: ")))
            benefits.append(int(input("Refreshment allowance: ")))
            benefits.append(int(input("Recreation allowance: ")))
            benefits.append(int(input("Retainer allowance: ")))
            benefits.append(int(input("Special pay: ")))
            benefits.append(int(input("SSG pay: ")))
            benefits.append(int(input("Security allowance: ")))
            benefits.append(int(input("TA/DA/Conveyance (not expended): ")))
            benefits.append(int(input("Tiffin allowance: ")))
            benefits.append(int(input("Transport maintenance allowance: ")))
            benefits.append(int(input("Training allowance: ")))
            benefits.append(int(input("Travel allowance: ")))
            benefits.append(int(input("Uniform allowance: ")))
            benefits.append(int(input("Washing allowance: ")))
            benefits.append(int(input("Worthiness pay: ")))
            benefits.append(int(input("Others: ")))
        return benefits


class TaxCalculator:
    def __init__(self, taxable_income):
        self.taxable_income = taxable_income
        self.exemption_limit = 0

    def set_exemption_limit(self, category, num_autistic_children):
        exemptions = {
            1: 350000,
            2: 400000,
            3: 475000,
            4: 500000
        }
        self.exemption_limit = exemptions.get(category, 0) + (num_autistic_children * 50000)

    def calculate_tax(self):
        taxable_income_after_exemption = max(0, self.taxable_income - self.exemption_limit)
        return self._calculate_tax_liability(taxable_income_after_exemption)

    def _calculate_tax_liability(self, taxable_income):
        tax_liability = 0
        slabs = [
            (100000, 0.05),
            (400000, 0.10),
            (500000, 0.15),
            (500000, 0.20),
            (2000000, 0.25),
            (float('inf'), 0.30)
        ]

        for limit, rate in slabs:
            if taxable_income <= 0:
                break
            taxable_amount = min(taxable_income, limit)
            tax_liability += taxable_amount * rate
            taxable_income -= taxable_amount

        return tax_liability


def main():
    is_government_employee = input("Are you a Government Employee? (Y/N): ").upper()

    name_of_employer = input("Enter the name of your employer: ")
    designation = input("Enter your designation: ")
    is_shareholder = input("Are you a Shareholder Director? (Y/N): ")

    income_calculator = IncomeCalculator(is_government_employee)
    income_calculator.calc_income()

    # Calculate taxable income based on exemptions
    total_income = income_calculator.income_from_job
    if is_government_employee == "N":
        taxable_income = total_income - (total_income / 3 if (total_income / 3) < 450000 else 450000)
    else:
        income = total_income[1] + total_income[2]
        taxable_income = income - (income / 3 if (income / 3) < 450000 else 450000)  # You can adjust this logic if necessary

    print("Your taxable income is:", taxable_income)

    print("Please select your category: \n 1. Normal Person (Male) \n 2. Woman or age greater than 64 years \n "
          "3. Third Gender or Autistic \n 4. Gazetted Freedom Fighters who were injured during war \n ")

    category = int(input("Enter the category number: "))
    num_autistic_children = 0

    if input("Do you have any autistic child? (Y/N): ").upper() == "Y":
        num_autistic_children = int(input("Enter the number of autistic children: "))

    tax_calculator = TaxCalculator(taxable_income)
    tax_calculator.set_exemption_limit(category, num_autistic_children)
    tax_liability = tax_calculator.calculate_tax()
    print("Your tax liability is:", tax_liability)


if __name__ == "__main__":
    main()

def calc_income(is_government: str):
    income_from_job = basic_salary = house_rent_allowance = medical_allowance = festival_bonus = rent_free_accommodation = accommodation_at_concessional_rate = vehicle_facility_provided = other_non_cash = arrear_salary = education_allowance = entertainment_allowance = contribution_to_rpf = gratuity = interest_rpf = leave_allowance = other_bonus = overtime_allowance = pension = arrear_pay = appointment_pay = batsman_allowance = charge_allowance = chawki_allowance = compensatory_allowance = conveyance_allowance = cook_allowance = daily_allowance = dearness_allowance = defence = deputation = disturbance = support_staff = education = flying_pay = foreign = gratuity = gpf = good_conduct_pay = hazardous = haircut = hill = honorarium = judicial = lumpgrant = medal = mobile = overtime = other_retirement = pension = personal = residential_telephone = ration = refreshment = recreation = retainer = special_pay = ssg = security = ta_da = tiffin = transport = training = travel = uniform = washing = worthiness = others = 0
    basic_salary = int(input("Basic salary: "))
    house_rent_allowance = int(input("House rent allowance: "))
    medical_allowance = int(input("Medical allowance: "))
    festival_bonus = int(input("Festival bonus: "))

    if is_government == "N":
        rent_free_accommodation = int(input("Value of rent free accommodation: "))
        accommodation_at_concessional_rate = int(input("Value of accommodation at concessional rate: ")) - int(input("Rent paid by Taxpayer: "))
        vehicle_facility = input("Do you have any vehicle facility? (Y/N): ").upper()
        if vehicle_facility == "Y":
            no_of_months = int(input("Enter the number of months you are having this facility: "))
            is_higher_cc = input("Is the vehicle higher than 2500cc? \n if Yes input Y, else input N: ").upper()
            if is_higher_cc == "Y":
                vehicle_facility_provided = no_of_months * 25000
            else:
                vehicle_facility_provided = no_of_months * 10000
        else: 
            pass

        other_benefit = input("Do you have other benefits? (Y/N) ")
        if other_benefit == "Y" :
            other_non_cash = int(input("Other non-case benefit: "))
            arrear_salary = int(input("Arrear salary: "))
            education_allowance = int(input("Education allowance: "))
            entertainment_allowance = int(input("Entertainment allowance: "))
            contribution_to_rpf = int(input("Employee's contribution to RPF: "))
            gratuity = int(input("Gratuity: "))
            interest_rpf = int(input("Interest accrued on RPF: "))
            leave_allowance = int(input("Leave allowance: "))
            other_bonus = int(input("Other bonus: "))
            overtime_allowance = int(input("Overtime allowance: "))
            pension = int(input("Pension: "))
            ta_da = int(input("TA/DA/Conveyance etc. not Expended: "))
            # Employee share schemes (Share received)
            # Employee share schemes (Transfer of share right)
            others = int(input("Others: "))

        else :
            pass

        income_from_job = basic_salary + house_rent_allowance + medical_allowance + festival_bonus + rent_free_accommodation + accommodation_at_concessional_rate + vehicle_facility_provided + other_non_cash + arrear_salary + education_allowance + entertainment_allowance + contribution_to_rpf + gratuity + interest_rpf + leave_allowance + other_bonus + overtime_allowance +pension + ta_da + others
        return income_from_job

    else:

        other_benefit = input("Do you have other benefits? (Y/N) ")
        if other_benefit == "Y" :
        
            arrear_pay = int(input("Arrear pay: "))
            appointment_pay = int(input("Appointment pay: "))
            batsman_allowance = int(input("Batsman allowance: "))
            charge_allowance = int(input("Charge allowance: "))
            chawki_allowance = int(input("Chawki allowance: "))
            compensatory_allowance = int(input("Compensatory allowence: "))
            conveyance_allowance = int(input("Conveyance allowance: "))
            cook_allowance = int(input("Cook allowance: "))
            daily_allowance = int(input("Daily allowance: "))
            dearness_allowance = int(input("Dearness allowance/Special benefit: "))
            defence = int(input("Defence service allowance"))
            deputation = int(input("Deputation allowance: "))
            disturbance = int(input("Disturbance allowence: "))
            support_staff = int(input("Allowance for support staff: "))
            education = int(input("Education allowance: "))
            flying_pay = int(input("Flying pay: "))
            foreign = int(input("Foreign allowance: "))
            gratuity = int(input("Gratuity: "))
            gpf = int(input("GPF interest: "))
            good_conduct_pay = int(input("Good conduct pay: "))
            hazardous = int(input("Hazardous job allowance: "))
            haircut = int(input("Haircut allowance: "))
            hill = int(input("Hill allowance: "))
            honorarium = int(input("Honorarium: "))
            judicial = int(input("Judicial allowance: "))
            lumpgrant = int(input("Lumpgrant/Leave encashment: "))
            medal = int(input("Medal allowance: "))
            mobile = int(input("Mobile/Cellphone allowance: "))
            overtime  = int(input("Overtime allowance: "))
            other_retirement = int(input("Other retirement benefits: "))
            pension = int(input("Pension: "))
            personal = int(input("Personal pay: "))
            residential_telephone = int(input("Residential telephone enchashment allowance: "))
            ration = int(input("Ration allowance: "))
            refreshment = int(input("Refreshment allowance: "))
            recreation = int(input("Rest and recreation allowance: "))
            retainer = int(input("Retainer allowance: "))
            special_pay = int(input("Special pay: "))
            ssg = int(input("SSG pay: "))
            security = int(input("Security allowance: "))
            ta_da = int(input("TA/DA/Conveyance(not expended): "))
            tiffin = int(input("Tiffin allowance: "))
            transport = int(input("Transport maintenance allowance: "))
            training = int(input("Training allowance: "))
            travel = int(input("Travel allowance: "))
            uniform = int(input("Uniform allowance: "))
            washing = int(input("Washing allowance: "))
            worthiness = int(input("Worthiness pay: "))
            others = int(input("Others: "))
        
        income_from_job = basic_salary + house_rent_allowance + medical_allowance + festival_bonus + arrear_pay + appointment_pay + batsman_allowance + charge_allowance + chawki_allowance + compensatory_allowance + conveyance_allowance + cook_allowance + daily_allowance + dearness_allowance + defence + deputation + disturbance + support_staff + education + flying_pay + foreign + gratuity + gpf + good_conduct_pay + hazardous + haircut + hill + honorarium + judicial + lumpgrant + medal + mobile + overtime + other_retirement + pension + personal + residential_telephone + ration + refreshment + recreation + retainer + special_pay +ssg + security +ta_da + tiffin + transport + training + travel + uniform + washing + worthiness + others
        a = [income_from_job, basic_salary, festival_bonus]
        return a
    


def tax_slab(taxable_income) :
    f = first = second = third = fourth = fifth = sixth = seventh= 0
    temp = taxable_income

    print("Please select your category: \n 1. Normal Person (Male) \n 2. Woman or age greater than 64 years \n "
          "3. Third Gender or Autistic \n 4. Gazetted Freedom Fighters who were injured during war \n ")

    t = int(input("Enter the category no.- "))

    match t:
        case 1:
            f = 350000
        case 2:
            f = 400000
        case 3:
            f = 475000
        case 4:
            f = 500000
        case _:
            print("You didn't enter valid category")

    t = input("Do you have any autistic child? (Y/N): ").upper()

    if t == "Y" :
        child = int(input("Enter the number of autistic children: "))
        f += child * 50000

    if temp >= f :
        first = 0
        print(first)
        temp = temp - f
        if temp >= 100000:
            second = 100000 * 0.05
            print(second)
            temp = temp - 100000
            if temp >= 400000:
                third = 400000 * 0.1
                print(third)
                temp = temp - 400000
                if temp >= 500000:
                    fourth = 500000 * 0.15
                    print(fourth)
                    temp = temp - 500000
                    if temp >= 500000:
                        fifth = 500000 * 0.2
                        print(fifth)
                        temp = temp - 500000
                        if temp >= 2000000:
                            sixth = 2000000 * 0.25
                            print(sixth)
                            temp = temp - 2000000
                            if temp >= 0:
                                seventh = temp * 0.3
                                print(seventh)
                        else:
                            sixth = temp * 0.25
                            print(fifth)
                    else :
                        fifth = temp * 0.2
                        print(fifth)
                else:
                    fourth = temp * 0.15
                    print(fourth)
            else:
                third = temp * 0.1
                print(third)
        else:
            second = temp * 0.05
            print(second)


    tax_liability = first + second + third + fourth + fifth + sixth
    return tax_liability

def calc_taxable_amount(income: int):
    x = income/3
    if x < 450000 :
        taxable_income = income - x
    else :
        taxable_income = income - 450000

    return taxable_income



def main():
    taxable_income = 0

    is_government_employee = input("Are you a Government Employee? (Y/N): ").upper()

    name_of_employeer = input("Enter the name of your employeer: ")

    designation = input("Enter your designation: ")

    is_shareholder = input("Are you a Shareholder Director? (Y/N): ")


    if is_government_employee == "N":
        income = calc_income(is_government_employee)
        taxable_income = calc_taxable_amount(income)
        
    else:
        i = calc_income(is_government_employee)
        income = i[1] + i[2]
        taxable_income = calc_taxable_amount(income)

    print("Your taxable income is:", taxable_income)

    tax_liability = tax_slab(taxable_income)
    print("Your tax liability is:", tax_liability)
    
    return


if __name__ == "__main__":
    main()
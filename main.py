from user_input import InputHandler
from retirement import Retirement


SS_LINK = "https://www.ssa.gov/OACT/quickcalc/"


def main():
    # get user params
    input_handler = InputHandler()
    try:
        age_type = "your current age"
        age = input_handler.input_int(0, 111, age_type)
        retire_age_type = "your retirement age"
        retirement_age = input_handler.input_int(0, 111, retire_age_type)
        inflation_type = "inflation (%)"
        inflation = input_handler.input_int(0 , 10, inflation_type)/100
        principle_type = "your initial principle ($)"
        principle = input_handler.input_int(0, 10000000, principle_type)
        monthly_invested_type = "your monthly investing"
        monthly = input_handler.input_int(0, 1000000, monthly_invested_type)
        apy_type = "pre-retirement APY (%)"
        yearly_apy_preretire = input_handler.input_int(0 , 35, apy_type)/100
        retire_pay_type = "your first retirement year distribution (todays $)"
        first_year_selfpay = input_handler.input_int(0, 100000, retire_pay_type)
        apy_type = "post-retirement APY (%)"
        yearly_apy_retire = input_handler.input_int(0 , 35, apy_type)/100
        print(f"To estimate social security you can use {SS_LINK}")
        ss_type = "your estimated monthly social security (in todays $)"
        social_security = input_handler.input_int(0, 10000, ss_type)*12
    except InputHandler.QuitProgram:
        return

    # simulate retirement
    years_till_retire = retirement_age - age
    preretire_amortization, retire_amortization = Retirement.the_works(years_till_retire, inflation, monthly, principle, yearly_apy_preretire, first_year_selfpay, yearly_apy_retire, social_security)

    # show preretirement amortization
    InputHandler.clear()
    try:
        input("Press enter to display preretirement amortization")
    except (KeyboardInterrupt, EOFError):
        pass
    Retirement.print_preretire_amortization(preretire_amortization, age)

    # show retirement amortization
    try:
        input("\n\nPress enter to display retirement amortization")
    except (KeyboardInterrupt, EOFError):
        pass
    InputHandler.clear()
    Retirement.print_retirement_amortization(retire_amortization, retirement_age)

if __name__ == "__main__":
    main()
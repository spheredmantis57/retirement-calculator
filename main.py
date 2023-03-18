"""Main file for retirement calculator program
"""
# Dowling: only two over
# pylint: disable=too-many-locals
from user_input import InputHandler
from retirement import Retirement


SS_LINK = "https://www.ssa.gov/OACT/quickcalc/"


def main():
    """the main function of the program
    """
    # get user params
    input_handler = InputHandler()
    try:
        input_type = "your current age"
        age = input_handler.input_int(0, 111, input_type)
        input_type = "your retirement age"
        retirement_age = input_handler.input_int(0, 111, input_type)
        input_type = "inflation (%)"
        inflation = input_handler.input_int(0, 10, input_type)/100
        input_type = "your initial principle ($)"
        principle = input_handler.input_int(0, 10000000, input_type)
        input_type = "your monthly investing"
        monthly = input_handler.input_int(0, 1000000, input_type)
        input_type = "pre-retirement APY (%)"
        yearly_apy_preretire = input_handler.input_int(0, 35, input_type)/100
        input_type = "your first retirement year distribution (todays $)"
        first_year_selfpay = input_handler.input_int(0, 100000, input_type)
        input_type = "post-retirement APY (%)"
        yearly_apy_retire = input_handler.input_int(0, 35, input_type)/100
        print(f"To estimate social security you can use {SS_LINK}")
        input_type = "your estimated monthly social security (in todays $)"
        social_security = input_handler.input_int(0, 10000, input_type)*12
    except InputHandler.QuitProgram:
        return

    # simulate retirement
    years_till_retire = retirement_age - age

    # make year pay future dollars
    first_year_selfpay_adjusted = \
        Retirement.calc_future_dollars(first_year_selfpay,
                                       inflation,
                                       years_till_retire)

    # calc invested by retire
    preretire_amortization = \
        Retirement.calc_investment(principle,
                                   yearly_apy_preretire,
                                   monthly,
                                   years_till_retire)
    invested_at_retirement = \
        (preretire_amortization[-1])[Retirement.PRE_EBALANCE_KEY]

    # calc future social_security
    if social_security != 0:
        social_security = Retirement.calc_future_dollars(social_security,
                                                         inflation,
                                                         years_till_retire)

    # simulate years in retirement
    retire_amortization = \
        Retirement.simulate_retirement(invested_at_retirement,
                                       first_year_selfpay_adjusted,
                                       yearly_apy_retire, inflation,
                                       social_security)


    # preretire_amortization, retire_amortization = \
    #     Retirement.the_works(
    #         years_till_retire,
    #         inflation, monthly,
    #         principle, yearly_apy_preretire,
    #         first_year_selfpay,
    #         yearly_apy_retire,
    #         social_security
    #         )

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
    Retirement.print_retirement_amortization(retire_amortization,
                                             retirement_age)

if __name__ == "__main__":
    main()

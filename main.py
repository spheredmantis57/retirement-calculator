"""Main file for retirement calculator program
"""
# Dowling: only two over
# pylint: disable=too-many-locals
from argparse import ArgumentParser

if __name__ == '__main__':
    # running as a standalone program
    from user_input import InputHandler
    from retirement import Retirement
else:
    # running as part of another project
    from .user_input import InputHandler
    from .retirement import Retirement

from flask import Flask, render_template, request

app = Flask(__name__)
SS_LINK = "https://www.ssa.gov/OACT/quickcalc/"

def get_amortizations(years_till_retire, first_year_selfpay, inflation, principle, yearly_apy_preretire, monthly, yearly_apy_retire, social_security):
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

    return preretire_amortization, retire_amortization


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

    preretire_amortization, retire_amortization = get_amortizations(years_till_retire, first_year_selfpay, inflation, principle, yearly_apy_preretire, monthly, yearly_apy_retire, social_security)

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

@app.route('/')
def retirement_calculator():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate_retirement():
    # input from the form
    current_age = int(request.form['current_age'])
    retirement_age = int(request.form['retirement_age'])
    inflation = float(request.form['inflation']) / 100
    principle = float(request.form['initial_principle'])
    monthly = float(request.form['monthly_investing'])
    pre_retire_apy = float(request.form['pre_retire_apy']) / 100
    first_year_selfpay = float(request.form['first_retirement_distribution'])
    post_retire_apy = float(request.form['post_retire_apy']) / 100
    social_security = float(request.form['estimated_monthly_social_security']) * 12
    # calculate
    # simulate retirement
    years_till_retire = retirement_age - current_age
    preretire_amortization, retire_amortization = get_amortizations(years_till_retire, first_year_selfpay, inflation, principle, pre_retire_apy, monthly, post_retire_apy, social_security)
    # display results
    return render_template('results.html',
                           preretire_amortization=preretire_amortization,
                           retire_amortization=retire_amortization,
                           age=current_age,
                           retirement_age=retirement_age)

if __name__ == "__main__":
    parser = ArgumentParser(description="Sample argparse script")
    parser.add_argument("--cli", action="store_true", help="Set this flag to enable the CLI mode")
    args = parser.parse_args()
    if args.cli:
        main()
    else:
        app.run()

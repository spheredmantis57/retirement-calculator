"""Main file for retirement calculator program
"""
# Dowling: only two over
# pylint: disable=too-many-locals
from argparse import ArgumentParser
from flask import Flask, render_template, request, Blueprint

try:
    from user_input import InputHandler
    from retirement import Retirement
except ImportError:
    pass

try:
    from .user_input import InputHandler
    from .retirement import Retirement
except ImportError:
    pass

# blue print to allow this website to be taken in by another flask app
RET_CALC_BLUE_PRINT = Blueprint('retire', __name__,
                                static_folder="static",
                                template_folder="templates")
APP = Flask(__name__)
SS_LINK = "https://www.ssa.gov/OACT/quickcalc/"

# pylint: disable=too-many-arguments
def get_amortizations(years_till_retire, first_year_selfpay, inflation,
                      principle, yearly_apy_preretire, monthly,
                      yearly_apy_retire, social_security):
    """
    Helper function to get the amortizations for working years and retirement
    years.

    Arguments:
    years_till_retire (int) - the number of years till you retire
    first_year_selfpay (float) - the amount in todays dollars you want each year
                                 of retirement
    principle (float) - the amount you have invested right now
    yearly_apy_preretire (float) - APY of working year investment
    monthly (float) - the amount you invest each month
    yearly_apy_retire (float) - APY of retirement year investment
    social_security (float) - the amount you'll get from SS each year

    Returns:
    preretire_amortization, retire_amortization
    Refer to print_preretire_entry and print_retire_entry
    """
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
# pylint: enable=too-many-arguments


def cli():
    """the main (CLI) function of the program
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

    preretire_amortization, retire_amortization = \
        get_amortizations(years_till_retire, first_year_selfpay, inflation,
                          principle, yearly_apy_preretire, monthly,
                          yearly_apy_retire, social_security)

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

@RET_CALC_BLUE_PRINT.route('/')
@APP.route('/')
def retirement_calculator():
    """display main retirement window for input"""
    return render_template('calculator.html')

@RET_CALC_BLUE_PRINT.route('/calculate', methods=['POST'])
@APP.route('/calculate', methods=['POST'])
def calculate_retirement():
    """take the request from retirement_calculator() to get amortizations"""
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
    preretire_amortization, retire_amortization = \
        get_amortizations(years_till_retire, first_year_selfpay, inflation,
                          principle, pre_retire_apy, monthly, post_retire_apy,
                          social_security)
    # display results
    return render_template('results.html',
                           preretire_amortization=preretire_amortization,
                           retire_amortization=retire_amortization,
                           age=current_age,
                           retirement_age=retirement_age)

def main():
    """the main func of the program"""
    parser = ArgumentParser(description="Sample argparse script")
    parser.add_argument("--cli", action="store_true", help="Set this flag to enable the CLI mode")
    args = parser.parse_args()
    if args.cli:
        cli()
    else:
        APP.run()

if __name__ == "__main__":
    main()

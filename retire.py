import os

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


class Retirement:
    RETIREMENT_PRINCIPLE_KEY = "Principle"
    RETIREMENT_YEAR_PAY_KEY = "Withdraw"
    RETIREMENT_END_BAL_KEY = "End"

    PRE_SPRINCIPLE_KEY = "pre_start_prinr"
    PRE_INTEREST_KEY = "pre_interest"
    PRE_SBALANCE_KEY = "pre_start_balance"
    PRE_EBALANCE_KEY = "pre_end_balance"
    PRE_EPRINCIPLE__KEY = "pre_end_principle"

    def calc_future_dollars(todays_dollars, inflation, years):
        for _ in range(years):
            todays_dollars *= inflation + 1
        return todays_dollars

    def calc_investment(principle, growth, montly_invest, years):
        running_balance = principle
        actual_principle = running_balance
        amortization = list()
        for _ in range(years):
            year = {Retirement.PRE_SPRINCIPLE_KEY: actual_principle, Retirement.PRE_SBALANCE_KEY: running_balance}
            interest_yr = running_balance * growth
            yr_invest = 12 * montly_invest
            running_balance += interest_yr + yr_invest
            year[Retirement.PRE_INTEREST_KEY] = interest_yr
            year[Retirement.PRE_EBALANCE_KEY] = running_balance
            year[Retirement.PRE_EPRINCIPLE__KEY] = yr_invest + actual_principle
            actual_principle = year[Retirement.PRE_EPRINCIPLE__KEY]
            amortization.append(year)
        return amortization

    def print_retire_entry(year, principle, withdraw, end):
        fmt = "{0: >20}"
        year_fmt = "{0: ^6}"
        print(f"{year_fmt.format(year)} {fmt.format(principle)} {fmt.format(withdraw)} {fmt.format(end)}")
    
    def print_preretire_entry(year, sprin, sbal, interest, ebal, eprin):
        fmt = "{0: >20}"
        year_fmt = "{0: ^6}"
        print(f"{year_fmt.format(year)} {fmt.format(sprin)} {fmt.format(sbal)} {fmt.format(interest)} {fmt.format(ebal)} {fmt.format(eprin)}")

    def simulate_retirement(principle, initial_pay, growth, inflation, social_security=0):
        amortization = list()
        for _ in range(80):
            temp_dict = {Retirement.RETIREMENT_PRINCIPLE_KEY: principle, Retirement.RETIREMENT_YEAR_PAY_KEY: initial_pay}
            principle -= (initial_pay - social_security)
            social_security *= inflation + 1
            initial_pay *= inflation + 1
            principle *= growth + 1

            temp_dict[Retirement.RETIREMENT_END_BAL_KEY] = principle
            amortization.append(temp_dict)
            if principle < 0:
                break
        
        return amortization

    def print_retirement_amortization(amortization, age=0):
        fmt = "${:.2f}"
        Retirement.print_retire_entry("Year", Retirement.RETIREMENT_PRINCIPLE_KEY, Retirement.RETIREMENT_YEAR_PAY_KEY, Retirement.RETIREMENT_END_BAL_KEY)
        for year, info in enumerate(amortization):
            Retirement.print_retire_entry(year+age, fmt.format(info[Retirement.RETIREMENT_PRINCIPLE_KEY]), fmt.format(info[Retirement.RETIREMENT_YEAR_PAY_KEY]), fmt.format(info[Retirement.RETIREMENT_END_BAL_KEY]))

    def print_preretire_amortization(amortization, age=0):
        fmt = "${:.2f}"
        Retirement.print_preretire_entry("Year", "Start Principle", "Start Balance", "Interest", "End Balance", "End Prinicple")
        for year, info in enumerate(amortization):
            Retirement.print_preretire_entry(year+age, fmt.format(info[Retirement.PRE_SPRINCIPLE_KEY]), fmt.format(info[Retirement.PRE_SBALANCE_KEY]), fmt.format(info[Retirement.PRE_INTEREST_KEY]), fmt.format(info[Retirement.PRE_EBALANCE_KEY]), fmt.format(info[Retirement.PRE_EPRINCIPLE__KEY]))

    def the_works(years_till_retire, inflation, monthly_invested, principle, yearly_apy_preretire, first_year_selfpay, yearly_apy_retire, social_security=0):
        # make year pay future dollars
        first_year_selfpay_adjusted = Retirement.calc_future_dollars(first_year_selfpay, inflation, years_till_retire)

        # calc invested by retire
        preretire_amm = Retirement.calc_investment(principle, yearly_apy_preretire, monthly_invested, years_till_retire)
        invested_at_retirement = (preretire_amm[-1])[Retirement.PRE_EBALANCE_KEY]

        # calc future social_security
        if social_security != 0:
            social_security = Retirement.calc_future_dollars(social_security, inflation, years_till_retire)

        # simulate years in retirement
        retirement_ammortization = Retirement.simulate_retirement(invested_at_retirement, first_year_selfpay_adjusted, yearly_apy_retire, inflation, social_security)

        return preretire_amm, retirement_ammortization


def main():
    # age = 30
    # retirement_age = 60
    # inflation = 0.03
    # monthly_invested = 6000/12
    # principle = 5000
    # yearly_apy_preretire = 0.08
    # first_year_selfpay = 7200 # todays dollar
    # yearly_apy_retire = 0.05
    # # https://www.ssa.gov/OACT/quickcalc/
    # social_security = 1379 * 12
    age = 25
    retirement_age = 64
    inflation = 0.03
    monthly_invested = 1000
    principle = 10000
    yearly_apy_preretire = 0.088
    first_year_selfpay = 50000 # todays dollar
    yearly_apy_retire = 0.05
    # https://www.ssa.gov/OACT/quickcalc/
    social_security = 0
    # social_security = 1726 * 12

    years_till_retire = retirement_age - age
    preretire_amortization, retire_amortization = Retirement.the_works(years_till_retire, inflation, monthly_invested, principle, yearly_apy_preretire, first_year_selfpay, yearly_apy_retire, social_security)

    clear()
    input("Press enter to display preretirement amortization")
    Retirement.print_preretire_amortization(preretire_amortization, age)

    input("\n\nPress enter to display retirement amortization")
    clear()
    Retirement.print_retirement_amortization(retire_amortization, retirement_age)

if __name__ == "__main__":
    main()
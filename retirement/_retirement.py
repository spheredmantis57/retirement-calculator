"""Module for the Retirement class
"""

class Retirement:
    """Retirement class allows for general investing/retirement functions
    """
    RETIREMENT_PRINCIPLE_KEY = "Principle"
    RETIREMENT_YEAR_PAY_KEY = "Withdraw"
    RETIREMENT_END_BAL_KEY = "End"

    PRE_SPRINCIPLE_KEY = "pre_start_prinr"
    PRE_INTEREST_KEY = "pre_interest"
    PRE_SBALANCE_KEY = "pre_start_balance"
    PRE_EBALANCE_KEY = "pre_end_balance"
    PRE_EPRINCIPLE__KEY = "pre_end_principle"

    @staticmethod
    def calc_future_dollars(todays_dollars, inflation, years):
        """calculates the future dollars due to inflation

        Args:
            float:todays_dollars - amount to calculate future dollars from
            float:inflation - inflation rate
            int:years - number of years to simulate inflation

        Returns:
            float:future_dollars - dollars calculated with inflation
        """
        future_dollars = todays_dollars
        for _ in range(years):
            future_dollars *= inflation + 1
        return future_dollars

    @staticmethod
    def calc_investment(principle, growth, montly_invest, years):
        """create an amortization of an investment

        Args:
            float:principle - the starting balance
            float:growth - the APY
            int:years - the number of years the investment will grow

        Returns:
            list:the amortization chart
        """
        running_balance = principle
        actual_principle = running_balance
        amortization = list()
        for _ in range(years):
            year = {Retirement.PRE_SPRINCIPLE_KEY: actual_principle,
                    Retirement.PRE_SBALANCE_KEY: running_balance}
            interest_yr = running_balance * growth
            yr_invest = 12 * montly_invest
            running_balance += interest_yr + yr_invest
            year[Retirement.PRE_INTEREST_KEY] = interest_yr
            year[Retirement.PRE_EBALANCE_KEY] = running_balance
            year[Retirement.PRE_EPRINCIPLE__KEY] = yr_invest + actual_principle
            actual_principle = year[Retirement.PRE_EPRINCIPLE__KEY]
            amortization.append(year)
        return amortization

    @staticmethod
    def print_retire_entry(year, principle, withdraw, end):
        """prints a year of the retirement amortization

        Args:
            int:year - the year of the amortization entry
            float:principle - the amount of money left in that year
            float:withdraw - the amount taken out that year in retirement
            float:end - the money left that year after withdrawing
        """
        fmt = "{0: >20}"
        year_fmt = "{0: ^6}"
        print(f"{year_fmt.format(year)} {fmt.format(principle)} "
              f"{fmt.format(withdraw)} {fmt.format(end)}")

    # Dowling: only one over
    # pylint: disable=too-many-arguments
    @staticmethod
    def print_preretire_entry(year, sprin, sbal, interest, ebal, eprin):
        """prints a year of an investment

        Args:
            int:year - the year of the amortization entry
            float:sprin - the starting personally invested
            float:sbal - the starting total amount
            float:interest - the APY of the investment
            float:ebal - the ending total amount
            float:eprin - the ending personally invested
        """
        fmt = "{0: >20}"
        year_fmt = "{0: ^6}"
        print(f"{year_fmt.format(year)} {fmt.format(sprin)} {fmt.format(sbal)} "
              f"{fmt.format(interest)} {fmt.format(ebal)} {fmt.format(eprin)}")
    # pylint: enable=too-many-arguments

    @staticmethod
    def simulate_retirement(principle,
                            initial_pay,
                            growth,
                            inflation,
                            social_security=0):
        """creates an amortization of retirement years till money runs out

        Args:
            float:principle - the amount owned at retirement
            float:initial_pay - (todays dollars) amount to use each year in
                retirement (will go up each year with inflation)
            float:growth - APY of the investment
            float:inflation - percent of inflation
            float:social_security - (todays dollars) amount of social security
                received

        Returns:
            list:the amortization chart (dict for each year)
        """
        amortization = list()
        for _ in range(80):
            temp_dict = {Retirement.RETIREMENT_PRINCIPLE_KEY: principle,
                         Retirement.RETIREMENT_YEAR_PAY_KEY: initial_pay}
            principle -= (initial_pay - social_security)
            social_security *= inflation + 1
            initial_pay *= inflation + 1
            principle *= growth + 1

            temp_dict[Retirement.RETIREMENT_END_BAL_KEY] = principle
            amortization.append(temp_dict)
            if principle < 0:
                break

        return amortization

    @staticmethod
    def print_retirement_amortization(amortization, age=0):
        """prints each year of retirement

        Args:
            list:amortization - elements are dict of each year
            int:age - the age of the person for the year
        """
        fmt = "${:.2f}"
        Retirement.print_retire_entry("Year",
                                      Retirement.RETIREMENT_PRINCIPLE_KEY,
                                      Retirement.RETIREMENT_YEAR_PAY_KEY,
                                      Retirement.RETIREMENT_END_BAL_KEY)
        for year, info in enumerate(amortization):
            Retirement.print_retire_entry( \
                year+age,
                fmt.format(info[Retirement.RETIREMENT_PRINCIPLE_KEY]),
                fmt.format(info[Retirement.RETIREMENT_YEAR_PAY_KEY]),
                fmt.format(info[Retirement.RETIREMENT_END_BAL_KEY]))

    @staticmethod
    def print_preretire_amortization(amortization, age=0):
        """prints each year of preretirement

        Args:
            list:amortization - elements are dict of each year
            int:age - the age of the person for the year
        """
        fmt = "${:.2f}"
        Retirement.print_preretire_entry("Year",
                                         "Start Principle",
                                         "Start Balance",
                                         "Interest",
                                         "End Balance",
                                         "End Principle")
        for year, info in enumerate(amortization):
            Retirement.print_preretire_entry( \
                year+age,
                fmt.format(info[Retirement.PRE_SPRINCIPLE_KEY]),
                fmt.format(info[Retirement.PRE_SBALANCE_KEY]),
                fmt.format(info[Retirement.PRE_INTEREST_KEY]),
                fmt.format(info[Retirement.PRE_EBALANCE_KEY]),
                fmt.format(info[Retirement.PRE_EPRINCIPLE__KEY]))

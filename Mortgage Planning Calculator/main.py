###########################################################
# CSE 231 Project 03 - Mortgage Planning Calculator
#
#   Prompts for city, max square footage and monthly payment,
#   how much money can be put down as a down payment, and the current APR
#   Accounts for multiple cases if certain information is unknown
#
#   Based on constant price rates for each city (or national average),
#   Calculates monthly payments based on input and determines if it is affordable to the user
#   Also can print monthly payment schedule (amortization table)
#
###########################################################

NUMBER_OF_PAYMENTS = 360    # 30-year fixed rate mortgage, 30 years * 12 monthly payments
SEATTLE_PROPERTY_TAX_RATE = 0.0092
SAN_FRANCISCO_PROPERTY_TAX_RATE = 0.0074
AUSTIN_PROPERTY_TAX_RATE = 0.0181
EAST_LANSING_PROPERTY_TAX_RATE = 0.0162
AVERAGE_NATIONAL_PROPERTY_TAX_RATE = 0.011
SEATTLE_PRICE_PER_SQ_FOOT = 499.0
SAN_FRANCISCO_PRICE_PER_SQ_FOOT = 1000.0
AUSTIN_PRICE_PER_SQ_FOOT = 349.0
EAST_LANSING_PRICE_PER_SQ_FOOT = 170.0
AVERAGE_NATIONAL_PRICE_PER_SQ_FOOT = 244.0
APR_2023 = 0.0668

WELCOME_TEXT = '''\nMORTGAGE PLANNING CALCULATOR\n============================ '''
MAIN_PROMPT = '''\nEnter a value for each of the following items or type 'NA' if unknown '''
LOCATIONS_TEXT = '''\nWhere is the house you are considering (Seattle, San Francisco, Austin, East Lansing)? '''
SQUARE_FOOTAGE_TEXT = '''\nWhat is the maximum square footage you are considering? '''
MAX_MONTHLY_PAYMENT_TEXT = '''\nWhat is the maximum monthly payment you can afford? '''
DOWN_PAYMENT_TEXT = '''\nHow much money can you put down as a down payment? '''
APR_TEXT = '''\nWhat is the current annual percentage rate? '''
AMORTIZATION_TEXT = '''\nWould you like to print the monthly payment schedule (Y or N)? '''
LOCATION_NOT_KNOWN_TEXT = '''\nUnknown location. Using national averages for price per square foot and tax rate.'''
NOT_ENOUGH_INFORMATION_TEXT = '''\nYou must either supply a desired square footage or a maximum monthly payment. 
                                Please try again.'''
KEEP_GOING_TEXT = '''\nWould you like to make another attempt (Y or N)? '''

#################

while True:
    print(WELCOME_TEXT)
    print(MAIN_PROMPT)

    # inputs

    location = input(LOCATIONS_TEXT)

    square_footage = input(SQUARE_FOOTAGE_TEXT)
    if square_footage.isdigit():
        square_footage = float(square_footage)
    else:
        square_footage = None

    max_monthly_payment = input(MAX_MONTHLY_PAYMENT_TEXT)
    if max_monthly_payment.isdigit():
        max_monthly_payment = float(max_monthly_payment)
    else:
        max_monthly_payment = None

    expected_down_payment = input(DOWN_PAYMENT_TEXT)
    if expected_down_payment.isdigit():
        expected_down_payment = float(expected_down_payment)
    else:
        expected_down_payment = float(0)

    current_APR = input(APR_TEXT)
    if not current_APR.isalpha():
        current_APR = float(current_APR) * 0.01
    else:
        current_APR = float(APR_2023)

    if location not in "Seattle, San Francisco, Austin, East Lansing":
        print(LOCATION_NOT_KNOWN_TEXT)

    # calculations

    # CASE ONE AND TWO
    if (((square_footage is not None) and (max_monthly_payment is None)) or
            (square_footage is not None) and (max_monthly_payment is not None)):
        if location == "Seattle":
            home_cost = square_footage * SEATTLE_PRICE_PER_SQ_FOOT
            tax_rate = SEATTLE_PROPERTY_TAX_RATE
        elif location == "San Francisco":
            home_cost = square_footage * SAN_FRANCISCO_PRICE_PER_SQ_FOOT
            tax_rate = SAN_FRANCISCO_PROPERTY_TAX_RATE
        elif location == "Austin":
            home_cost = square_footage * AUSTIN_PRICE_PER_SQ_FOOT
            tax_rate = AUSTIN_PROPERTY_TAX_RATE
        elif location == "East Lansing":
            home_cost = square_footage * EAST_LANSING_PRICE_PER_SQ_FOOT
            tax_rate = EAST_LANSING_PROPERTY_TAX_RATE
        else:
            location = "the average U.S. housing market"
            home_cost = square_footage * AVERAGE_NATIONAL_PRICE_PER_SQ_FOOT
            tax_rate = AVERAGE_NATIONAL_PROPERTY_TAX_RATE

        # calculations
        principal_value = home_cost - expected_down_payment
        interest_rate = current_APR / 12
        property_taxes = home_cost * tax_rate
        monthly_taxes = property_taxes / 12
        monthly_mortgage_payment = ((principal_value * (interest_rate * (1 + interest_rate)**NUMBER_OF_PAYMENTS)) /
                                    (((interest_rate + 1)**NUMBER_OF_PAYMENTS) - 1))
        total_monthly_payment = monthly_mortgage_payment + monthly_taxes

        # print message, prints for both case one and two
        print('\n\nIn {:s}, an average {:,.0f} sq. foot house would cost ${:,.0f}.'
              .format(location, square_footage, home_cost))
        print('A 30-year fixed rate mortgage with a down payment of ${:,.0f} at {:.1f}% APR results'
              .format(expected_down_payment, current_APR*100))
        print('\tin an expected monthly payment of ${:,.2f} (taxes) + ${:,.2f} (mortgage payment) = ${:,.2f}'
              .format(monthly_taxes, monthly_mortgage_payment, total_monthly_payment))
        # don't prompt for amortization if max month pay is none (case two)
        # will do that after case two's additional message
        if max_monthly_payment is None:
            amortization_answer = input(AMORTIZATION_TEXT)

    # CASE TWO ADDITIONAL MESSAGE
    if (square_footage is not None) and (max_monthly_payment is not None):
        if max_monthly_payment > total_monthly_payment:
            print('Based on your maximum monthly payment of ${:,.2f} you can afford this house.'
                  .format(max_monthly_payment))
            amortization_answer = input(AMORTIZATION_TEXT)
        else:
            print('Based on your maximum monthly payment of ${:,.2f} you cannot afford this house.'
                  .format(max_monthly_payment))
            amortization_answer = input(AMORTIZATION_TEXT)

    # CASE THREE
    if (square_footage is None) and (max_monthly_payment is not None):
        square_footage_estimate = 100
        while square_footage is None:
            # use square footage estimate for home cost calculations
            if location == "Seattle":
                home_cost = square_footage_estimate * SEATTLE_PRICE_PER_SQ_FOOT
                tax_rate = SEATTLE_PROPERTY_TAX_RATE
            elif location == "San Francisco":
                home_cost = square_footage_estimate * SAN_FRANCISCO_PRICE_PER_SQ_FOOT
                tax_rate = SAN_FRANCISCO_PROPERTY_TAX_RATE
            elif location == "Austin":
                home_cost = square_footage_estimate * AUSTIN_PRICE_PER_SQ_FOOT
                tax_rate = AUSTIN_PROPERTY_TAX_RATE
            elif location == "East Lansing":
                home_cost = square_footage_estimate * EAST_LANSING_PRICE_PER_SQ_FOOT
                tax_rate = EAST_LANSING_PROPERTY_TAX_RATE
            else:
                location = "the average U.S. housing market"
                home_cost = square_footage_estimate * AVERAGE_NATIONAL_PRICE_PER_SQ_FOOT
                tax_rate = AVERAGE_NATIONAL_PROPERTY_TAX_RATE

            # calculations based on home cost using estimated square footage
            principal_value = home_cost - expected_down_payment
            interest_rate = current_APR / 12
            property_taxes = home_cost * tax_rate
            monthly_taxes = property_taxes / 12
            monthly_mortgage_payment = (
                        (principal_value * (interest_rate * (1 + interest_rate) ** NUMBER_OF_PAYMENTS)) /
                        (((interest_rate + 1) ** NUMBER_OF_PAYMENTS) - 1))
            total_monthly_payment = monthly_mortgage_payment + monthly_taxes

            if total_monthly_payment < max_monthly_payment:
                square_footage_estimate += 1
            else:
                # I am not sure why, but my square footage was always one more than it should've been
                # I was unsure how to fix it, so I just subtracted it by one and redid calculations for the
                # final answer + display message.
                square_footage = square_footage_estimate - 1

                # calculations
                if location == "Seattle":
                    home_cost = square_footage * SEATTLE_PRICE_PER_SQ_FOOT
                    tax_rate = SEATTLE_PROPERTY_TAX_RATE
                elif location == "San Francisco":
                    home_cost = square_footage * SAN_FRANCISCO_PRICE_PER_SQ_FOOT
                    tax_rate = SAN_FRANCISCO_PROPERTY_TAX_RATE
                elif location == "Austin":
                    home_cost = square_footage * AUSTIN_PRICE_PER_SQ_FOOT
                    tax_rate = AUSTIN_PROPERTY_TAX_RATE
                elif location == "East Lansing":
                    home_cost = square_footage * EAST_LANSING_PRICE_PER_SQ_FOOT
                    tax_rate = EAST_LANSING_PROPERTY_TAX_RATE
                else:
                    location = "the average U.S. housing market"
                    home_cost = square_footage * AVERAGE_NATIONAL_PRICE_PER_SQ_FOOT
                    tax_rate = AVERAGE_NATIONAL_PROPERTY_TAX_RATE

                principal_value = home_cost - expected_down_payment
                interest_rate = current_APR / 12
                property_taxes = home_cost * tax_rate
                monthly_taxes = property_taxes / 12
                monthly_mortgage_payment = (
                        (principal_value * (interest_rate * (1 + interest_rate) ** NUMBER_OF_PAYMENTS)) /
                        (((interest_rate + 1) ** NUMBER_OF_PAYMENTS) - 1))
                total_monthly_payment = monthly_mortgage_payment + monthly_taxes

                print('\n\nIn {}, a maximum monthly payment of ${:,.2f} allows the purchase of a house of '
                      '{:,.0f} sq. feet for ${:,.0f}'.format(location, max_monthly_payment, square_footage, home_cost))
                print('\t assuming a 30-year fixed rate mortgage with a ${:,.0f} down payment at {:.1f}% APR.'
                      .format(expected_down_payment, current_APR*100))
                keep_going_answer = input(KEEP_GOING_TEXT)

    # CASE FOUR
    if (square_footage is None) and (max_monthly_payment is None):
        print(NOT_ENOUGH_INFORMATION_TEXT)
        keep_going_answer = input(KEEP_GOING_TEXT)

    # AMORTIZATION TABLE
    if amortization_answer == 'Y' or amortization_answer == 'y':

        print("\n{:^7s}|{:^12s}|{:^13s}|{:^14s}".format("Month", "Interest", "Payment", "Balance"))

        for i in range(1, 49):
            print("=", end="")

        # calculations
        payment_number = 1
        remaining_loan_amount = principal_value
        while payment_number <= NUMBER_OF_PAYMENTS:
            payment_to_interest = remaining_loan_amount * (current_APR / 12)
            payment_to_loan = monthly_mortgage_payment - payment_to_interest
            print("\n{:^7d}| ${:>9,.2f} | ${:>10,.2f} | ${:>11,.2f}".format(payment_number, payment_to_interest,
                                                                            payment_to_loan, remaining_loan_amount),
                  end="")
            # reassign remaining loan amount AFTER printing message, so first line is initial loan amount
            remaining_loan_amount = remaining_loan_amount - payment_to_loan
            payment_number += 1

        # accounts for a line break after the amortization table, before prompting for keep_going_answer
        print("")

    keep_going_answer = input(KEEP_GOING_TEXT)

    if keep_going_answer == 'Y' or keep_going_answer == 'y':
        continue
    else:
        break

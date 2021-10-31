from math import ceil, floor, log
import argparse
parser = argparse.ArgumentParser(description="This program calculates monthly payments, annuity monthly payment amount, "
                                             "loan principal and monthly differentiated payment")


# add parameters
parser.add_argument("--type", choices=["annuity", "diff"],
                    help="this is the type of payment options. \
                    Supply either 'annuity' for Annuity or \
                    'diff' for Differentiate.")
parser.add_argument("--payment", type=int, help="(Annuity only) this is the monthly payment amount.")
parser.add_argument("--principal", type=int, help="This is the principal loan total.")
parser.add_argument("--periods", type=int, help="This is the total number of payments.")
parser.add_argument("--interest", type=float, help="This is the agreed interest rate.")

# parse arguments
cli = parser.parse_args()

# add arguments into a collection
user_arg = cli.type
args = {
    "payment": cli.payment,
    "principal": cli.principal,
    "periods": cli.periods,
    "interest": cli.interest,
}

# define functions


def annuity_payment(principal=None, periods=None, interest=None):
    # When the user enters 'a'; computes the monthly payment
    if principal is None and interest is None and periods is None:
        principal = int(input('Enter the loan principal: '))
        periods = int(input("Enter the number of months: "))
        interest = float(input('Enter the loan interest: '))
    i = nominal_interest_rate(interest)
    result_annuity_payment = principal * ((i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1))
    print(f"Your monthly payment = {int(ceil(result_annuity_payment))}!")


def loan_principal(monthly=None, periods=None, interest=None):
    # When the user enters 'p'; computes the total (principal) loan.
    i = nominal_interest_rate(interest)
    if monthly is None and periods is None and interest is None:
        monthly = float(input('Enter the annuity payment: '))
        periods = int(input("Enter the number of months: "))
        interest = float(input('Enter the loan interest: '))
        principal = monthly / ((interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1))
        print(f"Your loan principal = {int(principal)}!")

    principal = monthly / ((i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1))
    print(f"Your loan principal = {int(ceil(principal))}")
    print(f"Overpayment = {monthly * periods - principal}")


def nominal_interest_rate(interest):
    return (interest / 100) / 12


def no_payments(principal=None, monthly=None, interest=None):
    # When the user enters 'n'; computes the numbers of months required.
    i = nominal_interest_rate(interest)
    if principal is None and monthly is None and interest is None:
        principal = int(input('Enter the loan principal: '))
        monthly = float(input('Enter the monthly payment: '))
        interest = float(input('Enter the loan interest: '))
    x = monthly / (monthly - i * principal)
    y = i + 1
    no_p = log(x, y)
    print(no_months(no_p))
    print(f"Overpayment = {monthly * ceil(no_p) - principal}")


def diff_payment(p, nn, m, ii):
    parenthesis = p - ((p * (m - 1)) // nn)
    d = p // nn + ii * parenthesis
    return d


def no_months(months):
    nn = ceil(months)
    years = floor(nn / 12)
    months = abs(int(nn - years * 12))
    if years == 1:
        if months == 1:
            return f"{years} year and {months} month"
        elif months == 0:
            return f"{years} year"
        else:
            return f"{years} year and {months} months"
    elif years > 1:
        if months == 1:
            return f"{years} years and {months} month"
        elif months == 0:
            return f"{years} years"
        else:
            return f"{years} years and {months} months"
    else:
        return f"{years} years and {months} months"


def general_calc(principal=None, monthly=None, periods=None, interest=None):
    # Entry point function; asks user to select a option
    if principal is None and monthly is None and periods is None and interest is None:
        get_input = input('What do you want to calculate?\n'
                          'type "n" - for number of monthly payments,\n'
                          'type "a" for annuity monthly payment amount,\n'
                          'type "p" - for loan principal: ')
        if get_input == "n":
            no_payments()
            return
        elif user_arg == 'a':
            annuity_payment()
            return
        elif get_input == "p":
            loan_principal()
            return
    else:
        if principal and monthly and interest:
            no_payments(principal, monthly, interest)
            return
        if principal and periods and interest:
            annuity_payment(principal, periods, interest)
            return
        if monthly and periods and interest:
            loan_principal(monthly, periods, interest)
            return


# verify conditions
check_args = True
no_args = len(args)
for a in args:
    if args[a] and args[a] < 0:
        check_args = False
    no_args -= 1 if args[a] is None else 0
if check_args:
    if user_arg == 'annuity':
        if no_args < 3:  # checking if user no of args for annuity is valid, required no of args is 3
            print('Incorrect parameters')
        general_calc(args['principal'], args['payment'], args['periods'], args['interest'])
    elif user_arg == 'diff':
        i = nominal_interest_rate(args['interest'])
        # diff_payment(p, nn, m, ii):
        m = 1
        sum_monthly_payment = 0
        while m <= args['periods']:
            print(f"Month {m}: payment is {ceil(diff_payment(args['principal'], args['periods'], m, i))}")
            sum_monthly_payment += ceil(diff_payment(args['principal'], args['periods'], m, i))
            m += 1
        print(f"Overpayment = {sum_monthly_payment - args['principal']}")
else:
    print('Incorrect parameters')

#!/usr/bin/env python3

"""Bill Split Calculator

This script prompts the user for a total bill amount, number of people,
and a tip percentage. It validates input, calculates the tip, total bill,
and each person's share, then displays a formatted receipt.
"""


def get_positive_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            amount = float(value)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print('Please enter a positive number.')


def get_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            count = int(value)
            if count <= 0:
                raise ValueError
            return count
        except ValueError:
            print('Please enter a whole number greater than zero.')


def choose_tip_percentage():
    options = {
        '1': 10,
        '2': 15,
        '3': 20,
        '4': 'custom'
    }

    while True:
        print('\nChoose a tip percentage:')
        print('1. 10%')
        print('2. 15%')
        print('3. 20%')
        print('4. Custom percentage')
        choice = input('Enter an option (1-4): ').strip()

        if choice in options:
            if options[choice] == 'custom':
                custom_tip = get_positive_float('Enter custom tip percentage: ')
                return custom_tip
            return float(options[choice])

        print('Invalid choice. Please select 1, 2, 3, or 4.')


def format_currency(amount):
    return f'${amount:,.2f}'


def print_receipt(subtotal, tip_percent, tip_amount, total, per_person, people):
    print('\n=== Bill Split Receipt ===')
    print(f'Subtotal:        {format_currency(subtotal)}')
    print(f'Tip ({tip_percent:.1f}%):      {format_currency(tip_amount)}')
    print(f'Total bill:      {format_currency(total)}')
    print(f'Number of people: {people}')
    print(f'Each person owes: {format_currency(per_person)}')
    print('========================')


def main():
    print('Bill Split Calculator')
    print('---------------------')

    total_bill = get_positive_float('Enter the total bill amount: ')
    people = get_positive_int('Enter the number of people: ')
    tip_percent = choose_tip_percentage()

    tip_amount = total_bill * tip_percent / 100
    total_bill_with_tip = total_bill + tip_amount
    per_person = total_bill_with_tip / people

    print_receipt(
        subtotal=total_bill,
        tip_percent=tip_percent,
        tip_amount=tip_amount,
        total=total_bill_with_tip,
        per_person=per_person,
        people=people,
    )


if __name__ == '__main__':
    main()

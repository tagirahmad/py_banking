# Write your code here
import math
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def create_db_if_exists():
    cur.execute(
        'CREATE TABLE IF NOT EXISTS card (id INTEGER , number TEXT, pin TEXT, balance INTEGER DEFAULT  0);'
    )
    conn.commit()


def insert_into_db_new_card(card_number, pin):
    cur.execute(
        f'INSERT INTO card (number, pin) VALUES ({card_number}, {pin});'
    )
    conn.commit()


def add_income(income, card_number):
    balance = int(get_balance(card_number))
    print()
    print(f'{balance} its a balance')
    new_balance = balance + int(income)
    cur.execute(
        f'UPDATE card SET balance = "{new_balance}" WHERE number = "{card_number}";'
    )
    conn.commit()


def get_balance(card_number):
    cur.execute(
        f'SELECT balance FROM card WHERE number = "{card_number}";'
    )
    balance = cur.fetchone()
    return balance[0]


def make_transfer(money_count, transfer_card, sender_card):
    balance_sender_card = int(get_balance(sender_card))
    balance_transfer_card = int(get_balance(transfer_card))
    if balance_sender_card - money_count >= 0:
        new_balance = balance_sender_card - money_count
        cur.execute(
            f'UPDATE card SET balance = "{new_balance}" WHERE number = "{sender_card}";'
        )
        cur.execute(
            f'UPDATE card SET balance = "{balance_transfer_card + money_count}" WHERE number = "{transfer_card}"'
        )
        print(f'{int(get_balance(sender_card))} its a balance sender card')
        print(f'{int(get_balance(transfer_card))} its a balance transfer card')
        conn.commit()
        return True
    else:
        return False


def close_account(card_number):
    cur.execute(
        f'DELETE FROM card WHERE number = "{card_number}";'
    )
    conn.commit()


def check_for_card_existence(card_number):
    cur.execute(
        f'SELECT number FROM card WHERE number = "{card_number}";'
    )
    row = cur.fetchone()
    return row


def login(card_number, pin):
    cur.execute(
        f'SELECT number FROM card WHERE number = "{card_number}" AND pin = "{pin}";'
    )
    row = cur.fetchone()
    return row


create_db_if_exists()


def welcome_message():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    global user_choose
    user_choose = int(input())


def logout_message():
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')
    global user_choose
    user_choose = int(input())


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def luthn_algorithm(card_number):
    card_number_as_list = [int(x) for x in card_number]
    last_num = card_number_as_list[-1]
    card_number_as_list.pop()

    for index, num in enumerate(card_number_as_list):
        if index % 2 == 0:
            card_number_as_list[index] = num * 2

    for index, num in enumerate(card_number_as_list):
        if num > 9:
            card_number_as_list[index] = num - 9

    card_number_as_list.append(last_num)
    sum_of_card_numbers = sum(card_number_as_list)
    # # return True if sum_of_card_numbers % 10 == 0 else False
    # print(f'sum of card numbers: {sum_of_card_numbers}')
    if sum_of_card_numbers % 10 == 0:
        return True
    else:
        return False


def generate_card_number(numbers_count):
    num_of_15_digits = str(4) + '00000' + str(random_with_N_digits(numbers_count - 7))
    num_of_15_digits_as_list = [int(x) for x in num_of_15_digits]
    num_of_15_digits_as_list.append(0)

    for index, num in enumerate(num_of_15_digits_as_list):
        if index % 2 == 0:
            num_of_15_digits_as_list[index] = num * 2
    num_of_15_digits_as_list.pop()

    for index, num in enumerate(num_of_15_digits_as_list):
        if num > 9:
            num_of_15_digits_as_list[index] = num - 9

    sum_of_list = sum(num_of_15_digits_as_list)
    last_digit = math.ceil(sum_of_list / 10) * 10 - sum_of_list
    result_card_number = num_of_15_digits + str(last_digit)
    return int(result_card_number)


def generate_pin():
    return random_with_N_digits(4)


class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
        self.logged = False
        self.balance = 0


program_is_working = True
while program_is_working:
    welcome_message()
    if user_choose == 1:
        # global user_card
        user_card = Card(generate_card_number(16), generate_pin())
        insert_into_db_new_card(user_card.card_number, user_card.pin)
        print('Your card has been created')
        print('Your card number:')
        print(user_card.card_number)
        print('Your card PIN:')
        print(user_card.pin)
    elif user_choose == 2:
        print('Enter your card number:')
        card_input = int(input())
        print('Enter your PIN:')
        pin_input = int(input())
        login_result = login(card_input, pin_input)
        if login_result is not None:
            user_card = Card(card_input, pin_input)
            user_card.logged = True
            print('You have successfully logged in!')
            while user_card.logged:
                logout_message()
                if user_choose == 1:
                    print(f'Balance: {get_balance(user_card.card_number)}')
                if user_choose == 2:
                    print('Enter income:')
                    income = int(input())
                    add_income(income, user_card.card_number)
                    print('Income was added!')
                if user_choose == 3:
                    print('Transfer')
                    print('Enter card number:')
                    transfer_card_number = input()
                    algorithm_result = luthn_algorithm(transfer_card_number)
                    if algorithm_result:
                        result = check_for_card_existence(transfer_card_number)
                        if result is None:
                            print('Such a card does not exist.')
                        else:
                            if user_card.card_number == transfer_card_number:
                                print("You can't transfer money to the same account!")
                            else:
                                print('Enter how much money you want to transfer')
                                desired_transfer_money_count = int(input())
                                is_success = make_transfer(desired_transfer_money_count, transfer_card_number,
                                                           user_card.card_number)
                                if is_success:
                                    print('Success!')
                                else:
                                    print('Not enough money!')
                    else:
                        print('Probably you made a mistake in the card number. Please try again!')
                if user_choose == 4:
                    close_account(user_card.card_number)
                    print('The account has been closed!')
                    user_card.logged = False
                if user_choose == 5:
                    print('You have successfully logged out!')
                    user_card.logged = False
                if user_choose == 0:
                    print('Bye!')
                    user_card.logged = False
                    program_is_working = False
        else:
            print('Wrong card number or PIN!')
    elif user_choose == 0:
        print('Bye!')
        program_is_working = False

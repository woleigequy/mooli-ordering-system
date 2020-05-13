from models.DAO import DAO
from utils.validation import is_money
from models.shared import find_customer

import string
from random import randint

# Prepare the char set for the coupon code
# Modify the char set according to your needs
# The char set contains all upper case letters and 0 to 9
char_set = list(string.ascii_uppercase)
[char_set.append(n) for n in range(0, 10)]

def generate_random_coupon_code():
    # Generate a coupon code of length 16
    return ''.join([str(char_set[randint(0, len(char_set)-1)]) for n in range(0, 16)])

def add_redeem_cards(value, batch = 1):
    # Clean the input data
    value = str(value).strip()
    batch = str(batch).strip()

    # Check is the input valid
    if not is_money(value) or not batch.isdecimal():
        raise Exception('Invalid input type.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """INSERT INTO redeem_card (
        redeem_code,
        value
    ) VALUES (
        %(redeem_code)s,
        %(value)s
    )"""
    for i in range(int(batch)):
        cursor.execute(sql, {'redeem_code': generate_random_coupon_code(), 'value': value})
        # Commit every 10 writes
        if (i + 1) % 10 == 0:
            dao.commit()
    dao.commit()

def delete_redeem_card(redeem_code):
    # Clean the input data
    redeem_code = str(redeem_code).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Check if the redeem card exists
    if find_redeem_card(redeem_code) is None:
        raise Exception('The redeem card does not exists.')

    sql = """DELETE FROM redeem_card WHERE redeem_code = %(redeem_code)s"""
    cursor.execute(sql, {'redeem_code': redeem_code})
    dao.commit()

def find_redeem_card(redeem_code):

    # Clean the input data
    param = str(redeem_code).strip()

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM redeem_card WHERE redeem_code = %(redeem_code)s"""
    cursor.execute(sql, {'redeem_code': redeem_code})
    result = cursor.fetchone()
    return result

def get_redeem_cards(limit = 0, offset = 0):
    # Clean the input data
    limit = str(limit).strip()
    offset = str(offset).strip()

    if not limit.isdecimal() or not offset.isdecimal():
        raise Exception('Invalid input.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    # Query database
    sql = """SELECT * FROM redeem_card ORDER BY redeem_code ASC"""
    if not int(limit) == 0:
        sql += ' LIMIT ' + limit + ' OFFSET ' + offset
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def redeem(customer_id, redeem_code):
    # Clean the input data
    customer_id = str(customer_id).strip()
    redeem_code = str(redeem_code).strip()

    # Find redeem card
    redeem_card = find_redeem_card(redeem_code)
    if redeem_card is None:
        raise Exception('Invalid redeen code.')

    # Find user
    customer = find_customer(method = 'id', param = customer_id)
    if customer is None:
        raise Exception('Customer not found.')

    # Establish db connection
    dao = DAO()
    cursor = dao.cursor()

    sql = """UPDATE customer SET balance = %(new_balance)s WHERE customer_id = %(customer_id)s"""
    new_balance = customer['balance'] + redeem_card['value']
    cursor.execute(sql, {'new_balance': new_balance, 'customer_id': customer_id})
    sql = """DELETE FROM redeem_card WHERE redeem_code = %(redeem_code)s"""
    cursor.execute(sql, {'redeem_code': redeem_code})
    dao.commit()

import datetime
import hashlib
import json


genesis_block = {
    'previous_hash': 'XYZ',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
transactions = []
owner='Mihai'


def get_datetime():
    date_time = datetime.datetime.now()
    date = str(date_time.year) + '.' + str(date_time.month) + '.' + str(date_time.day)
    time = str(date_time.hour) + ':' + str(date_time.minute) + ':' + str(date_time.second)
    return date + '/' + time


def user_input_transaction():
    user_input_receiver = input('Choose receiver: ')
    user_input_amount = float(input('Select amount: '))
    add_transaction(receiver=user_input_receiver, amount=user_input_amount)


def add_transaction(receiver, sender=owner, amount=1.0):
    transactions.append({
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'timestamp': get_datetime()
    })


def clear_transactions():
    transactions = []


def mine_block():
    block = {
        'previous_hash': create_hash(blockchain[-1]),
        'index': blockchain[-1]['index'] + 1,
        'transactions': transactions
    }
    blockchain.append(block)


def create_hash(previous_block):
    starting_string = ''
    delimiter = '-'
    for index, key in enumerate(previous_block):
        if index == 0:
            starting_string = starting_string + str(previous_block[key])
        else:
            starting_string = starting_string + delimiter + str(previous_block[key])
    ''' Return hashable special identification hash '''
    return hashlib.sha256(json.dumps(starting_string).encode()).hexdigest()


def validate_blockchain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != create_hash(blockchain[index - 1]):
                return False
    return True


def print_blockchain():
    for index, block in enumerate(blockchain):
        print(str(index) + '. ' + str(block))


waiting_input = True
while waiting_input:
    print('Select:')
    print('1. Add transaction')
    print('2. Mine block')
    print('3. Print pending transactions')
    print('4. Mine new block')
    print('5. Print blockchain')
    print('q. Quit')
    print('---------------------')
    user_input = input('Please input your choice: ')

    if user_input == '1':
        user_input_transaction()
    elif user_input == '2':
        pass
    elif user_input == '3':
        print(transactions)
    elif user_input == '4':
        mine_block()
        clear_transactions()
    elif user_input == '5':
        print('Validating blockchain...')
        print('Blockchain is valid: ' + str(validate_blockchain()))
        print_blockchain()
    elif user_input == 'q':
        waiting_input = False
    else:
        print('Please select a valid input')

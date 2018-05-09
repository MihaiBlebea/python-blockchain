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
mining_reward = 10
owner = 'Mihai'
budget = 100
contacts = {owner}


def get_datetime():
    date_time = datetime.datetime.now()
    date = str(date_time.year) + '.' + str(date_time.month) + '.' + str(date_time.day)
    time = str(date_time.hour) + ':' + str(date_time.minute) + ':' + str(date_time.second)
    return date + '/' + time


def user_input_transaction():
    user_input_receiver = input('Choose receiver: ')
    if user_input_receiver == 'q':
        return print('process was aborted')
    user_input_amount = input('Select amount: ')
    if user_input_amount == 'q':
        return print('process was aborted')
    else:
        user_input_amount = float(user_input_amount)
    user_confirmation = input('Are you sure you want to send {} the amount of {} ? [yes/no]: '.format(user_input_receiver, user_input_amount))
    if user_confirmation == 'yes' or user_confirmation == 'y':
        return add_transaction(receiver=user_input_receiver, amount=user_input_amount)
    elif user_confirmation == 'no' or user_confirmation == 'n':
        return print('process was aborted')
    else:
        pass


def add_transaction(receiver, sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'timestamp': get_datetime()
    }
    if verify_balance(transaction):
        transactions.append(transaction)
        return True
    else:
        return False


def verify_balance(transaction):
    if transaction['sender'] == owner:
        interim_balance = budget - transaction['amount'] 
        if interim_balance > 0:
            return True
        else:
            return False

def mine_block():
    reward_transaction = {
        'sender': 'MININIG_REWARD',
        'receiver': owner,
        'amount': mining_reward,
        'timestamp': get_datetime()
    }
    ''' Append the reward transaction to a copy of transactions array, 
        if something goes bad we can always have the transactions in a safe place '''
    copied_transactions = transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': create_hash(blockchain[-1]),
        'index': blockchain[-1]['index'] + 1,
        'transactions': copied_transactions
    }

    blockchain.append(block)
    return True


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
    print(' ________________________________')
    print('|Select:                         |')
    print('|[1]. Add transaction            |')
    print('|[2]. Print pending transactions |')
    print('|[3]. Mine new block             |')
    print('|[4]. Print blockchain           |')
    print('|[q]. Quit                       |')
    print(' --------------------------------')
    user_input = input('Please input your choice: ')

    if user_input == '1':
        if user_input_transaction():
            print('RESULT: Transaction was performed')
        else:
            print('RESULT: Sorry, transaction could not be performed at this time')
    elif user_input == '2':
        print(transactions)
    elif user_input == '3':
        if mine_block():
            transactions = []
    elif user_input == '4':
        print('Validating blockchain...')
        print('Blockchain is valid: ' + str(validate_blockchain()))
        print_blockchain()
    elif user_input == 'q':
        waiting_input = False
    else:
        print('Please select a valid input')

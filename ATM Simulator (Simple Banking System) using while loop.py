# ATM Simulator (Simple Banking System) using while loop

# Allow users to check balance, deposit, withdraw, and exit
# Keeps running until the user chooses to exit
# Input validation to prevent errors

balance = 854
pin = '072199'

print('Please enter your PIN')
i = input('> ')

while i != pin:
    print('Wrong PIN Number')
    i = input('''Please input your PIN again.\n> ''')
print('''Please wait...
\n .
\n .
\n .

''')

while True:
#if i == pin:
    print('''ATM MENU
      \n 1: Check Balance
      \n 2: Deposit Money
      \n 3: Withdraw Money
      \n 4: Exit ''')

    choice = input('Choose an Option (1-4):\n> ')

# if 1 = check balance
    if choice == '1':
        yes = input(f'''Current Balance: ${balance}
        \nContinue using the machine? (yes or no)
        \n> ''').lower # Shows balance

        if yes:
            print('''ATM MENU
            \n 1: Check Balances
            \n 2: Deposit Money
            \n 3: Withdraw Money
            \n 4: Exit ''')
        else:
              print('Thank you for using!\nPlease take your card out.')

# if 2 deposit money it should add current balance with the amount to be deposited
    elif choice == '2':
        amount = int(input('Enter deposit amount:\n$'))
        if amount > 0:
            balance += amount
            print(f'You have deposited ${amount}.\nCurrent Balance: ${balance}')
        else:
            print('Invalid amount!')
# if 3 withdraw money, so - current balance
    elif choice == '3':
        withdrawAmount = int(input('''Input amout to be withdraw\n> '''))
        if withdrawAmount > balance:
            print('Insuffient Fund. Please input the right amount')
        elif withdrawAmount - balance:
            print(f'You withdrawed ${withdrawAmount}\nCurrent Balance: ${balance}')
            
# if 4. else: close
    elif choice == '4':
        print('Thank you for using!\nPlease take your card out.')
        break

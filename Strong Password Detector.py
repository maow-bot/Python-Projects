
# Strong Password Detector
# Ensure password are at least 8 characters long
# Have both uppercase and lowercase letters
# Contain at least one number


#problem -> # if user input at least 1 upper case and at least 1 number = true (strong)
    # if user input 1 uppercase and no number = false
    # -> if user input no uppercase and at least 1 number = false

import re

password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$')

# user input
user_password =input('Please enter password: ')

#check password streght
if password_regex.match(user_password):
    print('That is a strong ass password')
else:
    print('That is a weak ass password')


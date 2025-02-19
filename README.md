# BankApplication

This is a project im actually creating, it's been about 2 weeks and i've made the biggest part of it (I think).
I got this idea from a friend and i thought that it could really be a good project to develop my skills in python.

# How does it work?

So just download the file and run the Client.py file with Python 3.11.9 to get the program running.
You will have to create an account so just follow the steps and you'll be fine.

When arriving to your dashboard you will have 5 buttons on the right, the top one (Account) everything related to the account management part and the loans,below there is the transfert part you enter the IBAN number related to the account you want to send money to and the amount you want to send. The iban number can be found in the info window, the button just below the transfert one. The settings button lets you change your username, password and delete your account. Then, the logout button just log you out from your account.

# More

When creating your account, you start at 0€ so feel free to change this data in the Main.json file from your account (for exemple for my account i will go to Data then Users then Arthur then Accounts and then Main.json, in there ill change the "Balance" value to 1000 for exemple, and ill have my money)

# Finish

Please, Im still learning python so tell me if you have something to tell me like for exemple I know that using json to store data isn't the best and im working on it, plus, i want to know what to add next or where can i improve my program.

Anyways, thanks for testing the project, let me know how do you find it!

# BankID

If you've looked through the file you may have found the BankID directory, for now it is useless but it is a long process that will create a unique id code (just like sha-256 for password) when creating your account, it will make the user able to reset his password if he forgets it. Look at the "createID" file in this directory to find a bit more info. Its the little cryptography part that i like to add in all my programs.

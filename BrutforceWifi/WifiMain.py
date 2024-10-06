import os

print('1 - Regular hack')
print('2 - Bruteforce wifi')
print('PS You can enter " --help" for more information (For example 1 --help)')
def choise():
    Type_of_Hack = input("> ")

if choise.Type_of_Hack == "1":
    exec(open('WifiHack.py', 'r', encoding='utf-8').read())

elif choise.Type_of_Hack == "2":
    exec(open('WiifiHack1.py', 'r', encoding='utf-8').read())

if choise.Type_of_Hack == "1 --help":
    print("First, a DDoS attack is carried out on the network until it is turned off, and then the same network (access point) is created to obtain the password.")

if choise.Type_of_Hack == "2 --help":
    print 
import random
import os
from Crypto.Cipher import AES
import base64

passwordRandomizer = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*'
directory = "emailAccounts"

entered = False
while not entered:
    secretKey = raw_input("Enter a 16 character long encryption key. \n\
Make sure you remember this key\n\
as you will need it to access any data: \n")

    if len(secretKey) != 16:
        print "\nNot 16 characters\n"
    else:
        entered = False
        break

print '\n'

def encryption(data, excludeNewLine=False):
    BLOCK_SIZE = 16
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    cipher = AES.new(secretKey)

    encoded = EncodeAES(cipher, data)
    
    if excludeNewLine == False:
        return '\n {}'.format(encoded)
    else:
        return encoded

def decryption(data):
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    cipher = AES.new(secretKey)
    decoded = DecodeAES(cipher, data)
    return decoded

def createEmailAccount(email, name, birthDate, password):

    if password == '' or password == ' ':
        password = createPassword(10)
        print "\nThe password generated is {}".format(password)
    if password != '':
        pass

    createEmailFile(email, name, birthDate, password)

def createEmailFile(email, name, birthDate, password):
    emailFile = "{}/{}.txt".format(directory, encryption(email, True))

    if not os.path.isfile(emailFile):
        write_file(emailFile, encryption('Email: {} \nName:{} \nBirth-Date:{} \nPassword:{}\n'.format(email, \
        name, birthDate, password)))
    else:
        print "Email already exists"

def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

def createPassword(passLength):
    password = ''
    for x in range(0, passLength):
        randomLetter = random.randint(0, len(passwordRandomizer)-1)
        password += passwordRandomizer[randomLetter]
    return password

def addAccountForEmail(domainName, email, username, password):
    emailFile = "{}/{}.txt".format(directory, encryption(email, True))

    if password == '' or password == ' ':
        password = createPassword(10)
        print "\nThe password generated is {}".format(password)
    if password != '':
        pass
    
    append_to_file(emailFile, encryption('{}\n\
    Email: {}\n\
    Username:{} \n\
    Password:{}\n'.format(domainName, email, username, password)))

def displayFileContents(email):
    with open ('{}/{}.txt'.format(directory, encryption(email, True)), 'rb') as f:
        for line in f:
            print decryption(line)

def displayEmails():
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            print(decryption(file[:-4]))

def userInput():
    exit = False

    print "To add a new email account, type: new email. \n\
To add an user account associated with an email, type: add account. \n\
To simply create a password, type: password generator.\n\
To view a file, type: display file.\n\
To change the encryption key, type: change key. \n\
To display your emails, type: display emails. \n"

    while not exit:
        uInput = raw_input("Input: ")

        if uInput.lower() == 'new email':
            print "\nPress Enter/Return when finished with your input. \n"
            email = raw_input("Enter the email address you would like to add: \n")
            name = raw_input("Enter the name associated with the email account (Can be left blank): \n")
            birthDate = raw_input("Enter the birth date associated with the email account (Can be left blank): \n")
            password = raw_input("Press enter for a randomly generated password, or type your own password: \n")
            createEmailAccount(email, name, birthDate, password)
            
        if uInput.lower() == "add account":
            domainName = raw_input("\nEnter the name of the website/application, for this user account: \n")
            email = raw_input("\nEnter the email used for this account: \n")
            username = raw_input("\nEnter the username for this account: \n")
            password = raw_input("Press enter for a randomly generated password, or type your own password: \n")
            addAccountForEmail(domainName, email, username, password)
            
        if uInput.lower() == "password generator":
            print "Generated password: {} \n".format(createPassword(10))
            
        if uInput.lower() == "display file":
            email = raw_input("Enter the email to view its, passwords, and accounts: \n")
            print
            displayFileContents(email)

        if uInput.lower() == "change key":
            secretKey = raw_input("Enter the new encryption key \n\
(you will still need to use the previous key, in order to access the data encrypted with it): \n")

        if uInput.lower() == "display emails":
            displayEmails()

userInput()

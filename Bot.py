from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
from selenium.webdriver.common.keys import Keys
import time 
import random
import getpass
import re
import os

#chrome_options.add_argument("--headless")

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def userFile(fileName):
    
    if not isInPath(fileName): file = open(fileName,"w+")
    else: file = open(fileName, "a")
    while True:
        print("Ingresar usuario a comentar o EXIT para salir")
        user = input("Usuario: ")

        if user.upper() != "EXIT":
            user = user.replace(" ", "")
            user = '@' + user
            file.write("%s\n" % user)
        else: break

    file.close() 

def openFile(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print("No existe", fileName)
        userFile(fileName)
        openFile(fileName)
    if os.path.getsize(fileName) == 0:
        print("El archivo", fileName, "esta vacio")
        userFile(fileName)
        openFile(fileName)

def botComment(fname):
    openFile(fname)
    f = open(fname, 'r')
    usersList = []
    usersList = re.findall(r'(@.*)', f.read())

    username = input("Ingrese su usuario: ")
    password = getpass.getpass("Ingrese su contraseña: ")
    url = input("Ingrese la URL del post a comentar: ")
    quantity = int(input("Ingrese la cantidad a taguear: "))
    if quantity > len(usersList):
        quantity = len(usersList)

    global chrome
    chrome = webdriver.Chrome(options = chrome_options)
    chrome.get("https://www.instagram.com/")
    time.sleep(random.randint(9, 15))
    usern = chrome.find_element_by_name("username")     
    usern.send_keys(username)    
    passw = chrome.find_element_by_name("password")     
    passw.send_keys(password)       
    log_cl = chrome.find_element_by_class_name("L3NKy")     
    log_cl.click()
    time.sleep(random.randint(2, 4))
    not_now = chrome.find_element_by_class_name("sqdOP.yWX7d.y3zKF")     
    not_now.click()
    time.sleep(random.randint(2, 4))
    while True:
        makeComment(usersList, quantity, url)

def makeComment(userList, quantity, postURL):
    chrome.get(postURL)
    time.sleep(random.randint(6, 12))
    commentArea = chrome.find_element_by_class_name('Ypffh')
    commentArea.click()
    time.sleep(random.randint(2, 4))
    commentArea = chrome.find_element_by_class_name('Ypffh')
    commentArea.click()
    users = random.sample(userList, quantity)

    for i in range(quantity):
        commentArea.send_keys(users[i])
        commentArea.send_keys(" ")

    commentArea.send_keys(Keys.ENTER)
    time.sleep(random.randint(250, 380))

def convert(s): 
    new = "" 
    for x in s: 
        new += x  
    return new 

def isInPath(fname):
    dir = __file__
    i = 0
    lista = list(dir)
    while i != 6:

        del lista[-1]
        i += 1

    return find(fname, convert(lista))

def startBot():
    possibleAnswers = ['A', 'I']
    print("Que desea realizar: - (A)gregar Usuarios Al Archivo")
    print("                    - (I)niciar Bot")
    option = input("Su respuesta: ")

    while option not in possibleAnswers:
        option = input("Ingrese una opcion valida:")

    if option.upper() == 'A': userFile("Usuarios.txt")
    else: botComment("Usuarios.txt")

startBot()
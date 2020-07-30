from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
from selenium.webdriver.common.keys import Keys
import time 
import random
import getpass
import re
import os
import datetime 

possibleAnswers = ['S', 'N']
option = input("Desea visualizar los movimientos realizados? (S/N): ")

while option.upper() not in possibleAnswers:
    option = input("Ingrese una opcion valida (S/N): ")

if option.upper() == 'N':
    chrome_options.add_argument("--headless")

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def insertToFile(fileName):
    
    if not isInPath(fileName): file = open(fileName,"w+")
    else: file = open(fileName, "a")
    while True:
        if fileName == "Usuarios.txt":
            print("Ingresar usuario a comentar o EXIT para salir")
            user = input("Usuario: ")

            if user.upper() != "EXIT":
                user = user.replace(" ", "")
                user = '@' + user
                file.write("%s\n" % user)
            else: break
        else:
            print("Ingresar URL de sorteo o EXIT para salir")
            giveAway = input("URL: ")

            if giveAway.upper() != "EXIT":
                giveAway = giveAway.replace(" ", "")
                file.write("%s\n" % giveAway)
            else: break

    file.close() 

def openFile(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print("No existe", fileName)
        insertToFile(fileName)
        openFile(fileName)
    if os.path.getsize(fileName) == 0:
        print("El archivo", fileName, "esta vacio")
        insertToFile(fileName)
        openFile(fileName)

def isStopTime(day, hour, minutes):
    now = datetime.datetime.now()
    isDay = day == now.day
    isHour = hour == now.hour
    isMinute = minutes <= now.minute

    return isDay and isHour and isMinute

def getNumber(text): return int(input(text))

def getTime(stopTime):
    hour = int(stopTime[:2])
    minutes = int(stopTime[3:])

    return (hour, minutes)

def botComment():
    userFile = "Usuarios.txt"
    giveAwayFile = "Sorteos.txt"

    openFile(userFile)
    f = open(userFile, 'r')
    usersList = []
    usersList = re.findall(r'(@.*)', f.read())
    f.close()

    openFile(giveAwayFile)
    f = open(giveAwayFile, 'r')
    giveAwayList = []
    giveAwayList = re.findall(r'https://www\.instagram\.com/p/.*|www\.instagram\.com/p/.*', f.read())
    f.close()

    username = input("Ingrese su usuario: ")
    password = getpass.getpass("Ingrese su contraseña: ")
    quantity = getNumber("Ingrese la cantidad a taguear: ") 

    possibleAnswers =['S', 'N']
    option = input("Desea setear un timer para finalizar automaticamente (S/N):")

    while option.upper() not in possibleAnswers:
        option = input("Ingrese una opcion valida (S/N): ")

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

    giveAway = 0

    tempList = [elem for elem in usersList]
    random.shuffle(tempList)

    if option.upper() == 'S':
        day = getNumber("Ingrese el día a terminar: ")
        stopTime = input("Ingrese la hora a terminar (HH:MM): ")
        hour, minutes = getTime(stopTime)

        while not isStopTime(day, hour, minutes):
            if tempList == []:
                giveAway += 1
                tempList = [elem for elem in usersList]
                random.shuffle(tempList)
            
            if giveAway == len(giveAwayList):
                giveAway = 0

            makeComment(tempList, quantity, giveAwayList[giveAway])
    
    else:
        while True:
            if tempList == []:
                giveAway += 1
                tempList = [elem for elem in usersList]
                random.shuffle(tempList)
            
            if giveAway == len(giveAwayList):
                giveAway = 0

            makeComment(tempList, quantity, giveAwayList[giveAway])



def makeComment(usersList, quantity, postURL):

    chrome.get(postURL)
    time.sleep(random.randint(6, 12))

    commentArea = chrome.find_element_by_class_name('Ypffh')
    commentArea.click()
    time.sleep(random.randint(2, 4))

    commentArea = chrome.find_element_by_class_name('Ypffh')
    commentArea.click()
    users = []

    if quantity > len(usersList):
        quantity = len(usersList)

    for elem in range(quantity):
        users.append(usersList.pop())

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
    possibleAnswers = ['AU', 'I', 'AS']
    print("Que desea realizar: - (A)gregar (U)suarios Al Archivo")
    print("                    - (A)gregar (S)orteos Al Archivo")
    print("                    - (I)niciar Bot")
    option = input("Su respuesta: ")

    while option.upper() not in possibleAnswers:
        option = input("Ingrese una opcion valida:")

    if option.upper() == 'AU': insertToFile("Usuarios.txt")
    elif option.upper() == 'AS': insertToFile("Sorteos.txt")
    else: botComment()

startBot()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
from selenium.webdriver.common.keys import Keys
import time 
import random
import re
import os
chrome_options.add_argument("--headless")
def archivoDeUsuarios():
    f= open("usuarios.txt","w+")
    while (True):
        print("ingresar usuario con el @ para seguir agregando o cualquier otra cosa no nulla para terminar de ingresar")
        arroba = input()
        if(arroba[0] == '@'):
            f.write("%s\n"%arroba)
        else:
            break
    f.close() 

def openfile(filename):
    fname = filename
    try:
        f = open(fname, 'r')
    except FileNotFoundError:
        print("no existe el archivo de personas a arrobar")
        archivoDeUsuarios()
        openfile(fname)
    if(os.path.getsize(fname) == 0):
        print("El archivo de personas a arrobar esta vacio agrega usuarios capo")
        archivoDeUsuarios()
        openfile(filename)

def botcomment():
    fname = 'usuarios.txt'
    openfile(fname)
    f = open(fname, 'r')
    lst = []
    lst = re.findall(r'(@.*)', f.read())
    print("enter username") 
    username = input() 
    print("enter password") 
    password = input() 
    print("ingresar la url del post a comentar") 
    url = input()
    print("ingrese a cuantos usuarios arrobar")
    cant = int(input())

    global chrome
    #webdriver.Chrome(options=chrome_options)
    #webdriver.Chrome(executable_path = "chromedriver.exe")
    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get("https://www.instagram.com/")
    time.sleep(random.randint(9, 15))
    usern = chrome.find_element_by_name("username")     
    usern.send_keys(username)    
    passw = chrome.find_element_by_name("password")     
    passw.send_keys(password)       
    log_cl = chrome.find_element_by_class_name("L3NKy")     
    log_cl.click()
    time.sleep(random.randint(4, 9))
    not_now = chrome.find_element_by_class_name("sqdOP.yWX7d.y3zKF")     
    not_now.click()
    time.sleep(random.randint(4, 9))
    for i in(0, 150):
        commentar(lst, cant, url)
        i+=1
    chrome.quit()

def commentar(lista_usuarios, var_cantidad, post_url):
    url = post_url
    cant = var_cantidad
    lst = lista_usuarios
    chrome.get(url)
    time.sleep(random.randint(10, 15))
    commentArea = chrome.find_element_by_class_name('Ypffh')
    commentArea.click()
    time.sleep(random.randint(4, 9))
    commentArea = chrome.find_element_by_class_name('Ypffh')
    commentArea.click()
    usuarios = random.sample(lst, cant)
    for i in range(0, cant):
        commentArea.send_keys(usuarios[i])
        commentArea.send_keys(" ")
    commentArea.send_keys(Keys.ENTER)
    time.sleep(random.randint(250, 380))

def startBot():
    print("ingrese 1 para crear lista de usuarios a etiquetar o cualquier cosa para iniciar el bot")
    desicion = input()
    if(desicion == 1):
        archivoDeUsuarios()
    else:
            botcomment()
startBot()

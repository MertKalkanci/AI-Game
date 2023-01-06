import openai
import PySimpleGUI as GUI
import cloudscraper
from tkinter import *
from PIL import Image , ImageTk
import os
import io

currentUI = "start"
currentGameFile = "game_main.txt"
currentGame = ""


def readfile(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        print("Error : " + str(e))
        input("waiting for input to quit program")
        exit()



key = readfile("key.txt")


try:
    openai.api_key = key
except Exception as e:
    print("Error  :" + e)

def gpt3(x):
    try: 
        response = openai.Completion.create(
            engine ="text-curie-001",
            prompt = x,
            temperature = 0.35,
            max_tokens = 100,)
        return response.choices[0].text
    except Exception as e:
        return "Error : " + str(e)

def dalle(x):
    try:
        response = openai.Image.create(
            prompt=x,
            n=1,
            size="256x256",)
        image_url = response['data'][0]['url']
        
        
        image_data = (
            cloudscraper.create_scraper(    browser={"browser": "chrome", "platform": "windows", "mobile": False}    )
            .get(image_url)
            .content)

        return image_data
    except Exception as e:
        print("Error  :" + str(e))
        return 'error.png'

startLayout = [
    [GUI.Text('Default game or Custom Game ?', size=(50,10), key="Header")],
    [GUI.Button("Default Game"), GUI.Button("Custom Game")],
]

customGameSelectionLayout = [
    [GUI.Text('WriteFileLocation', size=(50,10), key="Header")],
    [GUI.Text('Input', size =(15, 1)), GUI.InputText()],
    [GUI.Button("Continue")],
]

gameLayout = [
    [GUI.Text('Header', size=(50,10), key="Header")],
    [GUI.Image('temp.png', key="Image")],
    [GUI.Text('Input', size =(15, 1)), GUI.InputText()],
    [GUI.Button("Continue")],
    ]

window = GUI.Window("Demo", startLayout)



while True:
    event,values = window.read()

    if(currentUI == "start"):

        if event == GUI.WIN_CLOSED: # if user closes window or clicks cancel
            GUI.exit()
        if event == "Default Game":
            currentUI = "gameStart"
        if event == "Custom Game":
            window.close()
            window = GUI.Window("Demo", customGameSelectionLayout)
            currentUI = "gameSelection"

    if(currentUI == "gameSelection"):

        if event == GUI.WIN_CLOSED:
            GUI.exit()
        if event == "Continue":
            currentGameFile = values[0]
            currentUI = "gameStart"



    if(currentUI == "gameStart"):
        window.close()
        window = GUI.Window("Game", gameLayout)
        currentGame = readfile(currentGameFile)


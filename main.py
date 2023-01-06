import openai
import PySimpleGUI as GUI
import cloudscraper
import textwrap
from tkinter import *
from PIL import Image
from random import randint

global dalleStyleFile
global dalleStyle
global currentUI
global currentGameFile
global gamePromptCurrent
global playerPrompt
global endPrompt
global decisionMade
global decision
global temperatureValue

dalleStyleFile = "GameStyles/game_main_style.txt"
dalleStyle = "as an epic oil painting"
currentUI = "start"
currentGameFile = "GameModes/game_main.txt"
gamePromptCurrent = ""
playerPrompt = "\nPLayer:"
endPrompt = "\n"
decisionMade = False
decision = 1
temperatureValue = 0.5


def readfile(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        print("Error : " + str(e))
        input("waiting for input to quit program")
        exit()

key = readfile("key.txt")

#region OpenAI

try:
    openai.api_key = key
except Exception as e:
    print("Error  :" + e)

def gpt3(x):
    try: 
        response = openai.Completion.create(
            engine ="text-davinci-003",
            prompt = x,
            temperature = temperatureValue,
            max_tokens = 512,
            stop = "Player:")
        print(f"\n\n\nTemperature : {temperatureValue} \n====\nResponse:\n====\n {response.choices[0].text}")
        return response.choices[0].text
    except Exception as e:
        return "GPT Error : " + str(e)

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
        print("DALLE Error  :" + str(e))
        return 'error.png'

#endregion

startLayout = [
    [GUI.Text('Default game or Custom Game ?', size=(50,10), key="Header")],
    [GUI.Text("AI Temperature Level: "),GUI.Slider(orientation ='horizontal', key='TemperatureSlider', range=(50,150))],
    [GUI.Button("Default Game"), GUI.Button("Custom Game")],
]

customGameSelectionLayout = [
    [GUI.Text('Configuration', size=(50,10), key="Header")],
    [GUI.Text('Game Text Location', size =(15, 1)), GUI.InputText("Default")],
    [GUI.Text('Image Style Text', size =(15, 1)), GUI.InputText("Default")],
    [GUI.Button("Play Game")],
]

gameLayout = [
    [GUI.Text( text="", size=(200,18), key="GameText")],
    [GUI.Image('temp.png', key="Image")],
    [GUI.Text('Make Decision', key="DecisionText")],
    #[GUI.Text('Input', size =(15, 1)), GUI.InputText()],
    [GUI.Button("No Decision")],[GUI.Button("Decision 1")],[GUI.Button("Decision 2")],

    [GUI.Button("Continue")],
]

window = GUI.Window("Demo", startLayout)

def configureGame():
    global gamePromptCurrent
    gamePromptCurrent = currentGamePrompt


def promptMaker(playerDecision):
    global gamePromptCurrent
    if playerDecision == 0:
        gamePromptCurrent += f"{playerPrompt} What's next ?{endPrompt}"
    gamePromptCurrent += f"{playerPrompt} I decide {playerDecision} what's next ?{endPrompt}"

def dallePromptMaker(gptResponse):
    output = ""
    if (gptResponse.split("\n")[0] == "" or gptResponse.split("\n")[0] == None):
        output = f"{dalleStyle} " + gptResponse.split("\n")[1]
    else:
        output = f"{dalleStyle} " + gptResponse.split("\n")[0]
        
    return output

while True:
    global currentGamePrompt
    

    event,values = window.read()

    if event == GUI.WIN_CLOSED: # if user closes window or clicks cancel
            exit()

    if(currentUI == "start"): # başlangıç menüsü
        temperatureValue = float(values["TemperatureSlider"] / 100)
         
        if event == "Default Game": # oyunu direk başlat
            currentUI = "gameStart"

        if event == "Custom Game": # oyunu ayarlama menüsüne geç
            currentUI = "gameSelection"

            window.close()
            window = GUI.Window("Demo", customGameSelectionLayout)

    if(currentUI == "gameSelection"): # oyun ayarlama menüsü
        if event == "Play Game": # oyunu başlat
            if values[0] != "Default":
                currentGameFile = values[0]
            if values[1] != "Default":
                dalleStyleFile = values[1]
            currentUI = "gameStart"
               
    if(currentUI == "gameStart"): # oyun başlatlırken pencereyelre promptu ayarla

        currentGamePrompt = readfile(currentGameFile)
        dalleStyle = readfile(dalleStyleFile)
        configureGame()

        currentUI = "game"
        
        window.close()
        window = GUI.Window("Game", gameLayout, finalize = True)
        window["GameText"].update(currentGamePrompt)

    if(currentUI == "game"):
        if event == "Continue": # sıradaki tur
            if not decisionMade:
                decision = randint(1,2)
            promptMaker(decision)
            gptResponse = gpt3(gamePromptCurrent)
            currentGamePrompt += gptResponse
            
            window["GameText"].update(gptResponse)
            window["Image"].update(data=dalle(dallePromptMaker(gptResponse)))
                

            decisionMade = False

        if event == "No Decision":
            decision = 0
            decisionMade = True

            window["DecisionText"].update(f"You decided {decision}")
        if event == "Decision 1":
            decision = 1
            decisionMade = True

            window["DecisionText"].update(f"You decided {decision}")
        if event == "Decision 2":
            decision = 2
            decisionMade = True

            window["DecisionText"].update(f"You decided {decision}")


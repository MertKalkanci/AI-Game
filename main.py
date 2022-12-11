import openai
import PySimpleGUI as GUI
import cloudscraper
from tkinter import *
from PIL import Image , ImageTk
import os
import io

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

        
        with open('temp.png', 'wb') as handler:
            handler.write(image_data)

        return 'temp.png'
    except Exception as e:
        print("Error  :" + str(e))
        return 'error.png'

layout = [
    [GUI.Text('Header', size=(50,10), key="Header")],
    [GUI.Image(dalle("a drawing of a child says !!WELCOME!!"), key="Image")],
    [GUI.Text('Input', size =(15, 1)), GUI.InputText()],
    [GUI.Button("Continue")],
     ]

window = GUI.Window("Demo", layout)

while True:
    event,values = window.read()
    if event == GUI.WIN_CLOSED: # if user closes window or clicks cancel
        GUI.exit()
    if event == "Continue":
        window['Header'].update(gpt3(values[0]))
        window['Image'].update(dalle(values[0]))

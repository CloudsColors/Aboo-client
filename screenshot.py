import pyautogui as pygui
import datetime
import os

def screenshot():
    now = datetime.datetime.now()
    fileName = "image-"+now.strftime("%m-%d %H:%M:%S")
    fileExtension = ".png"
    sh = pygui.screenshot(region=(1920,0,1920,1080))
    sh.save(r"C:\Users\Andreas\Desktop\filename.png")
    #sh.save(os.path.dirname(os.path.abspath(__file__))+"/screenshots/"+fileName+fileExtension)

if __name__ == "__main__":
    screenshot()
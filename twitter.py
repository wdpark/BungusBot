import keyboard
import webbrowser
import sys
import time

def chromeOpen(url):
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    # https://stackoverflow.com/questions/31715119/how-can-i-open-a-website-in-my-web-browser-using-python
    webbrowser.get(chrome_path).open(url)

num_to_field = 27

def type_field(text):
    for x in range(0,num_to_field):
        keyboard.press_and_release('tab')
    time.sleep(1)
    keyboard.write("check out highlights at " + text)
    time.sleep(2)
    for x in range(0,7):
        keyboard.press_and_release('tab')
    time.sleep(1)
    keyboard.press_and_release('space')
    time.sleep(1)
    keyboard.press(55)
    keyboard.press('w')
    keyboard.release(55)
    keyboard.release('w')
    time.sleep(1)
    keyboard.press(55)
    keyboard.press('tab')
    keyboard.release(55)
    keyboard.release('tab')

print(keyboard.get_shortcut_name(['tab']))

chromeOpen("https://twitter.com/")
time.sleep(3)
type_field(sys.argv[1])

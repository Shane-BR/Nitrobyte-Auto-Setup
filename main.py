import pyautogui

from sys import argv
from subprocess import Popen
from pathlib import Path

# Allows the first arg to assign an amount of time to search for the buttons before failing
button_search_time = int(argv[0]) if len(argv) > 0 and argv[0].isdigit else 15

def main ():
    paths = open("paths.txt").read().split("\n")
    for i in range(len(paths)):
        paths[i] = paths[i].split(" ") # TODO remove
        try:
            print("Launching: " + paths[i][0])
            process = Popen([paths[i][0]])

            filename = Path(paths[i][0]).stem

            navigateInstaller(filename)

            # wait until current program is finished then close it
            # current then equals next opened program
            # loop this until no more open programs remain

        except:
            print("Unable to launch: " + paths[i][0])
        

def navigateInstaller(filename):
    # click all nececary buttons to begin instalation
    # ALL PROGRAMS SHOULD BE INSTALLING AT THE SAME TIME

    # find folder that is called "filename"
    # press each button png in step order
    step = 1
    path = "resources/" + filename + "/" + str(step) + ".PNG"
    while button := pyautogui.locateOnScreen(path, minSearchTime=button_search_time) != None:
        pyautogui.click(button)
        step += 1
    else:
        print("Unable to locate button for step " + step +  "!")
    

if __name__ == "__main__":
    main()

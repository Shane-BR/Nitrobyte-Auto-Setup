import pyautogui
import subprocess

from pathlib import Path

def main ():
    paths = open("paths.txt").read().split("\n")
    for i in range(len(paths)):
        paths[i] = paths[i].split(" ") # TODO remove
        try:
            print("Launching: " + paths[i][0])
            process = subprocess.Popen([paths[i][0]])

            filename = Path(paths[i][0]).stem

            navigateInstaller(filename)
            # click all nececary buttons to begin instalation
            # ALL PROGRAMS SHOULD BE INSTALLING AT THE SAME TIME

        except:
            print("Unable to launch: " + paths[i][0])
        

def navigateInstaller(filename):
    # find folder that is called "filename"
    # press each button png in step order
    step = 1
    while button := pyautogui.locateOnScreen("resources/" + filename + "/" + str(step) + ".png", grayscale=False) != None:
        pyautogui.click(button)
        step += 1
    

if __name__ == "__main__":
    main()

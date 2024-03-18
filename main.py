import pyautogui
import win32api
import win32con

from pywintypes import DEVMODEType
from sys import argv
from subprocess import Popen, check_output
from pathlib import Path
from time import sleep

# Allows the first arg to assign an amount of time to search for the buttons before failing
button_search_time = int(argv[1]) if len(argv) > 1 and argv[1].isdigit else 3
op_width = int(argv[2]) if len(argv) > 2 and argv[2].isdigit else 1280
op_height = int(argv[3]) if len(argv) > 3 and argv[3].isdigit else 1024

init_width = win32api.GetSystemMetrics(0)
init_height = win32api.GetSystemMetrics(1)

def main ():

    # change os resolution to fit the given screenshots
    setWindowsResolution(op_width, op_height)

    paths = open("paths.txt").read().split("\n")
    for i in range(len(paths)):
        paths[i] = paths[i].split(" ") # TODO remove
        try:
            print("Launching: " + paths[i][0])
            process = Popen([paths[i][0]])

            filename = Path(paths[i][0]).stem

            navigateInstaller(filename)

        except:
            print("Unable to launch: " + paths[i][0])

    # wait until current program is finished then close it
    # current then equals next opened program
    # loop this until no more open programs remain

    while True:
        processes_running = 0
        for i in range(len(paths)):
            process = Path(paths[i][0]).name
            if (isProcessRunning(process)):
                # is there a finish button?
                finish_button_img_path = "resources/" + process.split(".")[0] + "/finish.PNG"
                if (button := pyautogui.locateOnScreen(finish_button_img_path, minSearchTime=button_search_time)) != None:
                    pyautogui.click(button)
                else:
                    processes_running += 1

        if processes_running == 0:
            break




    # change resolution back to original
    setWindowsResolution(init_width, init_height)   

def navigateInstaller(filename):
    # click all nececary buttons to begin instalation
    # ALL PROGRAMS SHOULD BE INSTALLING AT THE SAME TIME

    # find folder that is called "filename"
    # press each button png in step order
    step = 1
    base_path = "resources/" + filename
    while (button := pyautogui.locateOnScreen(base_path + "/" + str(step) + ".PNG", minSearchTime=button_search_time)) != None:
        pyautogui.moveTo(button)
        sleep(5)
        step += 1
    
def setWindowsResolution(width, height):
    devmode = DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(devmode, 0)

def isProcessRunning(process_name):
    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)
    out = check_output(cmd, shell=True).decode()

    return process_name.lower() in out.lower()

if __name__ == "__main__":
    main()

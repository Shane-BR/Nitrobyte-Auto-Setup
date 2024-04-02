import os

from subprocess import Popen
from pathlib import Path
from time import sleep

def main ():

    os.system("") # needed for ANSI escape codes ¯\_(ツ)_/¯
    paths = open("paths.txt").read().split("\n")
    processes = []
    for i in range(len(paths)):

            if os.path.isfile(paths[i]) == False:
                continue

            p = Popen("msiexec.exe /i {} /qn ".format(os.path.abspath(paths[i]))) if paths[i].endswith("msi") else Popen(paths[i] + " /S /s /silent /verysilent -qn -s /norestart")
            processes.append(p)
    
    # Loop through all processes and see if they are still running or if they are done
    # check each 1/10 second
    syms = "|/-\\"
    loading_index = 0
    while True:
        cur_running = 0

        fails = 0

        print("\033[H", end="")
        print('\033[?25l', end="")
        loading_index += 1
        for process in processes:
            process.poll()
            loading_char = syms[loading_index % len(syms)]

            exec = process.args.split(" ")
            name = os.path.basename(exec[2] if exec[0] == "msiexec.exe" else exec[0])

            if process.returncode == None:
                 print(name + " - \033[1m" + loading_char)
                 cur_running += 1
            elif process.returncode != 0:
                 print(name + " - \033[1;31m ERR ({})".format(process.returncode))
                 fails += 1
            elif process.returncode == 0:
                 print(name + " - \033[1;32m DONE")
            
            print("\033[0m", end="")
        
        if (cur_running <= 0):
             break
        
        sleep(0.1)

    print('\033[?25h', end="")

    num_process = len(processes)
    print("\nSuccessfully installed {}/{} programs.".format(num_process-fails,num_process))
    os.system("pause")
         

if __name__ == "__main__":
    main()
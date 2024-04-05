import os
import sys
import json
from subprocess import Popen, call
from time import sleep

def main ():

    # CMD ARGS
    args = get_args()
    loading_type = args.get("--loading_type")
    sequential_loading = args.get("--seq") != None # MSI files will always wait for the last MSI file to finish
    path_file_arg = args.get("--path_file")
    path_file = path_file_arg if path_file_arg != None else "paths.txt"

    os.system("") # needed for ANSI escape codes ¯\_(ツ)_/¯

    try:
        paths = open(path_file).read().split("\n")
    except Exception as e:
        print(e)
        os.system("pause")
        exit(1)

    # skip whitespace and fill dict with paths as key (empty for now)
    processes = {}
    for path in paths:

        if not os.path.isfile(path):
            continue

        process = new_process(path) if not sequential_loading and not is_msi(path) else None
        processes.update({path : process})

    # Loop through all processes and see if they are still running or if they are done
    # check each 1/10 second
    syms = get_loading_type(loading_type)
    loading_index = 0
    while True:

        cur_loading = False
        msi_running = False
        install_fails = 0


        print("\033[H", end="")
        print('\033[?25l', end="")
        loading_index += 1
        for key in processes:

            name = os.path.basename(key)
            process = processes[key]

            if process == None:
                print(name + " - \033[1;36m Waiting" + "."*(1+(loading_index%3)) + "\033[0m \033[K") # dumb fix - color bleeding onto other text for some reason
                continue

            process.poll()
            loading_sym = syms[loading_index % len(syms)]

            if process.returncode == None:
                print(name + " - \033[34;1m" + loading_sym + "\033[K")
                cur_loading = True

                if is_msi(key):
                    msi_running = True

            elif process.returncode != 0:
                print(name + " - \033[1;31m ERR ({})\033[K".format(process.returncode))
                install_fails += 1
            else:
                print(name + " - \033[1;32m DONE\033[K")

            print("\033[0m", end="")
        if not cur_loading or (not msi_running and not sequential_loading):
            # Find next waiting process
            for key in processes: # key = the path to the installer

                handle_msi = is_msi(key) if cur_loading else True

                if processes[key] == None and handle_msi:
                    processes[key] = new_process(key)
                    cur_loading = True
                    break

            if not cur_loading:
                break       

        sleep(0.15)

    print('\033[?25h', end="")

    num_process = len(processes)
    print("\nSuccessfully installed {}/{} programs.".format(num_process-install_fails,num_process))

    while True:
        restart = input("Would you like to restart the PC (Y/N): ").lower()
        if restart == 'y':
            print("Restarting...")
            call(["shutdown", "-r", "-t", "0"])
            break
        elif restart == 'n':
            print("\033[1A",end="")
            break
        
         

    os.system("pause")
    
def get_args():
    args = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            split = arg.split("=")
            args.update({split[0] : split[1]})

    return args

def get_loading_type(type):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    loading_options = json.loads(open(os.path.join(base_path, "loading_types.json")).read())
    
    if type != None and type in loading_options:
        return loading_options[type]
    
    return loading_options["spinning_bar"]


def new_process(path):
    return Popen('msiexec.exe /i "{}" /qn '.format(os.path.abspath(path))) if path.endswith("msi") else Popen(path + " /S /s /silent /verysilent -qn -s /norestart")

def is_msi(path):
    return os.path.basename(path).endswith("msi")

if __name__ == "__main__":
    main()
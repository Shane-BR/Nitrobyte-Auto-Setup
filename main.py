import json
import os
from subprocess import Popen, call
import subprocess
import sys
from time import sleep

SILENT_PARAMS = ["/s", "/S", "-s", "/q", "-q", "/silent", "-silent", "/unattended", "-unattended", "/quiet", "-quiet", "/veryquiet" "-veryquiet"]
NO_RESTART_PARAM = "/norestart"
processes = {}

def main ():

    # CMD ARGS
    args = get_args()
    loading_type = args.get("--loading_type")
    sequential_loading = args.get("--seq") is not None # MSI files will always wait for the last MSI file to finish
    path_file_arg = args.get("--path_file")
    path_file = path_file_arg if path_file_arg is not None else "paths.txt"

    os.system("") # needed for ANSI escape codes ¯\_(ツ)_/¯

    try:
        paths = open(path_file).read().split("\n")
    except Exception as e:
        print(e)
        os.system("pause")
        exit(1)

    silent_string = list_of_params_to_string(SILENT_PARAMS)

    # skip whitespace and fill dict with paths as key (empty for now)
    for path in paths:

        if not os.path.isfile(path):
            continue

        process = new_process(path, get_next_params(None)) if not sequential_loading and not is_msi(path) else None
        processes.update({path : process})

    # Loop through all processes and see if they are still running or if they are done
    # check each 1/10 second
    syms = get_loading_type(loading_type)
    loading_index = 0
    while True:

        cur_loading = False
        msi_running = False
        install_fails = 0

        #print("\033[H", end="")
        #print('\033[?25l', end="")
        loading_index += 1
        for key in processes:

            name = os.path.basename(key)
            process = processes[key]

            if process is None:
                #print(name + " - \033[1;36m Waiting" + "."*(1+(loading_index%3)) + "\033[0m \033[K") # dumb fix - color bleeding onto other text for some reason
                continue

            process.poll()
            loading_sym = syms[loading_index % len(syms)]

            if process.returncode is None:
                #print(name + " - \033[34;1m" + loading_sym + "\033[K")
                cur_loading = True

                if is_msi(key):
                    msi_running = True

            elif process.returncode is 87: # Incorrect params
                # Retry with reduced params
                process = new_process(key, get_next_params(process))
                cur_loading = True

            elif process.returncode is not 0:
                #print(name + " - \033[1;31m ERR ({})\033[K".format(process.returncode))
                install_fails += 1
            #else:
                #print(name + " - \033[1;32m DONE\033[K")

            #print("\033[0m", end="")
        if not cur_loading or not sequential_loading:
            # Find next waiting process
            for key in processes: # key = the path to the installer

                if processes[key] is None and not (is_msi(key) and msi_running):
                    processes[key] = new_process(key, get_next_params(None)) # None for new process
                    cur_loading = True
                    break

            if not cur_loading:
                break       

        sleep(0.15)

    #print('\033[?25h', end="")

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

def get_loading_type(t):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    loading_options = json.loads(open(os.path.join(base_path, "loading_types.json")).read())
    
    if t is not None and t in loading_options:
        return loading_options[t]
    
    return loading_options["spinning_bar"]


def new_process(path, params):
    msi = is_msi(path)
    process = Popen('msiexec.exe /i "{}" /qn /norestart'.format(os.path.abspath(path)), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) if msi else Popen(path + " " + params, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) # Initial brute force approach
    return process
        
def get_next_params(process):

    # If there is no process return SILENT_PARAMS with NO_RESTART_PARAM
    if process is None:
        return list_of_params_to_string(SILENT_PARAMS) + " " + NO_RESTART_PARAM

    # pop off the front parameter and return it as a string
    cur_params = process.args[1:]

    # Equal with or without /norestart
    equal_silent = True
    for p in cur_params:
        if p not in SILENT_PARAMS and p is not NO_RESTART_PARAM:
            equal_silent = False

    if equal_silent:
        # Take first param in the list and return it
        return SILENT_PARAMS[0]
    elif (p := cur_params[0]) in SILENT_PARAMS:
        # Assume there is only one silent param
        # find the current param position in SILENT_PARAMS
        index = SILENT_PARAMS.index(p)
        # return param plus /norestart if /norestart exists in the original params
        rs = SILENT_PARAMS[index+1] + ((" " + NO_RESTART_PARAM) if NO_RESTART_PARAM in cur_params else "")
        print(rs)
        return rs
    
    # If the silent param(s) neither are equal to the entire SILENT_PARAMS list nor equal to one single param in it
    # return SILENT_PARAMS without the /norestart, indicating that /norestart may be the reason for error code 87
    return list_of_params_to_string(SILENT_PARAMS)

def list_of_params_to_string(params):
    s = ""
    for p in params:
        s = s + p + " "

    return s

def is_msi(path):
    return os.path.basename(path).endswith("msi")

if __name__ == "__main__":
    main()

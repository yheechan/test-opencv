#!/usr/bin/python3

import subprocess as sp
from pathlib import Path
import time
import multiprocessing
import json

home_dir = Path.home()


current_file = Path(__file__).resolve()
current_dir = current_file.parent
read_data_dir = current_dir / "read_data-v1"
answer_file = current_dir / "answer.txt"

def get_data(txt_file):
    data = {}
    with open(txt_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            info = line.split(" ")
            if info[0] == "Module:":
                module_name = info[1]
                data[module_name] = {}
            else:
                key = info[0][:-1]
                value = info[1]
                data[module_name][key] = value
    return data

def check_each_server(answer):
    for server_result in read_data_dir.iterdir():
        filename = server_result.name
        server_name = filename.split(".")[0][9:] + ".swtv"
        print(f"Checking {server_name}")
        data = get_data(server_result)
        check_data(server_name, data, answer)

def check_data(server_name, data, answer):
    error = []
    for module in data:
        for key in data[module]:
            if key == "total_time_taken":
                continue
            if key in answer[module]:
                if data[module][key] != answer[module][key]:
                    error.append(f"\t{module} {key} {data[module][key]} != {answer[module][key]}")
    
    if len(error) > 0:
        print(f"Error in {server_name}")
        for e in error:
            print(e)
        print()
    else:
        print(f"No error in {server_name}")

        

def main():
    answer = get_data(answer_file)
    check_each_server(answer)
    # data = {}
    # for server_result in read_data_dir.iterdir():
    #     filename = server_result.name
    #     server_name = filename.split(".")[0][9:] + ".swtv"
    #     data[server_name] = {}
        
    #     with open(server_result, "r") as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             line = line.strip()
    


if __name__ == '__main__':
    main()

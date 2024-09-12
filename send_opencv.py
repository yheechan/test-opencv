#!/usr/bin/python3

import subprocess as sp
from pathlib import Path
import time
import multiprocessing

home_dir = Path.home()


server_file =  home_dir / ".hosts/mbfl_servers"
current_file = Path(__file__).resolve()
current_dir = current_file.parent
opencv_zip = current_dir / "opencv-4.10.0-240911-v1.zip"
server_file = current_dir / "redo.txt"

def get_servers_list():
    with open(server_file, "r") as f:
        servers = f.read().splitlines()
    return servers

def send_opencv_zip(servers):
    cnt = 0
    jobs = []
    for server in servers:
        job = multiprocessing.Process(target=send_opencv_zip_to_server, args=(server,))
        jobs.append(job)
        job.start()
        cnt += 1
        if cnt % 5 == 0:
            time.sleep(1)
    
    for job in jobs:
        job.join()

def send_opencv_zip_to_server(server):
    sp.run(["scp", opencv_zip, f"{server}:~"], cwd=current_dir)
    print(f"Sent opencv.zip to {server}")

def unzip_opencv_zip(servers):
    cnt = 0
    jobs = []
    for server in servers:
        job = multiprocessing.Process(target=unzip_opencv_zip_on_server, args=(server,))
        jobs.append(job)
        job.start()
        cnt += 1
        if cnt % 5 == 0:
            time.sleep(1)
    
    for job in jobs:
        job.join()

def unzip_opencv_zip_on_server(server):
    sp.run(["ssh", server, "unzip", "-q", "opencv-4.10.0-240911-v1.zip", "-d", "test-opencv"], cwd=home_dir)
    print(f"Unzipped opencv.zip in {server}")

def execute_test(servers):
    jobs = []
    sleep_cnt = 0
    for server in servers:
        job = multiprocessing.Process(target=test_remote, args=(server,))
        jobs.append(job)
        job.start()
        sleep_cnt += 1
        if sleep_cnt % 5 == 0:
            time.sleep(1)
    
    for job in jobs:
        job.join()

def test_remote(server):
    # also write the output to a file
    cmd = ["ssh", server, f"cd test-opencv/opencv-4.10.0/ && time ./record_data.py > outuput_{server}.txt"]
    sp.run(cmd, cwd=home_dir)
    print(f"Tested opencv in {server}")

def execute_read(servers):
    jobs = []
    sleep_cnt = 0
    for server in servers:
        job = multiprocessing.Process(target=read_remote, args=(server,))
        jobs.append(job)
        job.start()
        sleep_cnt += 1
        if sleep_cnt % 5 == 0:
            time.sleep(1)
    
    for job in jobs:
        job.join()

def read_remote(server):
    # also write the output to a file
    cmd = ["ssh", server, f"cd test-opencv/opencv-4.10.0/ && time ./read_results.py > read_data{server}.txt"]
    sp.run(cmd, cwd=home_dir)
    print(f"Read opencv in {server}")

def bring_read_data(servers):
    read_data_dir = current_dir / "read_data"
    read_data_dir.mkdir(exist_ok=True)

    cnt = 0
    for server in servers:
        sp.run(["scp", f"{server}:~/test-opencv/opencv-4.10.0/read_data{server}.txt", f"{read_data_dir}/read_data{server}.txt"])
        print(f"Read data from {server}")
        cnt += 1
        if cnt % 5 == 0:
            time.sleep(1)

def main():
    server_list = get_servers_list()
    send_opencv_zip(server_list)
    unzip_opencv_zip(server_list)
    execute_test(server_list)
    execute_read(server_list)
    bring_read_data(server_list)
    


if __name__ == '__main__':
    main()

#!/home/user01/py_venv/paramiko-async-dev01/bin/python
"""
Dev for paramiko asyncio
"""

import concurrent.futures
import paramiko
import typing
import time



d1 = {
    "hostname": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show clock",
}
d2 = {
    "hostname": "192.168.100.2",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip route",
}
d3 = {
    "hostname": "192.168.100.3",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip interface brief",
}
d4 = {
    "hostname": "192.168.100.4",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show clock",
}
d5 = {
    "hostname": "192.168.100.5",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip route",
}
d6 = {
    "hostname": "192.168.100.6",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip interface brief",
}

d7 = {
    "hostname": "192.168.100.7",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show clock",
}
d8 = {
    "hostname": "192.168.100.8",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip route",
}
d9 = {
    "hostname": "192.168.100.9",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip interface brief",
}
d10 = {
    "hostname": "192.168.100.10",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip route",
}

l = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10,]


def ssh_connect(input_dict: dict) -> bytes:
    """
    Dev
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        input_dict["hostname"],
        username=input_dict["username"],
        password=input_dict["password"]
        )
    stdin, stdout, stderr = ssh_client.exec_command(input_dict["cli_cmd"])
    time.sleep(5)
    ssh_client.close()
    ssh_output_bytes = stdout.read()

    h = input_dict['hostname'].replace('.', '_')
    d = {'hostname': h, 'cli_output': ssh_output_bytes}

    return d


def write_file(input_dict, write_mode: str = 'w') -> None:
    file_name = f"{input_dict['hostname']}.txt"
    cli_output = input_dict['cli_output'].decode('utf-8')
    with open(file_name, write_mode) as f:
        f.write(cli_output)


if __name__ == '__main__':
    t_start1 = time.time()

    with concurrent.futures.ThreadPoolExecutor() as p:
        r = p.map(ssh_connect, l)
    
    print(time.time() - t_start1)
    t_start2 = time.time()

    with concurrent.futures.ThreadPoolExecutor() as p:
        p.map(write_file, r)
    
    print(time.time() - t_start2)
    print(time.time() - t_start1)

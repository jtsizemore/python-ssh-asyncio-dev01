#!/home/user01/py_venv/paramiko-async-dev01/bin/python
"""
Dev for paramiko asyncio
"""

import concurrent.futures as cfut
import paramiko
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
    "cli_cmd": "show interface description",
}
d3 = {
    "hostname": "192.168.100.3",
    "username": "cisco",
    "password": "cisco",
    "cli_cmd": "show ip interface brief",
}

l = [d1, d2, d3]


def main(input_dict):
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

    print(len(ssh_output_bytes))

    # return ssh_output_bytes


if __name__ == '__main__':
    t_start = time.time()

    with cfut.ThreadPoolExecutor() as p:
        p.map(main, l)
    
    print(time.time() - t_start)

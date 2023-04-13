#!/home/user01/py_venv/paramiko-async-dev01/bin/python
"""
Dev for paramiko asyncio
"""

import concurrent.futures
import paramiko
import typing
import time
import yaml


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


def write_file(input_dict, file_path="no_git_tmp", write_mode: str = 'w') -> None:
    """
    Dev
    """
    file_name = f"{file_path}/{input_dict['hostname']}.txt"
    cli_output = input_dict['cli_output'].decode('utf-8')
    with open(file_name, write_mode) as f:
        f.write(cli_output)


def yaml_func(input_file, file_mode="r"):
    """
    Dev
    """
    with open(input_file, file_mode) as f:
        s = f.read()
    return yaml.safe_load(s)


if __name__ == '__main__':
    t_start1 = time.time()

    l = yaml_func("network-device.yaml")

    with concurrent.futures.ThreadPoolExecutor() as p:
        r = p.map(ssh_connect, l)
    
    print(time.time() - t_start1)
    t_start2 = time.time()

    with concurrent.futures.ThreadPoolExecutor() as p:
        p.map(write_file, r)
    
    print(time.time() - t_start2)
    print(time.time() - t_start1)

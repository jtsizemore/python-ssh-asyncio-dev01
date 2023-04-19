#!/home/user01/py_venv/paramiko-async-dev01/bin/python
"""
Dev for paramiko asyncio
"""

import concurrent.futures
import paramiko
import argparse
import typing
import time
import yaml
import re


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


def write_file(input_dict: str, file_path: str='no_git_tmp', write_mode: str='w') -> None:
    """
    Dev
    """
    file_name = f"{file_path}/{input_dict['hostname']}.txt"
    cli_output = input_dict['cli_output'].decode('utf-8')
    with open(file_name, write_mode) as f:
        f.write(cli_output)


def yaml_func(input_file: str, file_mode: str='r'):
    """
    Dev
    """
    with open(input_file, file_mode) as f:
        s = f.read()
    return yaml.safe_load(s)


parser = argparse.ArgumentParser()
parser.add_argument(
    'file', help='fully qualified/absolute path to input Yaml file'
    )
args = parser.parse_args()
argparse_error_msg = \
'\nInvalid File Extension {}. Must be "yaml" or "yml" (case insensitive).'
error_str = '{}{}{}'.format('"', args.file.split('.')[-1], '"')

r_str = r"^(\w|\-|/|\.|\:|\s)+(\w|\-|/|\.|\:|\s)*\.(yaml|yml)$"
r = re.compile(r_str, re.IGNORECASE)


if __name__ == '__main__':
    if r.match(args.file):
        print(f"Input File Path: {args.file}")
    else:
        parser.error(argparse_error_msg.format(error_str))


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

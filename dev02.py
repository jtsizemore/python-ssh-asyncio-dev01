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


# paramiko ssh client
def ssh_connect(input_dict: dict) -> bytes:
    """
    Dev
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        input_dict['hostname'],
        username=input_dict['username'],
        password=input_dict['password']
        )
    # verify:
    #   - 'channel_mode' is string
    #   - 'channel_mode' lower case equals 'exec_command'
    #   - in case 'cli_cmd' list > 0, only take first index of 0
    if isinstance(input_dict['channel_mode'], str) and \
        input_dict['channel_mode'].lower() == 'exec_command':
        # change this print statment to logging
        print("exec mode")
        stdin, stdout, stderr = \
            ssh_client.exec_command(input_dict['cli_cmd'][0])
        time.sleep(5)
        ssh_client.close()
        ssh_output_bytes = stdout.read()
        h = input_dict['hostname'].replace('.', '_')
        d = {'hostname': h, 'cli_output': ssh_output_bytes}
        return d
    # verify:
    #   - 'channel_mode' is string
    #   - 'channel_mode' lower case equals 'invoke_shell'
    elif isinstance(input_dict['channel_mode'], str) and \
        input_dict['channel_mode'].lower() == 'invoke_shell':
        # change this print statment to logging
        print("invoke shell")
        rx_bytes_list = []
        paramiko_ssh_channel = ssh_client.invoke_shell()
        if paramiko_ssh_channel.send_ready():
            paramiko_ssh_channel.send('\nterminal length 0\n')
            time.sleep(1)
            for cmd in input_dict['cli_cmd']:
                send_str = f'{str(cmd)}\n'
                paramiko_ssh_channel.send(send_str)
                time.sleep(1)
                if paramiko_ssh_channel.recv_ready():
                    while paramiko_ssh_channel.recv_ready():
                        rx_bytes = paramiko_ssh_channel.recv(2048e6)
                        rx_bytes_list.append(rx_bytes)
                    time.sleep(5)
            h = input_dict['hostname'].replace('.', '_')
            d = {'hostname': h, 'cli_output': rx_bytes_list}
        return d


# write file from input dict
def write_file(
    input_dict: dict, file_path: str='no_git_tmp', write_mode: str='w'
    ) -> None:
    """
    Dev
    """
    file_name = f"{file_path}/{input_dict['hostname']}.txt"
    if isinstance(input_dict['cli_output'], bytes):
        # change this print statment to logging
        print("bytes")
        cli_output = input_dict['cli_output'].decode('utf-8')
        with open(file_name, write_mode) as f:
            f.write(cli_output)
    elif isinstance(input_dict['cli_output'], list):
        # change this print statment to logging
        print("list")
        cli_output_list = [
            i.decode('utf-8') for i in input_dict['cli_output']
            ]
        with open(file_name, write_mode) as f:
            f.writelines(cli_output_list)


# read yaml and convert to python obj
def yaml_func(input_file: str, file_mode: str='r'):
    """
    Dev
    """
    with open(input_file, file_mode) as f:
        s = f.read()
    return yaml.safe_load(s)


# argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    'file', help='fully qualified/absolute path to input Yaml file'
    )
args = parser.parse_args()
argparse_error_msg = \
    '\nInvalid File Extension {}. Must be "yaml" or "yml" (case insensitive).'
error_str = '{}{}{}'.format('"', args.file.split('.')[-1], '"')

# regex for argparse
r_str = r"^(\w|\-|/|\.|\:|\s)+(\w|\-|/|\.|\:|\s)*\.(yaml|yml)$"
r = re.compile(r_str, re.IGNORECASE)


# run
if __name__ == '__main__':
    if r.match(args.file):
        print(f"Input File Path: {args.file}")
    else:
        parser.error(argparse_error_msg.format(error_str))


    t_start1 = time.time()

    l = yaml_func(args.file)

    with concurrent.futures.ThreadPoolExecutor() as p:
        r = p.map(ssh_connect, l)
    
    print(time.time() - t_start1)
    t_start2 = time.time()

    with concurrent.futures.ThreadPoolExecutor() as p:
        p.map(write_file, r)
    
    print(time.time() - t_start2)
    print(time.time() - t_start1)

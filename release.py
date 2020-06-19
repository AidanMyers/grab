import argparse
import getpass
import subprocess
import torch

def release(node):
    pids = list(filter(None, subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid', '--id=' + str(node), '--format=csv,noheader']).decode('utf-8').split('\n')))
    
    for p in pids:
        if p in subprocess.check_output(['pgrep', '-u', str(getpass.getuser())]).decode('utf-8').split('\n'):
            subprocess.call(['kill', '-9', str(p)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('node', metavar='n', type=int, nargs='+', choices=range(torch.cuda.device_count()), help='node to be released')
    args = parser.parse_args()

    for n in args.node:
        release(n)

if __name__ == "__main__":
    main()
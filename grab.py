import argparse
import os
import subprocess
import sys
import torch

def necromancy():
    if os.fork():
        sys.exit()

def grab(node, reserved):
    #determine if node is available
    
    mem = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.free', '--id=' + str(node), '--format=csv,nounits,noheader']).decode('utf-8')
    x = torch.rand((256,1024,int(int(mem)*(reserved/100)))).cuda(node)

def main():
    necromancy()

    parser = argparse.ArgumentParser()
    parser.add_argument('node', metavar='n', type=int, nargs='+', choices=range(torch.cuda.device_count()), help='node to be grabbed')
    parser.add_argument('-r', '--reserved', type=int, choices=range(101), default=50, help='percentage of total memory to reserve')
    parser.add_argument('-t', '--time', type=int, help='number of minutes to hold the node')
    args = parser.parse_args()

    for n in args.node:
        grab(n, args.reserved)

    if(args.time):
        sleep(args.time*60)
        sys.exit()

    while(True):
        pass

if __name__ == "__main__":
    main()
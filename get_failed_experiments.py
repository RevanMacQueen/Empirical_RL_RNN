import glob, os
from pathlib import Path
from utils.utils import to_command
import json

root = Path('results_tau_1')

failed = []

total =0

for dir in root.iterdir():    

    done = False
    for File in os.listdir(dir):   
        
        if '.npy' in File:
            done = True


    if done == False:
        params_file = dir/'params.json'               
        params = json.load(open(params_file))

        failed.append(to_command(params))
    total += 1

with open("failed_experiments.txt", 'w+') as f:
    for l in failed:
        f.write(l)


print(total- len(failed))
print(total)
        
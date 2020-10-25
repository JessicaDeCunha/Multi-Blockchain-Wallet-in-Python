import subprocess
import json
import os

command = './derive -g --mnemonic="more silent beauty club calm again taste staff check poverty sport usual" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)

from constants import *

mnemonic = os.getenv('MNEMONIC', 'barrel gasp approve wire torch erode climb green undo adjust weasel black people pony sea')
import time
import subprocess

try:
    with open('last_updated','r') as last_updated:
        last_update = last_updated.readline()
        print(f'Last Run on: {last_update}')
except FileNotFoundError:
    pass

while True:
    subprocess.call(
        ["python.exe", "store.py"])

    time.sleep(900)

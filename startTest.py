import subprocess

def run_python_script(device, result_file):
    command = ['python', 'C:/Users/sofie/OneDrive/Documenten/unif/2022-2023/masterproef/morpheus/Main.py', device, result_file]
    subprocess.Popen(command)

# Call the function to start the Python script in a separate process
import sys
print("start")
device = sys.argv[1]
fileName = sys.argv[2]
print(device,fileName)
run_python_script(device, fileName)

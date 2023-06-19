import subprocess
import os

if __name__ == "__main__":
    # Command to be executed in the new terminal
    current_directory = os.getcwd()
    command = "cd " + current_directory
    # command = "python3 my_script.py"
    
    # Launch a new terminal window and execute the command
    subprocess.call(['osascript', '-e', 'tell app "Terminal" to do script "{}"'.format(command)])

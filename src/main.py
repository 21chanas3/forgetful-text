import importlib
import models
import os
from os import listdir
from os.path import isfile, join
import shlex

COMMAND_PATH = "./commands"  # path to the commands directory

# Create database interface
models.initialize()

# Dynamically load commands
command_files = [f for f in listdir(COMMAND_PATH) if isfile(join(COMMAND_PATH, f)) and f.split(".")[1] == "py"]
commands = {}
for file in command_files:
    name = os.path.basename(file).split(".")[0]
    module = importlib.import_module("commands." + name)
    commands.update({name: module})

os.system('title Forgetful')
print("Welcome to Forgetful")

while True:
    text = input("> ")  # Get the user's input
    text = shlex.split(text)  # Split the input into a list of arguments
    if text[0] == "exit":
        break
    elif text[0] in commands:
        module = commands.get(text[0])
        text.pop(0)  # Remove the command from the list of arguments
        module.run(text)  # Run the command with the remaining arguments
    else:
        print("No such command! Use 'help' to view all commands or 'exit' to exit the program")

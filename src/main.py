import importlib
import models
import os
from os import listdir
from os.path import isfile, join

COMMAND_PATH = "./commands"

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
    text = input("> ").split(" ")
    if text[0] == "exit":
        break
    elif text[0] in commands:
        module = commands.get(text[0])
        text.pop(0)
        module.run(text)
    else:
        print("No such command! Use 'help' to view all commands or 'exit' to exit the program")

import database as db
import argparse
import os

os.system('title Forgetful')
db.create_tables()
print("Welcome to Forgetful")

while True:
    text = input("> ")
    if text == "exit":
        break
    else:
        argparse.parser(text)




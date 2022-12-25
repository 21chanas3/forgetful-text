def run(args):
    if len(args) == 0:
        print("general help subdialog")
    elif args[0] == "task":
        print("task help subdialog")
    elif args[0] == "view":
        print("view help subdialog")
    else:
        print("No such sub-command found!")


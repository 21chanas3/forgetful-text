from models import Task


flags = ["-desc", "-due", "-do", "-p", "-s", "-t"]


def run(args):
    if len(args) == 0:
        print("No subcommand provided")
    elif args[0] == "add":
        task = Task.create(title=args[1])
    elif args[0] == "delete":
        pass
    elif args[0] == "edit":
        pass
    elif args[0] == "complete":
        pass
    else:
        print("Invalid subcommand")

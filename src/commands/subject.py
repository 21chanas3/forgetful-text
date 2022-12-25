from models import Subject
import re


def run(args):
    if len(args) == 0:
        print("No subcommand provided")
    elif args[0] == "add":
        if len(args) < 1:
            print("Please specify a name for the subject");
            return
        elif len(args) < 2:
            sub_name = str(args[1])
            subject = Subject.get_or_none(name=sub_name)
            if subject is not None:
                print("Subject already exist within database")
                return
            sub = Subject(title=sub_name, color="FFFFFF")
            sub.save()
            print("Subject " + str(sub.id) + " added: " + args[1])
        elif len(args) < 3:
            sub_name = str(args[1])
            sub_id = str(args[2])
            subject = Subject.get_or_none(name=sub_name)
            if subject is not None:
                print("Subject already exist within database")
                return
            valid_colour = re.match("^([A-Fa-f0-9]{6})$", sub_id)
            if not valid_colour:
                print("Invalid colour")
                return
            sub = Subject(title=sub_name, color=sub_id)
            sub.save()
            print("Subject " + str(sub.id) + " added: " + args[1] + " " + args[2])
        else:
            print("Too many arguments")
            return

    elif args[0] == "remove":
        # takes name or ID
        pass
    elif args[0] == "edit":
        pass
    elif args[0] == "list":
        pass # use prettytable
    else:
        print("Invalid subcommand")


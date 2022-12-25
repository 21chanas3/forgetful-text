from models import Subject
from prettytable import PrettyTable
import re


def run(args):
    table = PrettyTable()
    if len(args) == 0:
        print("No subcommand provided")

    elif args[0] == "add":
        if len(args) < 1:
            print("Too few arguments")
            return
        elif len(args) < 2:
            print("Please specify a name for the subject");
            return
        elif len(args) < 3:
            sub_name = str(args[1])
            subject = Subject.get_or_none(title=sub_name)
            if subject is not None:
                print("Subject already exist within database")
                return
            sub = Subject(title=sub_name, color="FFFFFF")
            sub.save()
            print("Subject " + str(sub.id) + " added: " + args[1])
        elif len(args) < 4:
            sub_name = str(args[1])
            sub_id = str(args[2])
            subject = Subject.get_or_none(title=sub_name)
            sub_color = str(args[2])
            subject = Subject.get_or_none(title=sub_name)
            if subject is not None:
                print("Subject already exist within database")
                return
            valid_colour = re.match("^([A-Fa-f0-9]{6})$", sub_color)
            if not valid_colour:
                print("Invalid colour")
                return
            sub = Subject(title=sub_name, color=sub_color)
            sub.save()
            print("Subject " + str(sub.id) + " added: " + args[1] + " " + args[2])
        else:
            print("Too many arguments")
            return

    elif args[0] == "remove":
        if len(args) == 1:
            print("Too few arguments")
            return
        elif len(args) < 3:
            if args[1].isnumeric():
                sub_name = str(args[1])
                sub = Subject.get_or_none(title=sub_name)
                if sub is None:
                    sub_id = int(args[1])
                    sub = Subject.get_or_none(id=sub_id)
                    if sub is None:
                        print("No such subject is named " + str(sub_id))
                        return
                    query = Subject.delete().where(Subject.id == sub_id)
                    query.execute()
                    return
                query = Subject.delete().where(Subject.title == sub_name)
                query.execute()
        else:
            print("Too many arguments")
            return

    elif args[0] == "edit":
        if len(args) < 3:
            print("Too few arguments")
            return
        elif len(args) < 4:
            if args[1].isnumeric():
                sub_id = int(args[1])
                sub = Subject.get_or_none(id=sub_id)
                if sub is None:
                    print("No such ID is founded " + str(sub_id))
                    return
                valid_colour = re.match("^([A-Fa-f0-9]{6})$", args[2])
                if not valid_colour:
                    query = Subject.update(title=args[2]).where(Subject.id == sub_id)
                    query.execute()
                query = Subject.update(color=args[2]).where(Subject.id == sub_id)
                query.execute()
            else:
                print("Insert a valid ID")
                return
        else:
            print("Too many arguments")
            return

    elif args[0] == "list":
        table.field_names = ["ID", "Name", "Color"]
        for subs in Subject.select():
            table.add_row([subs, subs.title, subs.color])
        print(table)
    else:
        print("Invalid subcommand")


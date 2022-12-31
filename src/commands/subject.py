from models import Subject, Task
from prettytable import PrettyTable
import re


# run subject command
def run(args):
    """
    :param args:
    :return:
    """
    table = PrettyTable()  # create a new table for prettytable

    if len(args) < 1:
        print("Please input an argument for subjects")
        return

    match args[0]:
        case 'add':
            if len(args) < 2:
                print("Please specify a name for the subject")
                return
            elif len(args) < 3:  # no color specified
                sub_name = str(args[1])
                subject = Subject.get_or_none(title=sub_name)  # check if subject already exist
                if subject is not None:
                    print("Subject already exist within database")
                    return
                sub = Subject(title=sub_name, color="FFFFFF")
                sub.save()  # save subject to database
                print("Subject " + str(sub.id) + " added: " + args[1])
            elif len(args) < 4:
                sub_name = str(args[1])
                sub_color = str(args[2])
                subject = Subject.get_or_none(title=sub_name)  # check if subject already exist
                if subject is not None:
                    print("Subject already exist within database")
                    return
                valid_colour = re.match("^([A-Fa-f0-9]{6})$", sub_color)  # check color hex code is valid
                if not valid_colour:
                    print("Invalid colour")
                    return
                sub = Subject(title=sub_name, color=sub_color)
                sub.save()  # save subject to database
                print("Subject " + str(sub.id) + " added: " + args[1] + " " + args[2])
            else:
                print("Too many arguments")
                return
        case 'remove':
            if len(args) < 3:
                if args[1].isnumeric():  # delete by ID
                    sub_name = str(args[1])
                    sub = Subject.get_or_none(title=sub_name)
                    if sub is None:  # delete by name
                        sub_id = int(args[1])
                        sub = Subject.get_or_none(id=sub_id)  # check if subject exist
                        if sub is None:  # subject does not exist
                            print("No such subject is named " + str(sub_id))
                            return
                        query = Subject.delete().where(Subject.id == sub_id)  # query to delete subject
                        query.execute()  # executes the query
                        return
                    query = Subject.delete().where(Subject.title == sub_name)  # query to delete subject
                    query.execute()  # executes the query
            else:
                print("Too many arguments")
                return
        case 'edit':
            if len(args) < 3:
                print("Too few arguments")
                return
            elif len(args) < 4:
                if args[1].isnumeric():  # edit by ID
                    sub_id = int(args[1])
                    sub = Subject.get_or_none(id=sub_id)  # check if subject exist
                    if sub is None:
                        print("No such ID is founded " + str(sub_id))
                        return
                    valid_colour = re.match("^([A-Fa-f0-9]{6})$", args[2])  # check if second arg is a color
                    if not valid_colour:
                        query = Subject.update(title=args[2]).where(Subject.id == sub_id)  # update subject name
                        query.execute()
                    query = Subject.update(color=args[2]).where(Subject.id == sub_id)  # update subject color
                    query.execute()
                else:
                    print("Insert a valid ID")
                    return
            else:
                print("Too many arguments")
                return
        case "list":
            table.field_names = ["ID", "Name", "Color"]
            for subs in Subject.select():
                table.add_row([subs, subs.title, subs.color])
            print(table)  # print table
        case "view":
            if len(args) > 2:
                print("Too many arguments")
                return
            elif len(args) < 1:
                print("Too few arguments")
                return
            sub_name = str(args[1])
            subject = Subject.get_or_none(title=sub_name)  # check if subject exist
            if subject is None:
                print("Subject does not exist within database")
                return
            subject = Subject.get(Subject.title == sub_name)
            print(subject.title)
            table.field_names = ["ID", "Complete", "Due Date", "Task Name", "Priority", "Do Date"]
            for task in Task.select().where(Task.subject_id == subject.title):  # add row for specified subject id
                table.add_row([task, task.complete, task.due_date, task.title, task.priority, task.do_date])
            print(table)
        case 'help':
            print('Usage: task [subcommand] <options>\n'
                  '\n'
                  'Subcommands:\n'
                  '\n'
                  '  add [title] <options>       Add a new task\n'
                  '  delete [task ID]            Delete a task by ID\n'
                  '  edit [task ID] <options>    Edit a task by ID\n'
                  '  complete [task ID]          Mark a task as complete or incomplete\n'
                  '  help                        Display this help message\n'
                  '\n')
        case _:
            print("Invalid subcommand")
            return

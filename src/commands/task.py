from models import Task
from datetime import datetime

flags = ["-n", "-d", "-due", "-do", "-p", "-s"]


def run(args):
    if len(args) == 0:
        print("No subcommand provided")
    elif args[0] == "add":
        task = Task(title=args[1])
        task = _parse_flags(task, args[2:])
        if task is not None:
            task.save()
            print("Task " + str(task.id) + " added: " + args[1])

    elif args[0] == "delete":
        if len(args) < 2 or not args[1].isnumeric():
            print("Please specify a numeric task ID")
            return
        task_id = int(args[1])
        task = Task.get_or_none(id=task_id)
        if task is None:
            print("No such task with ID " + str(task_id))
        else:
            task.delete_instance()
            print("Task " + args[1] + " deleted!")

    elif args[0] == "edit":
        if len(args) < 2 or not args[1].isnumeric():
            print("Please specify a numeric task ID")
            return
        task_id = int(args[1])
        task = Task.get_or_none(id=task_id)
        if task is None:
            print("No such task with ID " + str(task_id))
            return
        task = _parse_flags(task, args[2:])
        if task is not None:
            task.save()
            print("Task " + str(task.id) + " edited!")

    elif args[0] == "complete":
        if len(args) < 2 or not args[1].isnumeric():
            print("Please specify a numeric task ID")
            return
        task_id = int(args[1])
        task = Task.get_or_none(id=task_id)
        if task is None:
            print("No such task with ID " + str(task_id))
            return
        elif not task.complete:
            task.complete = True
            print("Task " + args[1] + " marked as complete!")
        elif task.complete:
            task.complete = False
            print("Task " + args[1] + " marked as incomplete!")
        task.save()
    else:
        print("Invalid subcommand")


def _parse_flags(task, args):
    current_flag = ""
    for arg in args:
        if current_flag == "" and arg in flags:
            current_flag = arg
        elif not current_flag == "":
            task = _set_field(task, current_flag, arg)
            current_flag = ""
        else:
            print("Unexpected argument!")
            return None
    return task


def _set_field(task, field, value):
    if field == "-n":
        task.title = value
    elif field == "-d":
        task.description = value
    elif field == "-due":
        res = _parse_date(value)
        task.due_date = res[0]
        task.due_time = res[1]
    elif field == "-do":
        res = _parse_date(value)
        task.do_date = res[0]
        task.do_time = res[1]
    elif field == "-p":
        task.priority = value
    elif field == "-s":
        task.subject = value
    return task


def _parse_date(value):
    values = value.split(" ")
    if len(values) == 2:
        return datetime.strptime(value, '%y/%m/%d %H:%M'), True
    elif len(values) == 1:
        return datetime.strptime(value, '%y/%m/%d'), False
    else:
        print("Invalid date!")
        return None

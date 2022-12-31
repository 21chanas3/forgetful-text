from models import Task
from prettytable import PrettyTable
from datetime import datetime, timedelta


def run(args):
    """
    :param args:
    :return:
    """

    # checks valid number of args
    if len(args) < 1:
        print("Too few arguments")
        return

    if len(args) > 1:
        print("Too many arguments")
        return

    table = PrettyTable()

    # Check the subcommand and update the table
    match args[0]:
        case 'duedate':
            table.field_names = ["ID", "Complete", "Due Date", "Task Name", "Priority", "Do Date"]
            for task in Task.select().order_by(Task.due_date):
                table.add_row([task, task.complete, task.due_date, task.title, task.priority, task.do_date])
            print(table)
        case 'dodate':
            table.field_names = ["ID", "Complete", "Do Date", "Task Name", "Priority", "Due Date"]
            for task in Task.select().order_by(Task.do_date):
                table.add_row([task, task.complete, task.do_date, task.title, task.priority, task.due_date])
            print(table)
        case 'priority':
            table.field_names = ["ID", "Complete", "Do Date", "Task Name", "Priority", "Due Date"]
            for task in Task.select().order_by(Task.priority):
                table.add_row([task, task.complete, task.do_date, task.title, task.priority, task.due_date])
            print(table)
        case 'today':
            table.field_names = ["ID", "Complete", "Do Date", "Task Name", "Priority", "Due Date"]
            for task in Task.select(). \
                    where((Task.do_date >= datetime.today().date()) &
                          (Task.do_date < datetime.today().date() + timedelta(days=1))). \
                    order_by(Task.do_date):
                table.add_row([task, task.complete, task.do_date, task.title, task.priority, task.due_date])
            print(table)
        case _:  # subcommand is not recognized
            print("There is no such subcommand for view")

from models import Task
from prettytable import PrettyTable
from datetime import datetime, timedelta
from peewee import fn


def run(args):
    table = PrettyTable()
    if args[0] == "duedate":
        table.field_names = ["ID", "Due Date", "Task Name", "Priority", "Do Date"]
        for task in Task.select().order_by(Task.due_date):
            table.add_row([task, task.due_date, task.title, task.priority, task.do_date])
        print(table)
    elif args[0] == "dodate":
        table.field_names = ["ID", "Do Date", "Task Name", "Priority", "Due Date"]
        for task in Task.select().order_by(Task.do_date):
            table.add_row([task, task.do_date, task.title, task.priority, task.due_date])
        print(table)
    elif args[0] == "priority":
        table.field_names = ["ID", "Do Date", "Task Name", "Priority", "Due Date"]
        for task in Task.select().order_by(Task.priority):
            table.add_row([task, task.do_date, task.title, task.priority, task.due_date])
        print(table)
    elif args[0] == "today":
        table.field_names = ["ID", "Do Date", "Task Name", "Priority", "Due Date"]
        for task in Task.select().\
                where((Task.do_date >= datetime.today().date()) &
                      (Task.do_date < datetime.today().date() + timedelta(days=1))).\
                order_by(Task.do_date):
            table.add_row([task, task.do_date, task.title, task.priority, task.due_date])
        print(table)

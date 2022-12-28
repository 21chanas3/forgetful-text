from models import Task
from datetime import datetime

flags = ['-n', '-d', '-due', '-do', '-p', '-s']


def run(args):
    if len(args) == 0:
        print('No subcommand provided')
        return
    match args[0]:
        case 'add':
            task = Task(title=args[1])
            task = _parse_flags(task, args[2:])
            if task is not None:
                task.save()
                print('Task ' + str(task.id) + ' added: ' + args[1])
        case 'delete':
            if len(args) < 2 or not args[1].isnumeric():
                print('Please specify a numeric task ID')
                return
            task_id = int(args[1])
            task = Task.get_or_none(id=task_id)
            if task is None:
                print('No such task with ID ' + str(task_id))
            else:
                task.delete_instance()
                print('Task ' + args[1] + ' deleted!')

        case 'edit':
            if len(args) < 2 or not args[1].isnumeric():
                print('Please specify a numeric task ID')
                return
            task_id = int(args[1])
            task = Task.get_or_none(id=task_id)
            if task is None:
                print('No such task with ID ' + str(task_id))
                return
            task = _parse_flags(task, args[2:])
            if task is not None:
                task.save()
                print('Task ' + str(task.id) + ' edited!')
        case 'complete':
            if len(args) < 2 or not args[1].isnumeric():
                print('Please specify a numeric task ID')
                return
            task_id = int(args[1])
            task = Task.get_or_none(id=task_id)
            if task is None:
                print('No such task with ID ' + str(task_id))
                return
            elif not task.complete:
                task.complete = True
                print('Task ' + args[1] + ' marked as complete!')
            elif task.complete:
                task.complete = False
                print('Task ' + args[1] + ' marked as incomplete!')
            task.save()
        case _:
            print('Invalid subcommand')


def _parse_flags(task, args):
    current_flag = ''
    for arg in args:
        if current_flag == '' and arg in flags:
            current_flag = arg
        elif not current_flag == '':
            task = _set_field(task, current_flag, arg)
            current_flag = ''
        else:
            print('Unexpected argument!')
            return None
    return task


def _set_field(task, field, value):
    match field:
        case "-n":
            task.title = value
        case '-d':
            task.description = value
        case '-due':
            res = _parse_date(value)
            task.due_date = res[0]
            task.due_time = res[1]
        case '-do':
            res = _parse_date(value)
            task.do_date = res[0]
            task.do_time = res[1]
        case '-p':
            task.priority = value
        case '-s':
            task.subject = value
        case _:
            return None
    return task


def _parse_date(value):
    values = value.split(' ')
    if len(values) == 2:
        return datetime.strptime(value, '%y/%m/%d %H:%M'), True
    elif len(values) == 1:
        return datetime.strptime(value, '%y/%m/%d'), False
    else:
        print('Invalid date!')
        return None

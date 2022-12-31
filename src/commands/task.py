from models import Task
from datetime import datetime

flags = ['-n', '-d', '-due', '-do', '-p', '-s']  # flags for commands


# runs command
def run(args):
    """
    :param args:
    :return:
    """
    if len(args) == 0:  # no arguments passed
        print('No subcommand provided')
        return

    match args[0]:
        case 'add':  # add task
            task = Task(title=args[1])
            task = _parse_flags(task, args[2:])  # parse flags for task
            if task is not None:
                task.save()  # save task to database
                print('Task ' + str(task.id) + ' added: ' + args[1])
        case 'delete':  # delete task
            if len(args) < 2 or not args[1].isnumeric():
                print('Please specify a numeric task ID')
                return
            task_id = int(args[1])
            task = Task.get_or_none(id=task_id)  # check if task exist by ID
            if task is None:  # task do not exist
                print('No such task with ID ' + str(task_id))
            else:
                task.delete_instance()  # delete task
                print('Task ' + args[1] + ' deleted!')
        case 'edit':  # edit task
            if len(args) < 2 or not args[1].isnumeric():
                print('Please specify a numeric task ID')
                return
            task_id = int(args[1])
            task = Task.get_or_none(id=task_id)  # check if task exist by ID
            if task is None:  # task do not exist
                print('No such task with ID ' + str(task_id))
                return
            task = _parse_flags(task, args[2:])  # parse flags
            if task is not None:
                task.save()  # save changes to task
                print('Task ' + str(task.id) + ' edited!')
        case 'complete':
            if len(args) < 2 or not args[1].isnumeric():
                print('Please specify a numeric task ID')
                return
            task_id = int(args[1])
            task = Task.get_or_none(id=task_id)  # check if task exist by ID
            if task is None:  # task do not exist
                print('No such task with ID ' + str(task_id))
                return
            elif not task.complete:
                task.complete = True
                print('Task ' + args[1] + ' marked as complete!')
            elif task.complete:
                task.complete = False
                print('Task ' + args[1] + ' marked as incomplete!')
            task.save()
        case 'help':
            print('Usage: task [subcommand] [options]\n'
                  '\n'
                  'Subcommands:\n'
                  '\n'
                  '  add [title] <options>       Add a new task\n'
                  '  delete [task ID]            Delete a task by ID\n'
                  '  edit [task ID] <options>    Edit a task by ID\n'
                  '  complete [task ID]          Mark a task as complete or incomplete\n'
                  '  help                        Display this help message\n'
                  '\n'
                  'Options:\n'
                  '\n'
                  '  -n [title]                  Set the title of the task\n'
                  '  -d [description]            Set the description of the task\n'
                  '  -due <YYYY/MM/DD HH:mm>     Set the due date and time of the task\n'
                  '  -do <YYYY/MM/DD HH:mm>      Set the start date and time of the task\n'
                  '  -p [priority]               Set the priority of the task (low, medium, or high)\n'
                  '  -s [subject]                Set the subject of the task\n')
        case _:
            print('Invalid subcommand')


# parses flags
def _parse_flags(task, args):
    current_flag = ''
    for arg in args:  # iterate over the elements in args
        if current_flag == '' and arg in flags:
            current_flag = arg
        elif not current_flag == '':
            task = _set_field(task, current_flag, arg)
            current_flag = ''
        else:
            print('Unexpected argument!')
            return None
    return task


# set values of field
def _set_field(task, field, value):
    # set the appropriate field in task based on the value of field
    match field:
        case "-n":
            task.title = value
        case '-d':
            task.description = value
        case '-due':
            res = _parse_date(value)  # parse date
            task.due_date = res[0]
            task.due_time = res[1]
        case '-do':
            res = _parse_date(value)  # parse date
            task.do_date = res[0]
            task.do_time = res[1]
        case '-p':
            task.priority = value
        case '-s':
            task.subject_id = value
        case _:
            return None
    return task


# parses date and time
def _parse_date(value):
    values = value.split(' ')  # split the date and time into a list

    if len(values) == 2:  # parse the date and time and return a tuple
        return datetime.strptime(value, '%y/%m/%d %H:%M'), True
    elif len(values) == 1:  # parse the date and return a tuple
        return datetime.strptime(value, '%y/%m/%d'), False
    else:
        print('Invalid date!')
        return None

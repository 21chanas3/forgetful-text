num_cmd = ["task", "view"]
task_cmd = ["add", "delete", "edit"]
tag_cmd = ["add", "delete", "list"]
add_task_cmd = ["duedate", "dodate", "priority", "tag", "class"]
view_cmd = ["duedate", "dodate", "priority", "all"]


# main parser function
def parser(txt):
    cmd = txt.split()  # splits text into list by space
    len_cmd = len(cmd) # length of command
    if not cmd[0] not in task_cmd:  # checks valid command
        return "invalid command"

    if cmd[0] == num_cmd[0]:  # task command
        task(cmd[1:], len_cmd)
    elif cmd[0] == num_cmd[1]:  # view command
        view(cmd[1:], len_cmd)


def task(cmd, len_cmd):
    if cmd[1] not in task_cmd:  # check task command
        return "invalid task command"

    if len_cmd - 1:
        if cmd[1] == task_cmd[0]:
            pass  # add task name
        elif cmd[1] == task_cmd[1]:
            pass  # delete task
        else:
            pass  # edit task name
    else:
        print("Please specify task command.\n")
        print("\t" + " ".join(task_cmd) + "\n")


def view(cmd, len_cmd):
    if cmd[1] not in view_cmd:  # check view command
        return "invalid view command"

    if len_cmd - 1:
        if cmd[1] == view_cmd[0]:
            pass  # return due date
        elif cmd[1] == view_cmd[1]:
            pass  # return do date
        elif cmd[1] == view_cmd[2]:
            pass  # return priority
        else:
            pass  # return all
    else:
        print("Please specify view command.\n")
        print("\t" + " ".join(view_cmd) + "\n")



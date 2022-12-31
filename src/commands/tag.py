import peewee
from models import Tag, Task, TaskTag
from prettytable import PrettyTable
import re


# run tag command
def run(args):
    """
    :param args:
    :return:
    """
    table = PrettyTable()  # create a new table for prettytable

    if len(args) < 1:
        print("Please input an argument for tags")
        return

    match args[0]:
        case 'add':
            if len(args) > 3:
                print("Too many arguments")
                return
            tag_name = str(args[1])
            tag = Tag.get_or_none(title=tag_name)  # check if tag exist
            if tag is not None:
                print("Tag already exist within database")
                return
            if len(args) == 3:
                tag_color = str(args[2])
                valid_colour = re.match("^([A-Fa-f0-9]{6})$", tag_color)  # check if color hex code is valid
                if not valid_colour:
                    print("Invalid colour")
                    return
                tag = Tag(title=tag_name, color=tag_color)
            else:
                tag = Tag(title=tag_name, color="FFFFFF")
            tag.save()
            print("Tag " + str(tag.title) + " added")
        case 'remove':
            if len(args) > 2:
                print("Too many arguments")
            tag_name = str(args[1])
            tag = Tag.get_or_none(title=tag_name)  # check if tag exist
            if tag is None:
                print("No tag is named " + str(tag_name))
                return
            task_tags = TaskTag.select().where(TaskTag.tag_id == tag)  # select the list of the tag ID
            if task_tags is not None:
                for task_tags, task in enumerate(task_tags):
                    task.delete_instance()  # deletes tag
            print("Tag " + args[1] + " deleted! ")
        case 'edit':
            if len(args) > 6:
                print("Too many arguments")
                return
            tag_old_name = args[1]
            _parser_edit(args[2:], tag_old_name)
        case 'assign':
            if not _check_tag(args):
                return
            task, tag = _check_tag(args)
            new_tag_name = TaskTag(task_id=task, tag_id=tag)
            new_tag_name.save()  # save changes to tag
            print("Tag: " + str(tag.title) + " is assigned to " + str(task.title))
        case 'unassign':
            if not _check_tag(args):
                return
            task, tag = _check_tag(args)
            query = TaskTag.delete().where((TaskTag.task_id == task.id) & (TaskTag.tag_id == tag.id))
            query.execute() # save changes to tag
            print("Tag: " + str(tag.title) + " is unassigned from " + str(task.title))
        case 'view':
            table.field_names = ["ID", "Name", "Color"]
            for tags in Tag.select():
                table.add_row([tags, tags.title, tags.color])
            print(table)
        case _:
            print("Invalid Subcommand")


# checks tag for assign/unassign functionality
def _check_tag(args):
    if len(args) > 3:
        print("Too many arguments")
        return None

    tag_name, task_id = str(args[1]), str(args[2])
    task = Task.get_or_none(id=task_id)  # check if task exist

    if task is None:
        print("No such task ID is founded " + str(task_id))
        return None

    try:
        task = Task.get(Task.id == task_id)
        tag = Tag.get(Tag.title == tag_name)
    except peewee.DoesNotExist:
        print("Invalid arguments")
        return None

    # selects list where Task and Tag ID matches
    task_tag = TaskTag.select().where((TaskTag.task_id == task) & (TaskTag.tag_id == tag))

    match args[0]:
        case 'assign':
            if task_tag.exists():
                print("Tag name " + str(tag.title) + " already assigned to " + str(task.title))
                return None
        case 'unassign':
            if not task_tag.exists():
                print("Tag name " + str(tag.title) + " not assigned to " + str(task.title))
                return None

    if tag is None:
        print("Tag ID does not exist")
        return None

    return task, tag


# parser for edit
def _parser_edit(args, tag_name):
    match args[0]:
        case '-name':
            tag_new_name = str(args[1])
            if len(args) > 2:  # there is second flag
                _parser_edit(args[2:], tag_name)
            tag = Tag.get_or_none(title=tag_name)  # check if tag exist
            if tag is None:
                print("No tag is named " + str(tag_name))
                return
            query = Tag.update(title=tag_new_name).where(Tag.title == tag_name)  # update name
            query.execute()
            print("Edits were made to " + str(tag_name))
            return
        case '-color':
            tag_color = str(args[1])
            valid_color = re.match("^([A-Fa-f0-9]{6})$", tag_color)  # check if color hex code is valid
            if not valid_color:
                print("Invalid color: " + tag_color)
                return
            query = Tag.update(color=tag_color).where(Tag.title == tag_name)  # update color
            query.execute()
            if len(args) > 2:  # there is second flag
                _parser_edit(args[2:], tag_name)
            print("Edits were made to " + str(tag_name))
            return
        case _:
            print("Invalid argument: " + str(args[0]))
            return

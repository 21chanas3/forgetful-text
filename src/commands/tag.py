"""
- Add subject view <name>: Prints a table with all tasks assigned to subject
- Add tags add <name> <optional=color>
- Add tags remove <name>
- Add tags edit <old_name> <new_name> <<optional=color>
- Add tags assign <name> <taskid>
- Add tags view
^ Assigns/Unassigns a tag to a task
"""
import peewee
from models import Tag, Task, TaskTag
from prettytable import PrettyTable
import re


def run(args):
    table = PrettyTable()
    if len(args) < 1:
        print("Please input an argument for tags")
        return

    match args[0]:
        case 'add':
            if len(args) > 3:
                print("Too many arguments")
                return
            tag_name = str(args[1])
            tag = Tag.get_or_none(title=tag_name)
            if tag is not None:
                print("Tag already exist within database")
                return
            if len(args) == 3:
                tag_color = str(args[2])
                valid_colour = re.match("^([A-Fa-f0-9]{6})$", tag_color)
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
            tag = Tag.get_or_none(title=tag_name)
            if tag is None:
                print("No tag is named " + str(tag_name))
                return
            tag = Tag.get(Tag.title == args[1])
            task_tags = TaskTag.get(TaskTag.task_id == tag)
            count_task = 0
            for count_task, task in enumerate(task_tags):
                task.delete_instance()
            print("Tag " + str(args[1]) + " deleted! " + str(count_task) + " tasks were unassigned from " + str(args[1]))
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
            new_tag_name.save()
            print("Tag: " + str(tag.title) + " is assigned to " + str(task.title))
        case 'unassign':
            if not _check_tag(args):
                return
            task, tag = _check_tag(args)
            query = TaskTag.delete().where((TaskTag.task_id == task.id) & (TaskTag.tag_id == tag.id))
            query.execute()
            print("Tag: " + str(tag.title) + " is unassigned from " + str(task.title))
        case 'view':
            table.field_names = ["ID", "Name", "Color"]
            for tags in Tag.select():
                table.add_row([tags, tags.title, tags.color])
            print(table)
        case _:
            print("Invalid Subcommand")


def _check_tag(args):
    if len(args) > 3:
        print("Too many arguments")
        return None
    tag_name, task_id = str(args[1]), str(args[2])
    task = Task.get_or_none(id=task_id)
    if task is None:
        print("No such task ID is founded " + str(task_id))
        return None
    try:
        task = Task.get(Task.id == task_id)
        tag = Tag.get(Tag.title == tag_name)
    except peewee.DoesNotExist:
        print("Invalid arguments")
        return None
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


def _parser_edit(args, tag_name):
    match args[0]:
        case '-name':
            tag_new_name = str(args[1])
            if len(args) > 2:
                _parser_edit(args[2:], tag_name)
            tag = Tag.get_or_none(title=tag_name)
            if tag is None:
                print("No tag is named " + str(tag_name))
                return
            query = Tag.update(title=tag_new_name).where(Tag.title == tag_name)
            query.execute()
            print("Edits were made to " + str(tag_name))
            return
        case '-color':
            tag_color = str(args[1])
            query = Tag.update(color=tag_color).where(Tag.title == tag_name)
            query.execute()
            if len(args) > 2:
                _parser_edit(args[2:], tag_name)
            print("Edits were made to " + str(tag_name))
            return
        case _:
            return None

def run(args):
    # display the general help dialog
    if len(args) == 0:
        print("Welcome to the \033[1mforgetful\033[0m help system! Here are the available sub-commands:")
        print("  task - Display help information for the 'task' command")
        print("  subject - Display help information for the 'subject' command")
        print("  tag - Display help information for the 'tag' command")
        print("  view - Display help information for the 'view' command")
        print("\nFor more information on a specific sub-command, enter '[sub-command] help'")
        return
    else:  # display an error message
        print("Too many arguments")
        return

class Task:
    def __init__(self, name, description="", due_date="", due_time="", do_date="", do_time="", priority=4, tags=[], subject=""):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.due_time = due_time
        self.do_date = do_date
        self.do_time = do_time
        self.priority = priority
        self.tags = tags
        self.subject = subject

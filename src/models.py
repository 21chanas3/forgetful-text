from peewee import *

# Create a database connection to a SQLite database
db = SqliteDatabase("database.db")


# Base model class
class BaseModel(Model):
    class Meta:
        database = db


# Define a model for tasks
class Task(BaseModel):
    title = TextField(unique=True)
    description = TextField(null=True)
    complete = BooleanField(default=False)
    due_date = DateTimeField(null=True)
    do_date = DateTimeField(null=True)
    due_time = BooleanField(null=True)
    do_time = BooleanField(null=True)
    priority = IntegerField(default=4)
    subject_id = IntegerField(null=True)


# Define a model for tags
class Tag(BaseModel):
    title = TextField(unique=True)
    color = TextField()


# Define a model for task-tag relationships
class TaskTag(BaseModel):
    task_id = IntegerField()
    tag_id = IntegerField()


# Define a model for subjects
class Subject(BaseModel):
    title = TextField(unique=True)
    color = TextField()


if __name__ == "__main__":
    pass


def initialize():
    db.connect()  # connect to the database
    db.create_tables([Task, Tag, TaskTag, Subject])  # create the tables for the models

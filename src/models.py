from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    title = TextField()
    description = TextField(null=True)
    complete = BooleanField(default=False)
    due_date = DateTimeField(null=True)
    do_date = DateTimeField(null=True)
    due_time = BooleanField(null=True)
    do_time = BooleanField(null=True)
    priority = IntegerField(default=4)
    subject_id = IntegerField(null=True)


class Tag(BaseModel):
    title = TextField()
    color = TextField()


class TaskTag(BaseModel):
    task_id = IntegerField()
    tag_id = IntegerField()


class Subject(BaseModel):
    title = TextField()
    color = TextField()


if __name__ == "__main__":
    pass


def initialize():
    db.connect()
    db.create_tables([Task, Tag, TaskTag, Subject])

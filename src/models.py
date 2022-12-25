from peewee import *

db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        database = db


class Tasks(BaseModel):
    title = TextField()
    description = TextField()
    complete = BooleanField()
    due_date = DateTimeField()
    do_date = DateTimeField()
    due_time = BooleanField()
    do_time = BooleanField()
    priority = IntegerField()
    subject_id = IntegerField()


class Tags(BaseModel):
    title = TextField()
    color = TextField()


class TaskTags(BaseModel):
    task_id = IntegerField()
    tag_id = IntegerField()


class Subjects(BaseModel):
    title = TextField()
    color = TextField()


if __name__ == "__main__":
    pass


def initialize():
    db.connect()
    db.create_tables([Tasks, Tags, TaskTags, Subjects])



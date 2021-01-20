from peewee import *
import os
from playhouse.db_url import connect
import datetime

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))

else:
    DATABASE = PostgresqlDatabase('swalef')


class Posts(Model):
    title = CharField()
    body = CharField()
    topic = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Posts], safe=True)
    print("TABLES Created")
    DATABASE.close()
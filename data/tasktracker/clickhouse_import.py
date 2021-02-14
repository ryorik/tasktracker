from clickhouse_driver import Client
#from .models import User, Step, Action
from datetime import datetime
from datetime import timedelta


print("Hello there")

client = Client('localhost')
client.execute('CREATE DATABASE IF NOT EXISTS `actions`')

client.execute("""CREATE TABLE IF NOT EXISTS `actions`.`events`(
    "time" DateTime('Europe/Moscow'),
    "user_id" UInt32,
    "join_date" Date,
    "registration_date" Date,
    "name" String,
    "email" String,
    "is_guest" UInt8,
    "step_id" UInt16,
    "action_id" UInt8
) ENGINE = Log""")

#actions = Action.objects.all()

#for action in actions:

client.execute(
    """INSERT INTO `actions`.`events` (time, user_id, join_date, registration_date, name, email, is_guest, step_id, action_id)
    VALUES (%(time)s, %(user_id)s, %(join_date)s, %(registration_date)s, %(name)s, %(email)s, %(is_guest)s, %(step_id)s, %(action_id)s)""",
    {
        'time': datetime.now(),
        'user_id': 2,
        'join_date': datetime.now(),
        'registration_date': datetime.now(),
        'name': 2,
        'email': 'asd@adfadf',
        'is_guest': 1,
        'step_id': 1,
        'action_id': 1 
    }
)
    



from clickhouse_driver import Client
from .models import User, Action
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import pika
from django.conf import settings

from celery import shared_task
from celery.schedules import crontab
from dateutil.parser import parse

@shared_task
def addToQueue(id):
    action = Action.objects.get(pk=id)
    user = action.user_id

    message = {
            'time': action.time,
            'user_id': action.user_id.id,
            'join_date': user.join_date,
            'registration_date': user.registration_date,
            'name': user.name,
            'email': user.email,
            'is_guest': user.is_guest,
            'step_id': action.target_id.id,
            'action_id': action.action_id
        }

    print(message)    

    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.APP_RABBITMQ_SERVER))
    channel = connection.channel()
    channel.queue_declare(queue='action_queue')
            
    channel.basic_publish(exchange='',
                      routing_key='action_queue',
                      body=json.dumps(
                          message,
                          sort_keys=True,
                          indent=1,
                         cls=DjangoJSONEncoder)
                      )
                          
@shared_task    
def clickhouse_import():
    actionsFromQueue = receive()    
    if (not actionsFromQueue):
        return

    client = Client(settings.APP_CLICKHOUSE_SERVER)
    client.execute('CREATE DATABASE IF NOT EXISTS `tasktracker`')

    client.execute("""CREATE TABLE IF NOT EXISTS `tasktracker`.`events`(
      "time" DateTime,
      "user_id" UInt32,
      "join_date" DateTime,
      "registration_date" DateTime,
      "name" String,
      "email" String,
      "is_guest" UInt8,
      "step_id" UInt32,
      "action_id" UInt8
    ) ENGINE = Log""")



    print(actionsFromQueue)
    for actionFromQueue in actionsFromQueue:
        action = json.loads(actionFromQueue)
        print(action)

        client.execute(
            """INSERT INTO `tasktracker`.`events` (time, user_id, join_date, registration_date, name, email, is_guest, step_id, action_id)
            VALUES (%(time)s, %(user_id)s, %(join_date)s, %(registration_date)s, %(name)s, %(email)s, %(is_guest)s, %(step_id)s, %(action_id)s)""",
            {
                'time': parse(action['time']),
                'user_id': action['user_id'],
                'join_date': parse(action['join_date']),
                'registration_date': fixLeadingZeros(parse(action['registration_date'])),
                'name': action['name'],
                'email': action['email'],
                'is_guest': int(action['is_guest']),
                'step_id': action['step_id'],
                'action_id': action['action_id']
            }
        )  


def receive():
    parameters = pika.ConnectionParameters(settings.APP_RABBITMQ_SERVER)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    queue = channel.queue_declare(queue='action_queue')
    result = []

    for x in range(queue.method.message_count):        
        method_frame, header_frame, body = channel.basic_get(queue = 'action_queue')        
        if method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
            return result
        else:            
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            result.append(body)

    connection.close()
    return result


def fixLeadingZeros(dt):
    withOutYear = dt.strftime("%d-%m %H:%M:%S")
    year = dt.strftime("%Y").zfill(4)
    return f'{year}-{withOutYear}'

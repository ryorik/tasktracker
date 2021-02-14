import json
import pika
from clickhouse_driver import Client
from dateutil.parser import parse


def receive():
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    queue = channel.queue_declare(queue='action_queue')
    result = []

    for x in range(queue.method.message_count - 1):        
        method_frame, header_frame, body = channel.basic_get(queue = 'action_queue')        
        if method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
            return result
        else:            
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            result.append(body)

    connection.close()
    return result
            

def clickhouse_import():
    actionsFromQueue = receive()    
    if (not actionsFromQueue):
        return

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



    print(actionsFromQueue)
    for actionFromQueue in actionsFromQueue:
        action = json.loads(actionFromQueue)
        print(action)

        client.execute(
            """INSERT INTO `actions`.`events` (time, user_id, join_date, registration_date, name, email, is_guest, step_id, action_id)
            VALUES (%(time)s, %(user_id)s, %(join_date)s, %(registration_date)s, %(name)s, %(email)s, %(is_guest)s, %(step_id)s, %(action_id)s)""",
            {
                'time': parse(action['time']),
                'user_id': action['user_id'],
                'join_date': parse(action['join_date']),
                'registration_date': parse(action['registration_date']),
                'name': action['name'],
                'email': action['email'],
                'is_guest': int(action['is_guest']),
                'step_id': action['step_id'],
                'action_id': action['action_id']
            }
        )        

clickhouse_import()

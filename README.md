Описание:
========================
Приложение на Django для регистрации действий пользователей.

### Как происходит регистрация сообщений:
1. Событие вызывается через REST-api
1. Запись о событии скаладывается в БД(SQLite) и кладется в очередь(RabbitMQ)
2. В менеджере задач (Celery) каждые пять минут (сейчас 30 сек чтобы долго не ждать результата) происходит забор сообщений и импорт их в ClickHouse. В роли брокера сообщений для Celery используется Redis - разворачивается автоматически

### Где посмотреть:
* Django - http://157.90.112.215:8000 admin@admin
* Redash - http://157.90.112.215 dataengineer@dataengineer1
* Rabbit - http://157.90.112.215:15672/ guest@guest



### Как развернуть:
Для удобства просмотра результатов в ClickHouse, система разорачивается вместе с Redash. Все разворчивается в docker, с помощь docker-compose.



При первом разворачивании:
1. Необходимо создать пользователя администратора Django. Для этого надо выполнить команды:
```shell
cd data
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```

2. Необходимо установить Redash. C помощью файла ./setup.sh. После этого система будет автоматически развернута на машине.
```shell
./setup.sh
```

В будущем запуск системы можно осуществить с помощью команды docker-compose up (минуя 2 подготовительных).
```shell
docker-compose up
```

## Доступные приложения:

### Django - 8000 порт
Web-приложение на Django. В нем доступна панель администратора в адресу /admin. Логин и пароль задается при разворчивании. В панели можно просмотреть данные на выполнению задач импорта (Celery) создать пользователей и задачи.
Сами действия (просмотр задачи, попытки решения) можно выполнить на главной странице

### Redash - 80 порт
Для просмотра БД ClickHouse

### Менеджер RabbitMQ - 15672 порт
Для просмотра очереди логов.

## Выполнение тестового задания по частям.
## Часть 0.
Вам необходимо изучить схемы таблиц (Приложение 0), определить типы данных в схеме событий и объяснить свой выбор.

Для моделей Django выбраны минмально подходящие по размеру типы полей БД. Сам выбор типа уже завасит от ORM и используемой БД.

### Схема таблицы "пользователи" (django)	

field|description|possible values|type
| --- | --- | --- | --- |
id|идентификатор пользователя|0, ...|Int
join_date|дата создания пользователя|00-00-0000, ...|DateTime
registration_date|дата регистрации пользователя|00-00-0000, ...|DateTime
name|имя пользователя|', ...|Char(200)
email|эл. почта пользователя|', ...|Char(200)
is_guest|является ли пользователь гостем (registration_date = 00-00-0000)|0, 1|Не создавала(Boolean в Django)

* Поле is_guest избыточно для хранения в БД, так как оно зависит от другого. Оно реализовано только как свойство в модели Django

### Схема таблицы "задачи" (django)

field|description|possible values|type
| --- | --- | --- | --- |
id|идентификатор задачи|0, ...|Int

### Схема таблицы "события" (django)

field|description|possible values|type
| --- | --- | --- | --- |
time|время события|00-00-0000|DateTime
id|порядковый номер события|0, ...|Int
action_id|идентификатор действия|0 - увидеть задачу 1 - сделать сабмит решения (попытаться решить задачу) 2 - решить задачу|Int
target_id|идентификатор объекта над которым совершается действие (step_id)|0, ...|Int
user_id|идентификатор пользователя|0, ...|Int - этого поля не хватает в таблице

* без поля user_id невозвможно однозначно определить пользователя

### Схема таблицы аналитической базы данных (clickhouse)

field|description|possible values|type
| --- | --- | --- | --- |
time|время события|00-00-0000|DateTime - дата-время вставляется в UTC
user_id|идентификатор пользователя|0, ...|UInt32
join_date|дата создания пользователя|00-00-0000, ...|DateTime - дата-время вставляется в UTC
registration_date|дата регистрации пользователя|00-00-0000, ...|DateTime - дата-время вставляется в UTC 
name|имя пользователя|', ...|String в CH строки произвольной длины|
email|эл. почта пользователя|', |String в CH строки произвольной длины|
is_guest|является ли пользователь гостем (registration_date = 00-00-0000)|0, 1|UInt8 - тип данных для хранения Boolean в ClickHouse
step_id|идентификатор задачи|0, ...|UInt32
action_id|идентификатор действия|0 - увидеть задачу 1 - сделать сабмит решения (попытаться решить задачу) 2 - решить задачу| UInt8 - Действий довольно ошраниченное количество

* Здесь же поле is_guest необходимо хранить как настоящее поле так как логика его формирования может измениться, а это аналитическая БД.

## Часть 1.
> Сделать прототип с помощью Django, в котором будут регистрироваться события взаимодействия объектов-пользователей с объектами задачами.

Создан и предоствалена инструкция по развертываню. Уже готовый вы можете посмотреть по адресу 

## Часть 2.
> Развернуть clickhouse и подключить его к вашему серверу. Написать код, который собирает данные и отправляет их в БД clickhouse раз в 5 минут. 

Развернут и предоствалена инструкция по развертываню. Уже готовый вы можете посмотреть по адресу 
## Часть 3.
> Сгенерировать n событий взаимодействия пользователя с объектами, убедиться, что все события корректно доставлены в clickhouse.

События генерируются в Web интерфейсе. Результат можно просмотреть в Redash

## Часть 4.
> Написать select запрос, результат, которого проиллюстрирует уникальных пользователей в срезе всех событий произошедших в прототипе по дням (clickhouse).

Запрос можно выполнить в Redash
```sql
SELECT
    toDate(e.time),
    e.name,
    e.action_id,
    COUNT(e.time) as `Количество`
FROM
    `tasktracker`.`events` e
GROUP BY
    toDate(e.time),
    e.name,
    e.action_id
```

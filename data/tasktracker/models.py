from django.db import models
from datetime import datetime
import pytz

utc=pytz.UTC

class User(models.Model):
    join_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания пользователя')
    registration_date = models.DateTimeField(auto_now=False, verbose_name='Дата регистрации пользователя')      
    name = models.CharField(max_length=200, verbose_name='имя пользователя')    
    email = models.EmailField(verbose_name='эл. почта пользователя') 
    def get_is_guest(self):        
        return (self.registration_date == datetime.min.replace(tzinfo=utc))

    def set_is_guest(self, value):        
        if (not value):
            self.registration_date = datetime.min.replace(tzinfo=utc)     

    is_guest = property(get_is_guest, set_is_guest)
     
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

class Step(models.Model):
    pass

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Action(models.Model):
    time = models.DateTimeField(auto_now=True, verbose_name='время события')         
    action_id = models.IntegerField(default=0, verbose_name='идентификатор действия')
    target_id = models.ForeignKey(Step, on_delete=models.CASCADE, verbose_name='идентификатор объекта над которым совершается действие (step_id)') 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='идентификатор пользователя')    

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


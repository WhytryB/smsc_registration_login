from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    #  Класс моделей в таблице для пользователя
    #  поле телефона пользователя называется - users, оно связанно с стандартным классом пользователя
    users = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personshop',  null=True)
    first_name = models.CharField('Имя', max_length=100, null=True, blank=False)
    second_name = models.CharField('Фамилия', max_length=100, null=True, blank=False)
    third_name = models.CharField('Отчество', max_length=100, null=True, blank=False)
    birthday = models.DateField('Дата рождения', null=True, blank=True)
    #  поле для храненения смс пароля пользователя
    sms_mes = models.CharField('Сообщение', max_length=100, null=True, blank=True)

    def __str__(self):
        return '{second_name} {first_name} {third_name}({birthday}){sms_mes}'.format (
            first_name=self.first_name,
            second_name=self.second_name,
            third_name=self.third_name,
            birthday=self.birthday,
            sms_mes = self.sms_mes
        )

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'




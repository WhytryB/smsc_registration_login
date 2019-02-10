from django import forms
from .models import Person
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UsersForm2(forms.Form):
    #  Класс формы, которая переопределяет валидацию юзернейма пользователя
    model = User
    username = forms.RegexField(label=_("Введите телефон: "),
                                regex=r'^((380\d{9})|((7|8)\d{10,11}))|(admin)$',
                                max_length=12,
                                help_text=_ ("Пример - '380934492757'"),
                                error_messages={'invalid': _("Только цифры, телефоны Украины и России,"
                                                             " не меньше 9 и не больше 12 символов")})


class UserForm(forms.ModelForm):
    # Класс формы которая расширяет функционал админки и добавляет поле username
    # на страницу добавления и редактирования персоны, а также изменяет валидацию юзернейма
    username = forms.RegexField(label=_("Введите телефон: "),
                                regex=r'^(380\d{9})|((7|8)\d{10,11})$',
                                max_length=12,
                                help_text=_ ("Пример - '380934492757'"),
                                error_messages={'invalid': _("Только цифры, телефоны Украины и России,"
                                                             " не меньше 9 и не больше 12 символов")})
    class Meta:
        model = User
        fields = ('username',)




class SmsForm(forms.ModelForm):
    #  Класс формы, поел которой хранит полученный код , который вводит пользователь при регитсрации или входе.
    sms_mes = forms.CharField(max_length=4,
                              label= "Введите полученный код",
                              required=False,
                              error_messages={
                                  'invalid': _("Не более 4 символов, только цифры и английские буквы"),
                                               })

    class Meta:
        model = Person
        fields = ('sms_mes',)


from django.shortcuts import render
from registration.models import Person
from registration.forms import UserForm, SmsForm, UsersForm2
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .smsc_api import *
import uuid

from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect


counter,mes = "1", "1"


def my_random_string(string_length=10):
    """ВОозвращает случайную строку"""
    random = str(uuid.uuid4())  # конвертирование UUID4 в строку.
    random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]




def registration(request):
    """
         Функция регистрации профиля персоны
         user_form -  работает из админки и содержит поле username пользвоателя
         sms_form -  Нужна для обработки кода смс
    """
    global counter,mes

    user_form = UserForm()
    sms_form = SmsForm()
    disabled,disabled2 = "","disabled" # Параметры кнопок,которые передаются в html

    if request.is_ajax():
        # Ajax запрос для автоматического определения ошибок при ввода телефона пользователем
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            return JsonResponse({'s': True})
        else:
            return JsonResponse({'error': user_form.errors})

    if request.method == "POST" and 'code' in request.POST or request.is_ajax():

        user_form = UserForm (request.POST)

        if user_form.is_valid():
            #  Отправка сообщения и валидация номера
            smsc = SMSC()
            phone = user_form.cleaned_data['username']
            mes = my_random_string(4)
            print(mes)
            # mes = "5"
            # counter = ['19', '1', '0.9', '194.4' ]
            # d = [ '-1' ]
            counter = smsc.send_sms(phones=phone, message=mes, sender="me") # Отправка смс с
            # введёными данными пользователя
            status_phone = smsc.get_status(phone=phone, id=counter[0])
            print(status_phone)

            if len(counter)<3 and status_phone[0] != "-1":
                #  Проверка статуса отправки сообщения сайтом
                messages.error(request, "Такого номера не существует    ")

            else:
                messages.success(request, "Код отправлен!")
                disabled = "disabled"
                disabled2 = ""

    if request.method == "POST" and 'reg' in request.POST:
        user_form = UserForm(request.POST)
        sms_form = SmsForm(request.POST)
        print(mes)#код отправки
        if user_form.is_valid () and sms_form.is_valid ():
            if mes == sms_form.cleaned_data['sms_mes']:# ПРоверка совпадает ли код пользователя и код отправленный ему
                # создание и аутентификаци персоны по введёным данным пользователя
                last_id = User.objects.latest('id').id   #  можно заменить на ваши модели
                last_i = Person.objects.latest('id').id  #  можно заменить на ваши модели
                password = "empty_password"
                User.objects.create_user (**user_form.cleaned_data, id=int(last_id)+1, password=password)
                create_person = Person(users_id = last_id+1, id = last_i+1)
                print(create_person)
                create_person.save()  #  сохранение новго пользователя и дальнейший его вход
                user = authenticate(
                    username=user_form.cleaned_data[ 'username' ],
                    password=password
                )
                login(request, user)
                messages.success (request, "Вы успешно зарегестрированы!")
                return redirect('edit_person', id=last_i+1)
            else:
                messages.error(request, "Вы ввели неверный код!")
                disabled2 = ""


    return render (request, 'sign_ip.html',
                   {"user_form": user_form,
                    "sms_form": sms_form,
                    "id": id,
                    "disabled": disabled,
                    "disabled2":disabled2})


def MyLoginView(request):
    """
         Функция входа пользователя на сайт
         user_form -  работает из админки и содержит поле username пользвоателя
         sms_form -  Нужна для обработки кода смс
       """
    global counter,mes
    user_form = UsersForm2()
    sms_form = SmsForm()
    disabled,disabled2 = "","disabled"

    if request.is_ajax():
        # Ajax запрос для автоматического определения ошибок при ввода телефона пользователем
        user_form = UsersForm2(request.POST)
        if user_form.is_valid():
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                return JsonResponse({'s': True})
            else:

                return JsonResponse({'error': {"username": "Такого номера в базе не существует!"}})
        else:
            return JsonResponse({'error': user_form.errors})

    if request.method == "POST" and 'code' in request.POST:

        user_form = UsersForm2(request.POST)
        if user_form.is_valid():
            # проверка существует ли пользователь с таким номером или нет
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                # Отправка сообщения и валидация номера
                smsc = SMSC ()
                phone = user_form.cleaned_data[ 'username' ]
                mes = my_random_string(4)
                print (mes)
                # mes = "5"
                # counter = [ '19', '1', '0.9', '194.4' ]
                # d = [ '-1' ]
                counter = smsc.send_sms(phones=phone, message=mes, sender="me")
                phone_status = smsc.get_status(phone=phone, id=counter[0])

                if len(counter) < 3 and phone_status[ 0 ] != "-1":
                    messages.error(request, "Вы ввели неверный телефон!")

                else:
                    messages.success (request, "Код отправлен!")
                    disabled = "disabled"
                    disabled2 = ""
                    data = {'message': phone}


            else:
                messages.error (request, "Такого номера в базе не существует!")

    if request.method == "POST" and 'reg' in request.POST:

        user_form = UsersForm2(request.POST)
        sms_form = SmsForm (request.POST)
        print(mes)
        if user_form.is_valid () and sms_form.is_valid ():
            password = "empty_password"
            # аутентификация пользователя
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=password
            )
            if user is not None:
                # Проверка валидности пользователя
                if mes == sms_form.cleaned_data['sms_mes']:
                    messages.success (request, "Вы успешно залогинили!")
                    login(request, user)
                    current_user = request.user.personshop.id
                    return redirect('person', id=current_user)
                else:
                    messages.error(request, "Вы ввели неверный код!")
                disabled2 = ""

    return render (request, 'login.html',
                   {"user_form": user_form,
                    "sms_form": sms_form,
                    "id": id,
                    "disabled": disabled,
                    "disabled2":disabled2})






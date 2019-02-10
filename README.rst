======================
sms_registration_login
======================

sms_registration_login это простое приложение для смс регитсрация и логина через
API "smsc".


Quick start
-----------
1.  Нужно установить все зависимые библиотеки, для этого в дикертории вашего проекта,
    перейдите  в терминал и пропишите команду::

    'pip install -r requirements.txt'

2. Добавить "registration" к вашим INSTALLED_APPS в настройках как показано ниже::

    INSTALLED_APPS = [
        ...
        'registration',
    ]

3. Добавить в ваш файл urls.py пути к view и задать url для registration и login::

    path('registration/', view.registration, name="signup"),
    path('login/', wi.MyLoginView, name='authapp-login'),

4. Запустите "python manage.py makemigrations", а затем "python manage.py migrate" для создания моделей registration.

5. Перейдите на http://127.0.0.1:8000/registration/ для создания нового пользователя.

6. Перейдите на http://127.0.0.1:8000/login/ для входа.
# Телегамм Бот
Бот предлагает зарегистрироваться указав имя, фамилию, пол. Автоматически сохраняется картинка профиля из телеграм.
Можно просматривать профили других зарегистрированных пользователей.

## Бот доступен по адресу @YPuzer_bot в будни с 11 до 20 часов МСК либо по запросу в ТГ.

## Стек
Python 3.10, PyTelegramBotAPI, Python telegram bot pagination, dotenv, postgreSQL

## Инструкция по запуску
* Клонируем репозиторий

	`
	git clone git@github.com:DOSuzer/hello_bot.git
	`


* Устанавливаем и активируем виртуальное окружение  

	`
    py -3.10 -m venv venv
    `
  
    `
    . venv/Scripts/activate
    `

* Устанавливаем зависимости из файла requirements.txt

	`
    pip install -r requirements.txt
    `

* В корне проекта создать файл .env и в него записать:

    - DB_USER='postgre'  имя пользователя БД

    - DB_PASS='password' пароль БД

    - TOKEN_API='...'    токен телеграм


* запускаем бота

    `
	python main.py
    `

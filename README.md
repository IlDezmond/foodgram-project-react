![workflow](https://github.com/IlDezmond/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Foodgram


### Описание

Продуктовый помощник - на этом сервисе пользователи смогут публиковать рецепты,
подписываться на публикации других пользователей, добавлять понравившиеся 
рецепты в список «Избранное», а перед походом в магазин скачивать сводный 
список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Вот, что было сделано в ходе работы над проектом:
- настроено взаимодействие Python-приложения с внешними API-сервисами;
- создан собственный API-сервис на базе проекта Django;
- подключено SPA к бэкенду на Django через API;
- созданы образы и запущены контейнеры Docker;
- созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;
- закреплены на практике основы DevOps, включая CI&CD.

## Как запустить проект

>*Клонировать репозиторий и перейти в него в командной строке:*


* ```bash
  git clone git@github.com:IlDezmond/foodgram-project-react.git
  ```

* ```bash
  cd foodgram-project-react/infra
  ```
  
>*Настроить переменные окружения в файле `.env` по пути `foodgram-project-react/infra`* <br>
>*Пример файла `example.env` находится там же`*

>*Собрать и запустить докер-контейнеры:*

* ```bash
  docker-compose up -d
  ```

>*Выполнить миграции, собрать статику, создать суперпользователя:*

* ```bash
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py collectstatic --no-input
  docker-compose exec web python manage.py createsuperuser
  ```

>*Открыть проект в браузере:*

* ```bash
  http://localhost
  ```

>*Для загрузки тестовых данных в БД, выполните команду в контейнере backend:*

* ```bash
    python manage.py loaddatautf8 data.json
  ```


### Полная документация к api находится по адресу

```URL
http://localhost/api/docs/
```

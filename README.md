# Проект "API для Yatube"
## Описание
Данный проект представляет собой API для блога. Он позволяет настроить взаимодействие с элементами блога вне зависимости от внешнего представления клиента и при необходимости добавить взаимодействие с другими приложениями.

Участники блога могут оставлять публикации и просматривать публикации других. Публикации могут относиться к какой-либо группе и имеют раздел комментариев от участников блога. Участники могут подписываться на других участников.
Неавторизованные пользователи могут просматривать публикации, комментарии и посты, но не могут добавлять, редактировать или удалять их. Группы доступны только для чтения всем пользователям.

Эндпоинты:
(`GET`, `POST`) - просмотреть свои подписки или подписаться на пользователя. Доступно только авторизованным пользователям. Доступен параметр search для GET-запроса подписок, начинающихся с заданной строки.
```
api/v1/follow/
```
(`GET`) - просмотреть группу с данным id.
```
api/v1/groups/{id}/
```
(`GET`) - просмотреть список групп.
```
api/v1/groups/
```
(`GET`, `POST`) - просмотреть список постов или создать новый. Доступны параметры limit и offset. Неавторизованным пользователям доступен только GET-запрос.
```
api/v1/posts/
```
(`GET`, `PUT`, `PATCH`, `DELETE`) - просмотреть конкретный пост (доступно неавторизованным пользователям), редактировать его или удалить.
```
api/v1/posts/{id}/
```
(`GET`, `POST`) - просмотреть список комментариев к посту с id, равным post_pk, или создать новый. Неавторизованным пользователям доступно только чтение.
```
api/v1/posts/{post_pk}/comments/
```
(`GET`, `PUT`, `POST`, `DELETE`) - просмотреть конкретный комментарий к посту (доступно неавторизованным пользователям), редактировать его или удалить.
```
api/v1/posts/{post_pk}/comments/{id}/
```
(`POST`) - получить JWT-токен для зарегистрированного пользователя.
```
api/v1/jwt/create/
```
(`POST`) - обновить JWT-токен для зарегистрированного пользователя.
```
api/v1/jwt/refresh/
```
(`POST`) - подтвердить JWT-токен.
```
api/v1/jwt/verify/
```

Примеры запросов можно просмотреть [ниже](#примеры-запросов).

## Установка:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/TheTangerineOwl/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python yatube_api/manage.py migrate
```

Запустить проект:

```
python yatube_api/manage.py runserver
```

## Примеры запросов

Получить JWT-токен пользователя `example` с паролем `somepassword`:
```
POST api/v1/jwt/create/
{
"username": "example",
"password": "somepassword"
}
```

"""Task:
Приложение состоит из 2 страниц:
1. Главная страница - список статей и кнопка добавить новую.
2. Создание статьи - страница с формой создания. (статьи хранить в глобальной переменной)

Задания:
1. На главной странице вывести список статей (сортировка от новых к
   старым). Для каждой статьи должны быть: заголовок, дата создания,
   текст, теги.
   Если статей больше 5, должна быть постраничная навигация с шагом в 5
   страниц.

2 На странице с формой создания статьи:
    a. Добавить ввод названия, текста, списка тегов. Теги вводятся через
       запятую или пробел.
    b. После создания статьи необходимо перенаправить пользователя на
       главную страницу.
    c. Если не заполнены какие то из полей, вывести соответствующую ошибку.
"""


from aiohttp import web
import aiohttp_jinja2
import jinja2

from app.routes import setup_routes
from app.config import Config
from app.middlewares import setup_middlewares


def create_app():
    app = web.Application()
    setup_routes(app)
    setup_middlewares(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(Config.BASE_DIR) + '/templates'))
    return app


aiohttp_app = create_app

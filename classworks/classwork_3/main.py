"""Task:
Создать приложение, позволяющее
сложить/вычесть/перемножить/поделить 2 числа. Вернуться со
страницы результата на ввод новых значений. Сохранять последние 3
операции и их результат для текущего пользователя.

Для выбора операции используйте html тэг select:
    <select name="operation">
    <option selected value="add">Сумма</option>
    <option value="sub">Вычитание</option>
    <option value="mul">Произведение</option>
    <option value="div">Деление</option>
    </select>
"""


from aiohttp import web
import aiohttp_jinja2
import jinja2

from routes import setup_routes
from config import Config


app = web.Application()
setup_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(Config.BASE_DIR) + '/templates'))
web.run_app(app)

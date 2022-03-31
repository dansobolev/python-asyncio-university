import json

from aiohttp import web
import aiohttp_jinja2

from exceptions import UnknownOperationTypeException, OperationTypeMissingException
from config import Config


async def health(request: web.Request) -> web.Response:
    return web.Response(text='We are ready to serve you!')


async def input_name(request) -> web.Response:
    if request.method == 'POST':
        data = await request.post()
        data = dict(data)
        operation = data.get('operation')
        if not 'operation':
            # TODO: configure exception handling
            raise OperationTypeMissingException("Missing operation type field")

        first_num = int(data['first_num'])
        second_num = int(data['second_num'])
        if operation == 'add':
            result = first_num + second_num
        elif operation == 'sub':
            result = first_num - second_num
        elif operation == 'mul':
            result = first_num * second_num
        elif operation == 'div':
            result = first_num / second_num
        else:
            raise UnknownOperationTypeException("Unknown operation type")

        data.update({'result': result})
        history = request.cookies.get('history')
        if not history:
            history_data = json.dumps([data])
        else:
            history_data = json.loads(history)
            if len(history_data) < 3:
                history_data.append(data)
            elif len(history_data) == 3:
                del history_data[0]
                history_data.append(data)
            history_data = json.dumps(history_data)

        redirect_location = Config.BASE_URL + str(request.app.router['input-name'].url_for())
        response = aiohttp_jinja2.render_template(
            'output.html', request, {'result': result, 'redirect': redirect_location})
        response.set_cookie('history', history_data)

        return response

    elif request.method == 'GET':
        history = request.cookies.get('history')
        context = {}
        if history:
            history_data = json.loads(history)
            context = {'history_data': history_data}
        return aiohttp_jinja2.render_template('input.html', request, context=context)

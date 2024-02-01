from sanic import json


class HelloRoute:

    @staticmethod
    async def get(request):
        return json({"res": "Hello, world."})

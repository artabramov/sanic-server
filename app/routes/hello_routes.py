from sanic import json
from app.models.user_models import User


class HelloRoute:

    @staticmethod
    async def get(request):
        # conn = request.ctx.conn
        user = User("user_login", "pass_hash", "first_name", "last_name")
        async with request.ctx.conn as conn:
            conn.commit()
        return json({"res": "Hello, world."})

from sanic import json
from app.models.user_models import User


class HelloRoute:

    @staticmethod
    async def get(request):
        user = User("user_login8", "pass_hash", "first_name", "last_name")
        user.mfa_key_encrypted = "asd8"
        user.jti_encrypted = "asdfsdf8"

        await request.ctx.entity_manager.insert(user, commit=True)
        await request.ctx.cache_manager.set(user)

        request.app.ctx.log.debug("hello, world")
        return json({"res": "Hello, world."})

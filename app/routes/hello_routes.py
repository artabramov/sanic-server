from sanic import json
from app.models.user_models import User


class HelloRoute:

    @staticmethod
    async def get(request):
        # user = User("user_login1", "pass_hash", "first_name", "last_name")
        # user.mfa_key_encrypted = "asd1"
        # user.jti_encrypted = "asdfsdf1"

        # request.ctx.session.add(user)
        # await request.ctx.session.flush()
        # await request.ctx.session.commit()

        request.app.ctx.log.debug("hello, world")
        return json({"res": "Hello, world."})

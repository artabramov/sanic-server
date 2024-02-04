from sanic import json
from app.models.user_models import User
from app.schemas.user_schemas import UserRegister
from sanic_ext import validate


class UserRoutes:

    @staticmethod
    @validate(query=UserRegister)
    async def get(request):
        """Register a new user.

        Now we will add some more details

        openapi:
        ---
        tags: ['users']
        parameters:
          - name: user_login
            type: string
            required: true
            in: query
            description: Latin string with length from 2 to 24.
          - name: user_pass
            type: string
            required: true
            in: query
            description: String no less than length 6.
          - name: first_name
            type: string
            required: true
            in: query
            description: String from 2 to 24 length without redundant spaces.
          - name: last_name
            type: string
            required: true
            in: query
            description: String from 2 to 24 length without redundant spaces.
        responses:
          200:
            description: OK
          422:
            description: Unprocessable Content
          500:
            description: Internal Server Error
        """
        user = User("user_login8", "pass_hash", "first_name", "last_name")
        user.mfa_key_encrypted = "asd8"
        user.jti_encrypted = "asdfsdf8"

        await request.ctx.entity_manager.insert(user, commit=True)
        await request.ctx.cache_manager.set(user)

        request.app.ctx.log.debug("hello, world")
        return json({"res": "Hello, world."})

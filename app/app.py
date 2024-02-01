from sanic import Sanic
from app.routes.hello_routes import HelloRoute
from app.config import get_config


app = Sanic("MyHelloWorldApp")
app.config.update(get_config())

app.add_route(HelloRoute.get, '/', methods=["GET"])

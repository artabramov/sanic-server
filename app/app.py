from sanic import Sanic
from app.routes.hello_routes import HelloRoute
from app.config import get_config
from app.context import ctx
from uuid import uuid4
import os
import time
from app.session import SessionCreator, Base
from app.logger import LoggerCreator


app = Sanic("Hide", config=get_config())
app.add_route(HelloRoute.get, '/', methods=["GET"])



@app.before_server_start
async def before_server_start(app, _):
	logger_creator = LoggerCreator(app.config)
	app.ctx.log = logger_creator.create_logger()

	app.ctx.session_creator = SessionCreator(app.config)
	async with app.ctx.session_creator.async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


@app.on_request
async def on_request(request):
	"""Create session and request identifiers."""
	ctx.trace_request_uuid = str(uuid4())
	ctx.pid = os.getpid()

	request.ctx.request_start_time = time.time()
	request.ctx.session = request.app.ctx.session_creator.create_session()
	request.app.ctx.log.debug("Request received, method=%s, url=%s, headers=%s." % (
		request.method, str(request.url), str(request.headers)))


@app.on_response
async def on_response(request, response):
    request_elapsed_time = time.time() - request.ctx.request_start_time
    request.app.ctx.log.debug("Response sent, request_elapsed_time=%s, status=%s, headers=%s, body=%s." % (
        request_elapsed_time, response.status, str(response.headers), response.body.decode("utf-8")))

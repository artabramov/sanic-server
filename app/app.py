from sanic import Sanic
from app.routes.user_routes import UserRoutes
from app.config import get_config
from app.context import ctx
from uuid import uuid4
import os
import time
from app.session import SessionCreator, Base
from app.cache import CacheCreator
from app.logger import LoggerCreator
from app.managers.entity_manager import EntityManager
from app.managers.cache_manager import CacheManager
from sanic import json
# from sanic_ext import Extend

app = Sanic("hide", config=get_config())
app.add_route(UserRoutes.get, '/', methods=["GET"])
# Extend(app)


@app.exception(Exception)
async def catch_anything(request, exception):
    return json({"error": "fuck"})


@app.before_server_start
async def before_server_start(app, _):
	logger_creator = LoggerCreator(app.config)
	app.ctx.log = logger_creator.create_logger()

	cache_creator = CacheCreator(app.config)
	app.ctx.cache = await cache_creator.create_cache()

	app.ctx.session_creator = SessionCreator(app.config)
	async with app.ctx.session_creator.async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


@app.on_request
async def on_request(request):
	"""Create session and request identifiers."""
	ctx.trace_request_uuid = str(uuid4())
	ctx.pid = os.getpid()

	request.ctx.request_start_time = time.time()

	session = request.app.ctx.session_creator.create_session()
	request.ctx.entity_manager = EntityManager(session, request.app.ctx.log)

	request.ctx.cache_manager = CacheManager(request.app.ctx.cache, request.app.ctx.log, request.app.config.REDIS_EXPIRE)
	
	request.app.ctx.log.debug("Request received, method=%s, url=%s, headers=%s." % (
		request.method, str(request.url), str(request.headers)))


@app.on_response
async def on_response(request, response):
    request_elapsed_time = time.time() - request.ctx.request_start_time
    request.app.ctx.log.debug("Response sent, request_elapsed_time=%s, status=%s, headers=%s, body=%s." % (
        request_elapsed_time, response.status, str(response.headers), response.body.decode("utf-8")))

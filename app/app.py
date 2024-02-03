from sanic import Sanic
from app.routes.hello_routes import HelloRoute
from app.config import get_config
# from app.session import SessionCreator, Base


app = Sanic("Hide", config=get_config())
app.add_route(HelloRoute.get, '/', methods=["GET"])



@app.before_server_start
async def setup_db(app, _):
	pass
	# app.ctx.session_creator = SessionCreator(app.config)
	# async with app.ctx.session_creator.engine.begin() as conn:
	# 	await conn.run_sync(Base.metadata.create_all)


@app.on_request
async def example(request):
	request.ctx.conn = request.app.ctx.session_creator.get_session()
	print("I execute before the handler.")


@app.on_response
async def example(request, response):
	print("I execute after the handler.")
